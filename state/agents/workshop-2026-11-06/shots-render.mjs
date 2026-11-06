// One-off: real Chromium over docs/probes/shots after the 6 Nov edits (no check script exists for that page).
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const DIR = '/Users/triton/PROTEUS/docs/probes/shots';
const req = createRequire('/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD/x.js');
const {chromium} = req('playwright');
const browser = await chromium.launch({headless: true});
for (const vp of [{width: 1280, height: 900}, {width: 375, height: 812}]) {
  const page = await browser.newPage({viewport: vp});
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.route('http://shots.test/**', (route) => {
    const f = path.join(DIR, new URL(route.request().url()).pathname.replace(/^\//, ''));
    if (fs.existsSync(f)) route.fulfill({path: f}); else route.fulfill({status: 404, body: ''});
  });
  await page.goto('http://shots.test/index.html');
  await page.waitForSelector('#strip circle');
  const r = await page.evaluate(() => ({
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    h1: document.querySelector('#h1').textContent,
    calnote: document.querySelector('#calnote').textContent,
    why: document.querySelector('#why').textContent.slice(0, 260),
    axis: [...document.querySelectorAll('#strip text')].map((t) => t.textContent).filter((t) => !t.endsWith('%')),
    misses: document.querySelectorAll('#miss tbody tr').length,
  }));
  console.log(vp.width, JSON.stringify({...r, errors}));
  await page.close();
}
await browser.close();
