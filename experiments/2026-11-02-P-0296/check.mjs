// Headless check of the deepened page at desktop (1600x900) and phone (375x812) width: the text against
// all rows of P-0294's v86 screen, horizontal overflow, the slider taking over, a seed change, page errors.
//   node experiments/2026-11-02-P-0296/check.mjs
import fs from 'node:fs';
import {createRequire} from 'node:module';

const EXP = '/Users/triton/PROTEUS/experiments/2026-11-02-P-0296';
const PAGE = EXP + '/out/dist/2026-11-02-P-0296.html';
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
const shot = fs.readFileSync('/Users/triton/PROTEUS/experiments/2026-11-02-P-0294/screen.txt', 'utf8').split('\n');
const emu = shot.slice(shot.findIndex((r) => r.startsWith('no os involved')) + 1);
while (emu.length && emu[emu.length - 1] === '') emu.pop();

const browser = await chromium.launch({headless: true});
const res = {page_kb: Math.round(fs.statSync(PAGE).size / 1024), views: {}};
for (const [name, vp] of [['desktop', {width: 1600, height: 900}], ['phone', {width: 375, height: 812}]]) {
  const page = await browser.newPage({viewport: vp});
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto('file://' + PAGE);
  await page.waitForFunction(() => window.BOOTGPT && window.SIM && window.SIM.ready, null, {timeout: 20000});
  const got = await page.evaluate(() => window.BOOTGPT);
  const sim = screen(got.text);
  const full = emu.length - 1;
  let differ = 0;
  for (let i = 0; i < full; i++) if (emu[i] !== sim[i]) differ++;
  // the slider takes over from the clock
  await page.evaluate(() => { const s = document.getElementById('bg-step'); s.value = '161'; s.dispatchEvent(new Event('input')); });
  await page.waitForTimeout(300);
  const sliderHeld = await page.evaluate(() => document.getElementById('bg-step').value);
  await page.screenshot({path: `${EXP}/${name}-step161.png`});
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  // a seed change regenerates the run
  await page.fill('#bg-seed', '1235');
  await page.dispatchEvent('#bg-seed', 'change');
  const other = await page.evaluate(() => window.BOOTGPT);
  res.views[name] = {
    rows_compared: emu.length, full_rows_differing: differ, last_row_prefix_match: sim[full].startsWith(emu[full]),
    printed_chars_compared: emu.reduce((a, r) => a + r.length, 0), horizontal_overflow_px: overflow,
    slider_value_after_300ms: sliderHeld, seed_after_change: '0x' + other.seed.toString(16),
    seed_change_new_text: other.text !== got.text, first_chars_seed_1235: other.text.slice(0, 30), page_errors: errors,
  };
  await page.close();
}
await browser.close();
fs.writeFileSync(EXP + '/results.json', JSON.stringify(res, null, 1));
console.log(JSON.stringify(res, null, 1));
