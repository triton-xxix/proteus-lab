// Real headless Chromium check of the page at desktop and phone width (the browser pane is denied unattended):
// serves the folder through Playwright routes, reports page errors, horizontal overflow, and how many charts drew,
// clicks the miss filter, and writes full-page PNGs to the folder given as the first argument.
//   node docs/probes/numbers/render.mjs <out-folder>
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const DIR = '/Users/triton/PROTEUS/docs/probes/numbers';
const OUT = process.argv[2];
fs.mkdirSync(OUT, {recursive: true});
const req = createRequire('/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD/x.js');
const {chromium} = req('playwright');
const S = JSON.parse(fs.readFileSync(DIR + '/data.json', 'utf8')).summary;

const browser = await chromium.launch({headless: true});
let bad = 0;
for (const [name, vp] of [['desktop', {width: 1280, height: 900}], ['phone', {width: 375, height: 812}]]) {
  const page = await browser.newPage({viewport: vp});
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.route('http://numbers.test/**', (route) => {
    const p = new URL(route.request().url()).pathname.replace(/^\//, '') || 'index.html';
    const f = path.join(DIR, p);
    if (fs.existsSync(f)) route.fulfill({path: f}); else route.fulfill({status: 404, body: ''});
  });
  await page.goto('http://numbers.test/index.html');
  await page.waitForSelector('#list .call');
  await page.waitForTimeout(300);
  const r = await page.evaluate(() => ({
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    h1: document.querySelector('#h1').textContent,
    charts: [...document.querySelectorAll('svg')].map((s) => s.id + ':' + s.children.length),
    calls: document.querySelectorAll('#list .call').length,
    clipped: [...document.querySelectorAll('svg text')].filter((t) => {
      const b = t.getBoundingClientRect(), s = t.ownerSVGElement.getBoundingClientRect();
      return b.left < s.left - 1 || b.right > s.right + 1;
    }).map((t) => t.textContent).slice(0, 10),
  }));
  const top = await page.evaluate(() => Math.round(document.querySelector('#list').getBoundingClientRect().top + window.scrollY));
  await page.screenshot({path: `${OUT}/${name}.png`, fullPage: true, clip: {x: 0, y: 0, width: vp.width, height: top + 300}});
  await page.click('#filters button[data-k="miss"]');
  const miss = await page.evaluate(() => document.querySelectorAll('#list .call').length);
  console.log(name, JSON.stringify({...r, miss_filter: miss, errors}));
  if (r.overflow > 0 || errors.length || r.calls !== S.n || miss !== S.miss || r.clipped.length) bad++;
  await page.close();
}
await browser.close();
console.log('render', bad ? `${bad} views with problems` : 'OK');
process.exit(bad ? 1 : 0);
