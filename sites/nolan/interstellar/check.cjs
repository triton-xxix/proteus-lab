#!/usr/bin/env node
// Lint for the Interstellar deep page. Reads the built HTML (default sites/builds/nolan/interstellar/index.html,
// or a saved live body passed as argv[2]) and the data it was built from, and fails if: the computed
// numbers (ratio, surface time, each leg's Earth time) are missing, a tag pair is unbalanced, "undefined"
// or "NaN" leaked in, the viewport meta is missing, or the converter does not run on a stub DOM.
'use strict';
const fs = require('fs');
const path = require('path');
const { human } = require('../lib/inception.cjs');
const { model, hm } = require('../lib/interstellar.cjs');

const file = process.argv[2] || path.resolve(__dirname, '..', '..', 'builds', 'nolan', 'interstellar', 'index.html');
const html = fs.readFileSync(file, 'utf8');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'research', 'clocks.json'), 'utf8'));
const m = model(data);
const fails = [];

const want = [Math.round(m.ratio).toLocaleString('en-GB'), hm(m.surfaceH), data.claims.find(c => c.id === 'earth_elapsed_total').value, human(m.oneHourGapY * 24 * 365.25)];
for (const l of m.legs) want.push(human(l.earth));
for (const w of want) if (!html.includes(w)) fails.push(`missing from body: ${w}`);
for (const tag of ['main', 'section', 'table', 'ol', 'li', 'svg', 'figure', 'script', 'form', 'select', 'output']) {
  const open = (html.match(new RegExp(`<${tag}[\\s>]`, 'g')) || []).length;
  const close = (html.match(new RegExp(`</${tag}>`, 'g')) || []).length;
  if (open !== close) fails.push(`unbalanced <${tag}>: ${open} open, ${close} close`);
}
if (/undefined|NaN|\[object/.test(html)) fails.push('undefined, NaN or [object leaked into the page');
if (!/<meta name="viewport"/.test(html)) fails.push('no viewport meta');
if (!/data\/interstellar-clocks\.json/.test(html)) fails.push('no link to the data');

const script = (html.match(/<script>([\s\S]*?)<\/script>/) || [])[1];
if (!script) fails.push('no inline script');
else {
  const handlers = {};
  const n = { value: '1', addEventListener: (e, f) => { handlers['n' + e] = f; } };
  const u = { value: '1', addEventListener: (e, f) => { handlers['u' + e] = f; } };
  const earth = { textContent: '' };
  const out = { dataset: { ratio: String(m.ratio) } };
  const document = { getElementById: id => ({ 'conv-n': n, 'conv-u': u, 'conv-earth': earth, 'conv-out': out })[id] };
  try {
    new Function('document', script)(document);
    handlers.ninput();
    if (earth.textContent !== human(m.ratio)) fails.push(`converter at 1 hour: ${earth.textContent} v ${human(m.ratio)}`);
    n.value = '1'; u.value = String(1 / 3600); handlers.uchange();
    if (earth.textContent !== human(m.ratio / 3600)) fails.push(`converter at 1 second: ${earth.textContent} v ${human(m.ratio / 3600)}`);
  } catch (e) { fails.push('inline script threw: ' + e.message); }
}

if (fails.length) { console.error('FAIL\n' + fails.map(f => ' - ' + f).join('\n')); process.exit(1); }
console.log(`OK ${path.basename(file)}: ${html.length} bytes, ${want.length} numbers found, converter ran on a stub DOM (1 hour = ${human(m.ratio)}, 1 second = ${human(m.ratio / 3600)})`);
