#!/usr/bin/env node
// webgpu-check: does a WebGPU page actually render in headless Chrome, with no console errors?
// Drives Chrome over the DevTools protocol on a real clock, because Chrome's one-shot
// --screenshot / --dump-dom flags never let an async WebGPU start finish (found in Proteus probe P-0173).
// No dependencies: Node 22 or later (built-in fetch and WebSocket) and an installed Chrome.
//
// Usage: node webgpu_check.mjs <url-or-file> [--wait 10000] [--watch "#fps,#err"] [--out dir]
//                              [--size 1280x720] [--chrome /path/to/chrome] [--port 9333]
// Exit code: 0 pass, 1 fail (no adapter, a console error or exception, or a blank frame), 2 could not run.
import { spawn } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
const opt = (name, dflt) => { const i = argv.indexOf("--" + name); return i >= 0 ? argv[i + 1] : dflt; };
const target = argv.find((a, i) => !a.startsWith("--") && !(i > 0 && argv[i - 1].startsWith("--")));
if (!target) { console.error("usage: node webgpu_check.mjs <url-or-file> [--wait ms] [--watch sel,sel] [--out dir]"); process.exit(2); }
const URL_ = /^[a-z]+:\/\//i.test(target) ? target : pathToFileURL(resolve(target)).href;
const WAIT = Number(opt("wait", 10000));
const WATCH = (opt("watch", "") || "").split(",").map((s) => s.trim()).filter(Boolean);
const OUT = resolve(opt("out", "."));
const [W, H] = opt("size", "1280x720").split("x").map(Number);
const PORT = Number(opt("port", 9333));
const CHROME = opt("chrome", [
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser",
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
].find((p) => existsSync(p)));
if (!CHROME) { console.error("no Chrome found; pass --chrome /path/to/chrome"); process.exit(2); }
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

mkdirSync(OUT, { recursive: true });
const profile = mkdtempSync(join(tmpdir(), "webgpu-check-"));
const chrome = spawn(CHROME, ["--headless=new", `--user-data-dir=${profile}`, "--enable-unsafe-webgpu",
  "--no-first-run", "--no-default-browser-check", `--window-size=${W},${H}`, `--remote-debugging-port=${PORT}`,
  "about:blank"], { stdio: "ignore" });
const quit = (code) => { try { chrome.kill(); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} process.exit(code); };

let targets = [];
for (let i = 0; i < 60 && !targets.some((t) => t.type === "page"); i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); } catch {}
  await sleep(250);
}
const page = targets.find((t) => t.type === "page");
if (!page) { console.error(`Chrome did not open a debugging port on ${PORT}`); quit(2); }

const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pending = new Map(); const events = []; let t0 = Date.now();
ws.addEventListener("message", (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); return; }
  const p = d.params || {};
  if (d.method === "Runtime.consoleAPICalled")
    events.push({ ms: Date.now() - t0, kind: p.type, text: p.args.map((a) => a.value ?? a.description).join(" ").slice(0, 300) });
  else if (d.method === "Runtime.exceptionThrown")
    events.push({ ms: Date.now() - t0, kind: "exception", text: (p.exceptionDetails.exception?.description || p.exceptionDetails.text).slice(0, 300) });
  else if (d.method === "Log.entryAdded")
    events.push({ ms: Date.now() - t0, kind: "log-" + p.entry.level, text: p.entry.text.slice(0, 300) });
});
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expr) => (await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;

await send("Runtime.enable"); await send("Log.enable"); await send("Page.enable");
t0 = Date.now();
await send("Page.navigate", { url: URL_ });
const samples = [];
for (let s = 1000; s <= WAIT; s += 1000) {
  await sleep(1000);
  const row = { ms: Date.now() - t0 };
  for (const sel of WATCH) row[sel] = await evaluate(`document.querySelector(${JSON.stringify(sel)})?.textContent ?? null`);
  samples.push(row);
}
const gpu = await evaluate(`(async()=>{ if(!navigator.gpu) return {api:false};
  const a = await navigator.gpu.requestAdapter(); if(!a) return {api:true, adapter:null};
  const i = a.info || {}; return {api:true, adapter:{vendor:i.vendor||"", architecture:i.architecture||"", description:i.description||""},
  fallback: a.isFallbackAdapter ?? i.isFallbackAdapter ?? null}; })()`);
const canvases = await evaluate(`[...document.querySelectorAll("canvas")].map(c=>[c.width,c.height])`);
const shot = (await send("Page.captureScreenshot", { format: "png" })).result.data;
writeFileSync(join(OUT, "shot.png"), Buffer.from(shot, "base64"));

// Blank-frame test: decode our own screenshot in a 2D canvas (a WebGPU canvas cannot be read back reliably).
const frame = await evaluate(`(async()=>{ const img = new Image(); img.src = "data:image/png;base64,${shot}";
  await img.decode(); const w = 160, h = Math.max(1, Math.round(160 * img.height / img.width));
  const c = new OffscreenCanvas(w, h); const g = c.getContext("2d"); g.drawImage(img, 0, 0, w, h);
  const d = g.getImageData(0, 0, w, h).data; const counts = new Map(); let dark = 0;
  for (let i = 0; i < d.length; i += 4) { const k = (d[i]>>4)<<8 | (d[i+1]>>4)<<4 | (d[i+2]>>4);
    counts.set(k, (counts.get(k)||0) + 1); if (d[i] + d[i+1] + d[i+2] < 30) dark++; }
  const n = d.length / 4; return { colours: counts.size, top: Math.max(...counts.values()) / n, dark: dark / n }; })()`);

const errors = events.filter((e) => ["error", "exception", "log-error", "assert"].includes(e.kind));
const reasons = [];
if (!gpu?.api) reasons.push("navigator.gpu missing");
else if (!gpu.adapter) reasons.push("no WebGPU adapter");
if (errors.length) reasons.push(`${errors.length} console error(s) or exception(s)`);
if (frame && frame.top > 0.98) reasons.push(`blank frame (${(frame.top * 100).toFixed(1)}% one colour)`);
const result = { url: URL_, verdict: reasons.length ? "fail" : "pass", reasons, waitMs: WAIT, size: [W, H],
  node: process.version, chrome: CHROME, gpu, canvases, frame, samples, events, errors: errors.length,
  checkedAt: new Date().toISOString() };
writeFileSync(join(OUT, "results.json"), JSON.stringify(result, null, 1) + "\n");
console.log(`${result.verdict.toUpperCase()} ${URL_}`);
console.log(`  adapter: ${gpu?.adapter ? [gpu.adapter.vendor, gpu.adapter.architecture].filter(Boolean).join(" ") || "unnamed" : "none"}`);
console.log(`  console errors: ${errors.length}, frame: ${frame?.colours} colours, ${(frame?.top * 100).toFixed(1)}% top colour`);
for (const r of reasons) console.log(`  fail: ${r}`);
console.log(`  wrote ${join(OUT, "results.json")} and shot.png`);
ws.close();
quit(reasons.length ? 1 : 0);
