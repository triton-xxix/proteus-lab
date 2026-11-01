// P-0286: open the built v8-live.html from file:// in headless Chromium (teardown's own playwright),
// wait, count canvases, console errors and outside requests, screenshot, write load.json.
import { createRequire } from "node:module";
import { writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const SRC = "/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD";
const HERE = "/Users/triton/PROTEUS/experiments/2026-11-01-P-0286";
const { chromium } = createRequire(SRC + "/package.json")("playwright");

const out = { errors: [], requests: [] };
const browser = await chromium.launch({ headless: true, args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
page.on("console", (m) => { if (m.type() === "error") out.errors.push(m.text()); });
page.on("pageerror", (e) => out.errors.push(String(e)));
page.on("request", (q) => { if (!/^(file|data|blob):/.test(q.url())) out.requests.push(q.url()); });
const t = Date.now();
await page.goto(pathToFileURL(SRC + "/teardown-out/dist/v8-live.html").href);
await page.waitForTimeout(8000);
out.load_s = (Date.now() - t) / 1000;
out.title = await page.title();
out.canvases = await page.evaluate(() => document.querySelectorAll("canvas").length);
out.webgl = await page.evaluate(() => { const c = document.querySelector("canvas"); return !!(c && (c.getContext("webgl2") || c.getContext("webgl"))); });
out.buttons = await page.evaluate(() => document.querySelectorAll("button").length);
out.body_text_chars = await page.evaluate(() => document.body.innerText.length);
out.fps = await page.evaluate(() => new Promise((res) => { let n = 0; const t0 = performance.now(); const f = () => { n++; if (performance.now() - t0 < 3000) requestAnimationFrame(f); else res(n / 3); }; requestAnimationFrame(f); }));
writeFileSync(HERE + "/load.json", JSON.stringify(out, null, 1));
// software GL is slow; a first screenshot attempt timed out at 30 s
try { await page.screenshot({ path: HERE + "/v8-live.png", timeout: 90000 }); out.screenshot = true; }
catch (e) { out.screenshot = String(e).slice(0, 120); }
await browser.close();
writeFileSync(HERE + "/load.json", JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
