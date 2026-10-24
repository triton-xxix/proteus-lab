#!/usr/bin/env node
// Lint for the Inception deep page. Reads the built HTML (default sites/builds/nolan/inception/index.html,
// or a URL's body saved to a file passed as argv[2]) and the data it was built from, and fails if:
// the computed durations are missing from the body, a tag pair is unbalanced, "undefined" or "NaN"
// leaked in, the viewport meta is missing, or the converter script does not run on a stub DOM.
'use strict';
const fs = require('fs');
const path = require('path');
const { human } = require('../lib/inception.cjs');

const file = process.argv[2] || path.resolve(__dirname, '..', '..', 'builds', 'nolan', 'inception', 'index.html');
const html = fs.readFileSync(file, 'utf8');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'research', 'clocks.json'), 'utf8'));
const fails = [];

for (const l of data.levels) {
  const h = data.flight_hours * Math.pow(data.factor_per_level, l.id);
  const want = human(h);
  if (!html.includes(want)) fails.push(`missing duration for ${l.name}: ${want}`);
  if (!html.includes(l.film_word)) fails.push(`missing film word for ${l.name}: ${l.film_word}`);
}
for (const tag of ['main', 'section', 'table', 'ol', 'li', 'svg', 'figure', 'script', 'form', 'select', 'output']) {
  const open = (html.match(new RegExp(`<${tag}[\\s>]`, 'g')) || []).length;
  const close = (html.match(new RegExp(`</${tag}>`, 'g')) || []).length;
  if (open !== close) fails.push(`unbalanced <${tag}>: ${open} open, ${close} close`);
}
if (/undefined|NaN|\[object/.test(html)) fails.push('undefined, NaN or [object leaked into the page');
if (!/<meta name="viewport"/.test(html)) fails.push('no viewport meta');
if (!/data\/inception-clocks\.json/.test(html)) fails.push('no link to the data');

// Run the inline script on a stub DOM: one input, one select, five outputs.
const script = (html.match(/<script>([\s\S]*?)<\/script>/) || [])[1];
if (!script) fails.push('no inline script');
else {
  const outputs = data.levels.map(l => ({ dataset: { level: String(l.id), q: l.rate_holds === false ? '1' : '' }, textContent: '' }));
  const handlers = {};
  const n = { value: String(data.flight_hours), addEventListener: (e, f) => { handlers['n' + e] = f; } };
  const u = { value: '1', addEventListener: (e, f) => { handlers['u' + e] = f; } };
  const out = { dataset: { factor: String(data.factor_per_level) }, querySelectorAll: () => outputs };
  const document = { getElementById: id => ({ 'conv-n': n, 'conv-u': u, 'conv-out': out })[id] };
  try {
    new Function('document', script)(document);
    n.value = '1'; u.value = '1';
    handlers.ninput();
    const want = data.levels.map(l => human(Math.pow(data.factor_per_level, l.id)) + (l.rate_holds === false ? '?' : ''));
    outputs.forEach((o, i) => { if (o.textContent !== want[i]) fails.push(`converter at 1 hour, level ${i}: ${o.textContent} v ${want[i]}`); });
  } catch (e) { fails.push('inline script threw: ' + e.message); }
}

if (fails.length) { console.error('FAIL\n' + fails.map(f => ' - ' + f).join('\n')); process.exit(1); }
console.log(`OK ${path.basename(file)}: ${html.length} bytes, ${data.levels.length} levels checked, converter ran on a stub DOM`);
