// P-0299: render stack-diagram's built HTML to light and dark PNGs of .canvas at scale 2, the way its
// render_png.py does, but with the Node Playwright already in the sandbox (no Python Playwright here).
//   node experiments/2026-11-02-P-0299/render.mjs
import fs from 'node:fs';
import {createRequire} from 'node:module';

const EXP = '/Users/triton/PROTEUS/experiments/2026-11-02-P-0299';
const req = createRequire('/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD/x.js');
const {chromium} = req('playwright');

const browser = await chromium.launch({headless: true});
const res = {html_kb: Math.round(fs.statSync(EXP + '/out.html').size / 1024), themes: {}};
for (const theme of ['light', 'dark']) {
  const page = await browser.newPage({viewport: {width: 1200, height: 800}, deviceScaleFactor: 2});
  const errors = [];
  const requests = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('request', (r) => { if (!r.url().startsWith('file:') && !r.url().startsWith('data:')) requests.push(r.url()); });
  await page.goto('file://' + EXP + '/out.html');
  if (theme === 'dark') await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
  await page.waitForTimeout(300);
  const info = await page.evaluate(() => {
    const imgs = [...document.querySelectorAll('img')];
    const visible = imgs.filter((i) => i.offsetParent !== null);
    const groups = [...document.querySelectorAll('.group')].map((g) => g.getBoundingClientRect());
    const nodes = [...document.querySelectorAll('.node')].map((n) => n.getBoundingClientRect());
    const inside = nodes.filter((n) => groups.some((g) => n.left >= g.left && n.right <= g.right && n.top >= g.top && n.bottom <= g.bottom)).length;
    return {imgs: imgs.length, visible: visible.length, broken: visible.filter((i) => !i.complete || i.naturalWidth === 0).length,
      nodes: nodes.length, nodes_inside_a_group: inside};
  });
  await page.locator('.canvas').screenshot({path: `${EXP}/diagram-${theme}.png`});
  res.themes[theme] = {...info, page_errors: errors.length, network_requests: requests.length};
  await page.close();
}
await browser.close();
fs.writeFileSync(EXP + '/render.json', JSON.stringify(res, null, 2));
console.log(JSON.stringify(res));
