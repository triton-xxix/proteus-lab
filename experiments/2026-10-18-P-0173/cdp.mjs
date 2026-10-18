// P-0173 leg 2: drive headless Chrome over CDP on a real clock, so the async WebGPU start can finish.
// Captures console, exceptions, #fps and #err text, the adapter's info, and a screenshot after WAIT ms.
// Usage: node cdp.mjs [waitMs] [chromePath]
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const PAGE = "file:///Users/triton/PROTEUS/sandbox/p0173-ocean.min.html";
const WAIT = Number(process.argv[2] || 10000);
const CHROME = process.argv[3] || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(CHROME, ["--headless=new", "--user-data-dir=/Users/triton/PROTEUS/sandbox/p0173-profile",
  "--enable-unsafe-webgpu", "--no-first-run", "--window-size=1280,720", `--remote-debugging-port=${PORT}`, "about:blank"],
  { stdio: "ignore" });

let targets;
for (let i = 0; i < 40; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); if (targets.length) break; } catch {}
  await sleep(250);
}
const page = targets.find((t) => t.type === "page");
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pending = new Map(); const events = [];
ws.addEventListener("message", (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); }
  else if (d.method === "Runtime.consoleAPICalled")
    events.push({ t: Date.now(), kind: d.params.type, text: d.params.args.map((a) => a.value ?? a.description).join(" ").slice(0, 300) });
  else if (d.method === "Runtime.exceptionThrown")
    events.push({ t: Date.now(), kind: "exception", text: (d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text).slice(0, 300) });
  else if (d.method === "Log.entryAdded")
    events.push({ t: Date.now(), kind: "log-" + d.params.entry.level, text: d.params.entry.text.slice(0, 300) });
});
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expr) => (await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;

await send("Runtime.enable"); await send("Log.enable"); await send("Page.enable");
const t0 = Date.now();
await send("Page.navigate", { url: PAGE });
const samples = [];
for (let s = 1000; s <= WAIT; s += 1000) {
  await sleep(1000);
  samples.push({ ms: Date.now() - t0, fps: await evaluate("document.getElementById('fps')?.textContent"),
    err: await evaluate("document.getElementById('err')?.textContent") });
}
const gpu = await evaluate(`(async()=>{ if(!navigator.gpu) return {gpu:false};
  const a = await navigator.gpu.requestAdapter(); if(!a) return {gpu:true, adapter:null};
  const i = a.info || {}; return {gpu:true, adapter:{vendor:i.vendor, architecture:i.architecture, description:i.description}, fallback: a.isFallbackAdapter ?? null}; })()`);
const canvas = await evaluate("(()=>{const c=document.getElementById('c'); return c? [c.width,c.height]:null})()");
const shot = await send("Page.captureScreenshot", { format: "png" });
writeFileSync(join(HERE, "shot-cdp.png"), Buffer.from(shot.result.data, "base64"));
const res = { node: process.version, chrome: CHROME, waitMs: WAIT, gpu, canvas, samples,
  events: events.map((e) => ({ ...e, t: e.t - t0 })),
  errors: events.filter((e) => e.kind === "error" || e.kind === "exception" || e.kind === "log-error").length };
writeFileSync(join(HERE, "results-cdp.json"), JSON.stringify(res, null, 1));
console.log(JSON.stringify(res, null, 1).slice(0, 6000));
ws.close(); chrome.kill();
process.exit(0);
