// Lints docs/probes/index.html (the every-probe index) and runs its script against data.json with a stub
// DOM, since the browser pane is denied in scheduled runs. Fails on unbalanced tags, missing local links,
// a script error, an empty chart, undefined/NaN in the output, or a list or filter that disagrees with data.json.
// node /Users/triton/PROTEUS/docs/probes/check.cjs
const fs = require('fs'), path = require('path'), vm = require('vm');
const DIR = __dirname;
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

const d = JSON.parse(fs.readFileSync(path.join(DIR, 'data.json'), 'utf8'));
for (const r of d.rows) if (r.page && !fs.existsSync(path.join(DIR, r.id, 'index.html'))) errs.push(`row ${r.id} links a missing page`);

const els = {};
const el = id => els[id] || (els[id] = {id, innerHTML: '', textContent: '', clientWidth: 0, value: '', style: {}, attrs: {}, on: {},
  setAttribute(k, v) { this.attrs[k] = v; }, addEventListener(k, f) { this.on[k] = f; }});
const document = {querySelector: s => el(s.replace(/^[#.]/, '')), querySelectorAll: () => [], addEventListener() {}};
const fetch = () => Promise.resolve({json: () => Promise.resolve(d)});
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const ctx = {document, fetch, window: {innerWidth: 860}, addEventListener() {}, setTimeout, clearTimeout, console};
const lis = () => (el('list').innerHTML.match(/<li>/g) || []).length;
const S = d.summary;
(async () => {
for (const w of [860, 375]) {
  ctx.window.innerWidth = w;
  for (const k in els) delete els[k];
  try { vm.runInNewContext(script, ctx); } catch (e) { errs.push(`script threw at ${w}px: ${e.message}`); }
  await new Promise(r => setTimeout(r, 50));
  for (const id of ['stats', 'legend', 'mix', 'weeks', 'src', 'filters', 'list'])
    if (!el(id).innerHTML || /undefined|NaN/.test(el(id).innerHTML)) errs.push(`#${id} empty or undefined/NaN at ${w}px`);
  for (const id of ['h1', 'kicker', 'weeknote', 'srcnote', 'count'])
    if (!el(id).textContent || /undefined|NaN/.test(el(id).textContent)) errs.push(`#${id} bad at ${w}px`);
  if (!el('h1').textContent.includes(`${S.n} probes`) || !el('h1').textContent.includes(`${S.by_verdict.works} worked`)) errs.push('headline numbers missing');
  if (lis() !== Math.min(30, S.n)) errs.push(`list shows ${lis()} rows, want ${Math.min(30, S.n)}`);
  if (!el('count').textContent.startsWith(`${S.n} shown`)) errs.push(`count says "${el('count').textContent}"`);
  const vb = el('weeks').attrs.viewBox || '';
  if (!vb.endsWith(' 220') || +vb.split(' ')[2] < 300) errs.push(`weeks viewBox ${vb} at ${w}px`);
  if (w === 860) {
    el('filters').on.click({target: {closest: () => ({dataset: {v: 'blocked'}})}});
    if (!el('count').textContent.startsWith(`${S.by_verdict.blocked} shown`)) errs.push(`blocked filter says "${el('count').textContent}"`);
    if (/t-works/.test(el('list').innerHTML)) errs.push('blocked filter shows a works row');
    el('q').value = 'P-0200';
    el('filters').on.click({target: {closest: () => ({dataset: {v: 'all'}})}});
    el('q').on.input();
    if (lis() !== 1 || !el('list').innerHTML.includes('href="P-0200/"')) errs.push('search for P-0200 did not give one row with its drawn page');
    console.log('srcnote:', el('srcnote').textContent);
    console.log('weeknote:', el('weeknote').textContent);
  }
}
  errs.forEach(e => console.log('FAIL', e));
  console.log('check probes index', errs.length ? `${errs.length} problems` : 'OK', '| bytes', html.length, '| verdicts', S.n);
  process.exit(errs.length ? 1 : 0);
})();
