#!/usr/bin/env node
// Lint for the Dunkirk deep page. Reads the built HTML (default sites/builds/nolan/dunkirk/index.html,
// or a URL's body saved to a file passed as argv[2]) and the data it was built from, and fails if:
// a computed speed or span is missing from the body, a crossing is missing, a tag pair is unbalanced,
// "undefined" or "NaN" leaked in, the viewport meta is missing, or the scrubber script does not run
// on a stub DOM.
'use strict';
const fs = require('fs');
const path = require('path');
const { human } = require('../lib/inception.cjs');
const { placeCrossings, perFilmMinute } = require('../lib/dunkirk.cjs');

const file = process.argv[2] || path.resolve(__dirname, '..', '..', 'builds', 'nolan', 'dunkirk', 'index.html');
const html = fs.readFileSync(file, 'utf8');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'research', 'strands.json'), 'utf8'));
const fails = [];
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');

for (const s of data.strands) {
  if (!html.includes(human(s.span_hours))) fails.push(`missing span for ${s.name}: ${human(s.span_hours)}`);
  const pm = human(perFilmMinute(s, data.runtime_min));
  if (!html.includes(pm)) fails.push(`missing per-film-minute for ${s.name}: ${pm}`);
}
const at = placeCrossings(data.crossings, data.strands);
for (const c of data.crossings) {
  const { h, bound } = at.get(c.id);
  if (h == null) fails.push(`crossing ${c.id} has no placeable strand`);
  else if (!html.includes(`${bound ? 'no earlier than' : 'about'} ${human(h)} before the end`)) fails.push(`crossing ${c.id} position missing: ${human(h)}`);
  if (!html.includes(esc(c.what).slice(0, 40)) && !html.includes(c.what.slice(0, 40))) fails.push(`crossing ${c.id} text missing`);
}
for (const tag of ['main', 'section', 'ol', 'li', 'svg', 'figure', 'script', 'form', 'output', 'g']) {
  const open = (html.match(new RegExp(`<${tag}[\\s>]`, 'g')) || []).length;
  const close = (html.match(new RegExp(`</${tag}>`, 'g')) || []).length;
  if (open !== close) fails.push(`unbalanced <${tag}>: ${open} open, ${close} close`);
}
if (/undefined|NaN|\[object/.test(html)) fails.push('undefined, NaN or [object leaked into the page');
if (!/<meta name="viewport"/.test(html)) fails.push('no viewport meta');
if (!/data\/dunkirk-strands\.json/.test(html)) fails.push('no link to the data');

// Run the inline script on a stub DOM: one range input, one minute output, one output per strand.
const script = (html.match(/<script>([\s\S]*?)<\/script>/) || [])[1];
if (!script) fails.push('no inline script');
else {
  const outputs = data.strands.map(s => ({ dataset: { span: String(s.span_hours) }, textContent: '' }));
  const handlers = {};
  const m = { value: '0', dataset: { runtime: String(data.runtime_min) }, addEventListener: (e, f) => { handlers[e] = f; } };
  const mv = { textContent: '' };
  const out = { querySelectorAll: () => outputs };
  const document = { getElementById: id => ({ 'dk-m': m, 'dk-mv': mv, 'dk-out': out })[id] };
  try {
    new Function('document', script)(document);
    m.value = String(data.runtime_min);
    handlers.input();
    data.strands.forEach((s, i) => { if (outputs[i].textContent !== human(s.span_hours)) fails.push(`scrubber at the last minute, ${s.name}: ${outputs[i].textContent} v ${human(s.span_hours)}`); });
    if (mv.textContent !== String(data.runtime_min)) fails.push('minute label did not update');
  } catch (e) { fails.push('inline script threw: ' + e.message); }
}

if (fails.length) { console.error('FAIL\n' + fails.map(f => ' - ' + f).join('\n')); process.exit(1); }
console.log(`OK ${path.basename(file)}: ${html.length} bytes, ${data.strands.length} strands and ${data.crossings.length} crossings checked, scrubber ran on a stub DOM`);
