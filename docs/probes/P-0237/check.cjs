// Lints docs/probes/P-0237 and runs the page script against data.json with a stub DOM, since the
// browser pane is denied in scheduled runs. Fails on unbalanced tags, missing local links, a data.json
// that differs from the probe's results.json, a script error, an empty chart, a wrong dot or row count,
// or headline numbers that do not match the probe's README.
// node /Users/triton/PROTEUS/docs/probes/P-0237/check.cjs
const fs = require('fs'), path = require('path'), vm = require('vm');
const DIR = __dirname, EXP = path.join(DIR, '../../../experiments/2026-10-27-P-0237');
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
const P = d.books.pinnacle, A = d.books.average, n = P.buckets.length;
const readme = fs.readFileSync(path.join(EXP, 'README.md'), 'utf8');
const pc = v => (100 * v).toFixed(1) + '%';
for (const v of [d.matches.toLocaleString('en-GB'), P.matches_with_odds.toLocaleString('en-GB'),
  P.buckets[0].win_rate.toFixed(3), pc(P.buckets[n - 1].roi), pc(A.buckets[n - 1].roi), pc(P.favourite_every_match.roi), pc(A.favourite_every_match.roi)])
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
    for (const id of ['stats', 'wr', 'roi', 'tbl-tbody']) {
      if (!el(id).innerHTML) errs.push(`#${id} empty at ${w}px`);
      if (/undefined|NaN|Infinity/.test(el(id).innerHTML)) errs.push(`#${id} has undefined/NaN at ${w}px`);
    }
    for (const id of ['shape', 'fav', 'caveats']) if (!el(id).textContent || /undefined|NaN/.test(el(id).textContent)) errs.push(`#${id} bad at ${w}px`);
    const rows = (el('tbl-tbody').innerHTML.match(/<tr>/g) || []).length;
    if (rows !== 2 * n) errs.push(`table has ${rows} rows, want ${2 * n}`);
    const wrDots = (el('wr').innerHTML.match(/<circle/g) || []).length;
    if (wrDots !== 4 * n) errs.push(`win-rate chart has ${wrDots} dots, want ${4 * n}`);
    const roiDots = (el('roi').innerHTML.match(/<circle/g) || []).length;
    if (roiDots !== 2 * n) errs.push(`return chart has ${roiDots} dots, want ${2 * n}`);
    if (!el('stats').innerHTML.includes(pc(P.buckets[n - 1].roi))) errs.push('longshot return missing from stats');
    if (!el('stats').innerHTML.includes(d.matches.toLocaleString('en-GB'))) errs.push('match count missing from stats');
    if (w === 860) console.log('shape:', el('shape').textContent, '\nfav:', el('fav').textContent);
  });
}
  errs.forEach(e => console.log('FAIL', e));
  console.log('check P-0237', errs.length ? `${errs.length} problems` : 'OK', '| bytes', html.length, '| bands', n);
  process.exit(errs.length ? 1 : 0);
})();
