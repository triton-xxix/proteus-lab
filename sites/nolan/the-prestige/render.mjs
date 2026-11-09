// Real headless Chromium check of the built Prestige page at desktop and phone width (the browser pane is
// denied unattended). Serves the build folder through Playwright routes, reports page errors, horizontal
// overflow, clipped chart labels and how many list rows drew, drags the scrubber to beat 8, flips the order
// toggle, and writes PNGs to the folder given as the first argument.
//   node sites/nolan/the-prestige/render.mjs <out-folder>
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const DIR = '/Users/triton/PROTEUS/sites/builds/nolan';
const OUT = process.argv[2];
fs.mkdirSync(OUT, {recursive: true});
const req = createRequire('/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD/x.js');
const {chromium} = req('playwright');
const data = JSON.parse(fs.readFileSync('/Users/triton/PROTEUS/sites/nolan/the-prestige/research/layers.json', 'utf8'));
const beat8 = data.beats.find((b) => b.film === 8);

const browser = await chromium.launch({headless: true});
let bad = 0;
for (const [name, vp] of [['desktop', {width: 1280, height: 900}], ['phone', {width: 375, height: 812}]]) {
  const page = await browser.newPage({viewport: vp});
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.route('http://prestige.test/**', (route) => {
    const p = new URL(route.request().url()).pathname.replace(/^\//, '');
    const f = path.join(DIR, p.endsWith('/') ? p + 'index.html' : p);
    if (fs.existsSync(f)) route.fulfill({path: f}); else route.fulfill({status: 404, body: ''});
  });
  await page.goto('http://prestige.test/the-prestige/');
  await page.waitForSelector('#seqs .seq');
  await page.waitForTimeout(400);
  await page.evaluate(() => { const n = document.getElementById('sc-n'); n.value = '8'; n.dispatchEvent(new Event('input', {bubbles: true})); });
  await page.waitForTimeout(400);
  const r = await page.evaluate(() => ({
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    what: document.getElementById('sc-what').textContent,
    open: document.querySelectorAll('.nest__l.is-on').length,
    rows: document.querySelectorAll('#seqs .seq').length,
    clipped: [...document.querySelectorAll('svg text')].filter((t) => {
      const b = t.getBoundingClientRect(), s = t.ownerSVGElement.getBoundingClientRect();
      return b.left < s.left - 1 || b.right > s.right + 1;
    }).map((t) => t.textContent).slice(0, 10),
  }));
  await page.screenshot({path: `${OUT}/${name}.png`, fullPage: true});
  await page.click('.mem__toggle button[data-order="story"]');
  const first = await page.evaluate(() => document.querySelector('#seqs .seq').dataset.story);
  console.log(name, JSON.stringify({...r, first_after_toggle: first, errors}));
  if (r.overflow > 0 || errors.length || r.rows !== data.beats.length || r.what !== beat8.what || first !== '1' || r.clipped.length) bad++;
  await page.close();
}
await browser.close();
console.log('render', bad ? `${bad} views with problems` : 'OK');
process.exit(bad ? 1 : 0);
