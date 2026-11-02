// Open the built page headless, read window.BOOTGPT.text, lay it out on an 80-column screen and compare it
// row by row with the v86 boot's screen (P-0294 screen.txt); screenshot one frame mid-run.
//   node experiments/2026-11-02-P-0295/check.mjs
import fs from 'node:fs';
import {createRequire} from 'node:module';

const EXP = '/Users/triton/PROTEUS/experiments/2026-11-02-P-0295';
const req = createRequire('/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD/x.js');
const {chromium} = req('playwright');

const screen = (text) => {
  const rows = [];
  let cur = '';
  for (const ch of text) {
    if (ch === '\n') { rows.push(cur); cur = ''; continue; }
    cur += ch;
    if (cur.length === 80) { rows.push(cur); cur = ''; }
  }
  rows.push(cur);
  return rows.map((r) => r.replace(/\s+$/, ''));
};

const browser = await chromium.launch({headless: true});
const page = await browser.newPage({viewport: {width: 1600, height: 900}});
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const t0 = Date.now();
await page.goto('file://' + EXP + '/out/dist/bootgpt-teardown.html?capture');
await page.waitForFunction(() => window.BOOTGPT && window.SIM && window.SIM.ready, null, {timeout: 20000});
const loadMs = Date.now() - t0;
const got = await page.evaluate(() => { window.SIM.render(12); return window.BOOTGPT; });
await page.screenshot({path: EXP + '/frame-12s.png'});
await browser.close();

const shot = fs.readFileSync('/Users/triton/PROTEUS/experiments/2026-11-02-P-0294/screen.txt', 'utf8').split('\n');
const hdr = shot.findIndex((r) => r.startsWith('no os involved'));
const emu = shot.slice(hdr + 1);
while (emu.length && emu[emu.length - 1] === '') emu.pop();
const sim = screen(got.text);
const full = emu.length - 1;
let differ = 0;
for (let i = 0; i < full; i++) if (emu[i] !== sim[i]) differ++;
const res = {
  page_kb: Math.round(fs.statSync(EXP + '/out/dist/bootgpt-teardown.html').size / 1024),
  load_ms: loadMs, seed: '0x' + got.seed.toString(16), steps: got.steps, page_errors: errors,
  emulator_full_rows: full, rows_differing: differ, last_row_prefix_match: sim[full].startsWith(emu[full]),
  printed_chars_compared: emu.reduce((a, r) => a + r.length, 0),
};
fs.writeFileSync(EXP + '/results.json', JSON.stringify(res, null, 1));
console.log(JSON.stringify(res, null, 1));
