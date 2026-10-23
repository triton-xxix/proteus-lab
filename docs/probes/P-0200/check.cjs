// Lints docs/probes/P-0200 and runs the page script against data.json with a stub DOM, since the
// browser pane is denied in scheduled runs. Fails on unbalanced tags, missing local links, a data.json
// that differs from the probe's results.json, a script error, or an empty chart.
// node /Users/triton/PROTEUS/docs/probes/P-0200/check.cjs
const fs = require('fs'), path = require('path'), vm = require('vm');
const DIR = __dirname, RES = path.join(DIR, '../../../experiments/2026-10-23-P-0200/results.json');
const html = fs.readFileSync(path.join(DIR, 'index.html'), 'utf8');
const errs = [];

const VOID = new Set(['meta', 'link', 'br', 'img', 'input', 'hr']);
const body = html.replace(/<style>[\s\S]*?<\/style>/, '').replace(/<script>[\s\S]*?<\/script>/, '');
const stack = [];
for (const m of body.matchAll(/<(\/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(\/?)>/g)) {
  const [, close, tag, self] = m, t = tag.toLowerCase();
  if (VOID.has(t) || self) continue;
  if (!close) stack.push(t);
  else if (stack[stack.length - 1] === t) stack.pop();
  else errs.push(`unexpected </${t}>, open ${stack.slice(-3)}`);
}
if (stack.length) errs.push(`unclosed ${stack}`);
for (const m of body.matchAll(/href="([^"]+)"/g)) {
  const h = m[1];
  if (!/^(https?:|#|mailto:)/.test(h) && !fs.existsSync(path.join(DIR, h))) errs.push(`missing local link ${h}`);
}

const dataText = fs.readFileSync(path.join(DIR, 'data.json'), 'utf8');
if (dataText !== fs.readFileSync(RES, 'utf8')) errs.push('data.json differs from results.json');
const d = JSON.parse(dataText);

const els = {};
const el = id => els[id] || (els[id] = {id, innerHTML: '', textContent: '', clientWidth: 0, attrs: {},
  setAttribute(k, v) { this.attrs[k] = v; }});
const document = {querySelector: s => el(s.replace(/^#/, '').replace(' tbody', '-tbody')), addEventListener() {}};
const fetch = () => Promise.resolve({json: () => Promise.resolve(d)});
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const ctx = {document, fetch, window: {innerWidth: 860}, addEventListener() {}, setTimeout, clearTimeout, console};
(async () => {
for (const w of [860, 375]) {
  ctx.window.innerWidth = w;
  for (const k in els) delete els[k];
  try { vm.runInNewContext(script, ctx); } catch (e) { errs.push(`script threw at ${w}px: ${e.message}`); }
  await new Promise(r => setTimeout(r, 50)).then(() => {
    for (const id of ['stats', 'paths', 'calls', 'tbl-tbody']) if (!el(id).innerHTML) errs.push(`#${id} empty at ${w}px`);
    for (const id of ['shape', 'limits']) if (!el(id).textContent || /undefined|NaN/.test(el(id).textContent)) errs.push(`#${id} bad at ${w}px`);
    for (const id of ['stats', 'paths', 'calls', 'tbl-tbody']) if (/undefined|NaN/.test(el(id).innerHTML)) errs.push(`#${id} has undefined/NaN at ${w}px`);
    const rows = (el('tbl-tbody').innerHTML.match(/<tr>/g) || []).length;
    if (rows !== d.trail.length) errs.push(`table has ${rows} rows, data ${d.trail.length}`);
    if (!el('stats').innerHTML.includes(d.final.full.toFixed(2))) errs.push('full Kelly final missing from stats');
    if (w === 860) console.log('shape:', el('shape').textContent);
  });
}
  errs.forEach(e => console.log('FAIL', e));
  console.log('check P-0200', errs.length ? `${errs.length} problems` : 'OK', '| bytes', html.length, '| calls', d.trail.length);
  process.exit(errs.length ? 1 : 0);
})();
