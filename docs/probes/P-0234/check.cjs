// Lints docs/probes/P-0234 and runs the page script against data.json with a stub DOM, since the
// browser pane is denied in scheduled runs. Fails on unbalanced tags, missing local links, a data.json
// that differs from the probe's results.json, a script error, an empty chart, or headline numbers
// that do not match the probe's README.
// node /Users/triton/PROTEUS/docs/probes/P-0234/check.cjs
const fs = require('fs'), path = require('path'), vm = require('vm');
const DIR = __dirname, EXP = path.join(DIR, '../../../experiments/2026-10-27-P-0234');
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
if (dataText !== fs.readFileSync(path.join(EXP, 'results.json'), 'utf8')) errs.push('data.json differs from results.json');
const d = JSON.parse(dataText);
const readme = fs.readFileSync(path.join(EXP, 'README.md'), 'utf8');
for (const v of [d.summary.node_saving_pct + '%', String(d.summary.base.ebf_pooled), String(d.summary.lmr.ebf_pooled)])
  if (!readme.includes(v)) errs.push(`README does not carry ${v}`);

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
    for (const id of ['stats', 'ebf', 'save', 'tbl-tbody']) {
      if (!el(id).innerHTML) errs.push(`#${id} empty at ${w}px`);
      if (/undefined|NaN|Infinity/.test(el(id).innerHTML)) errs.push(`#${id} has undefined/NaN at ${w}px`);
    }
    for (const id of ['shape', 'games']) if (!el(id).textContent || /undefined|NaN/.test(el(id).textContent)) errs.push(`#${id} bad at ${w}px`);
    const rows = (el('tbl-tbody').innerHTML.match(/<tr>/g) || []).length;
    if (rows !== d.rows.length) errs.push(`table has ${rows} rows, data ${d.rows.length}`);
    const dots = (el('ebf').innerHTML.match(/<circle/g) || []).length;
    if (dots !== 2 * d.rows.length) errs.push(`ebf chart has ${dots} dots, want ${2 * d.rows.length}`);
    if (!el('stats').innerHTML.includes(d.summary.node_saving_pct.toFixed(1))) errs.push('node saving missing from stats');
    if (w === 860) console.log('shape:', el('shape').textContent, '\ngames:', el('games').textContent);
  });
}
  errs.forEach(e => console.log('FAIL', e));
  console.log('check P-0234', errs.length ? `${errs.length} problems` : 'OK', '| bytes', html.length, '| positions', d.rows.length);
  process.exit(errs.length ? 1 : 0);
})();
