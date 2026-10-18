// P-0175: open a Meta Ads Library search in headless Chrome (fresh profile, never logged in) over CDP,
// wait, scroll a little, then save the page text, a screenshot and a summary. Reuses P-0173's cdp.mjs shape.
// Usage: node adlib.mjs [query] [waitMs]
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const Q = process.argv[2] || "plumber";
const WAIT = Number(process.argv[3] || 12000);
const URL = `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=GB&q=${encodeURIComponent(Q)}&search_type=keyword_unordered&media_type=all`;
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9334;
const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(CHROME, ["--headless=new", "--user-data-dir=/Users/triton/PROTEUS/sandbox/p0175-profile",
  "--no-first-run", "--window-size=1280,1600", `--user-agent=${UA}`, "--lang=en-GB", `--remote-debugging-port=${PORT}`, "about:blank"],
  { stdio: "ignore" });

let targets;
for (let i = 0; i < 40; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); if (targets.length) break; } catch {}
  await sleep(250);
}
const page = targets.find((t) => t.type === "page");
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pending = new Map();
ws.addEventListener("message", (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expr) => (await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;

await send("Page.enable");
await send("Page.navigate", { url: URL });
await sleep(WAIT);
for (let k = 0; k < 4; k++) { await evaluate("window.scrollBy(0, 1400)"); await sleep(1500); }
const text = (await evaluate("document.body.innerText")) || "";
const finalUrl = await evaluate("location.href");
const title = await evaluate("document.title");
const shot = await send("Page.captureScreenshot", { format: "png" });
writeFileSync(join(HERE, `shot-${Q}.png`), Buffer.from(shot.result.data, "base64"));
writeFileSync(join(HERE, `text-${Q}.txt`), text);
const count = text.match(/~?[\d,]+\s+results?/i);
const res = { at: new Date().toISOString(), query: Q, url: URL, finalUrl, title, chars: text.length,
  results_line: count ? count[0] : null, login_wall: /log in|log into facebook|you must log in/i.test(text.slice(0, 2000)),
  library_ids: (text.match(/Library ID: \d+/g) || []).length, sponsored: (text.match(/Sponsored/g) || []).length };
writeFileSync(join(HERE, `summary-${Q}.json`), JSON.stringify(res, null, 1));
console.log(JSON.stringify(res, null, 1));
ws.close(); chrome.kill();
process.exit(0);
