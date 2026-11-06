// Lints docs/probes/numbers/index.html and runs its script against data.json with a stub DOM at 860 and 375 px,
// since the browser pane is denied in scheduled runs. Fails on unbalanced tags, missing local links, a script
// error, an empty chart, undefined/NaN in the output, counts that do not sum, or a filter that shows the wrong rows.
// node /Users/triton/PROTEUS/docs/probes/numbers/check.cjs
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
const S = d.summary;
if (S.hit + S.partial + S.miss + S.unscored !== S.n) errs.push('scores do not sum to n');
if (d.rows.length !== S.n) errs.push('rows length differs from summary');
if (d.rows.filter(r => r.word).length !== S.word_hits) errs.push('word hits differ');
if (d.slices.reduce((a, s) => a + s.n, 0) !== S.n) errs.push('slices do not cover every call');
if (d.bins.reduce((a, s) => a + s.n, 0) !== S.n) errs.push('bins do not cover every call');
if (d.rows.some(r => !r.reason)) errs.push(`${d.rows.filter(r => !r.reason).length} rows have no reason`);
if (/—/.test(JSON.stringify(d.rows.map(r => r.reason)))) errs.push('em dash in a reason');

const els = {};
const el = id => els[id] || (els[id] = {id, innerHTML: '', textContent: '', clientWidth: 0, style: {}, attrs: {},
  setAttribute(k, v) { this.attrs[k] = v; }});
const buttons = {};
const document = {
  querySelector: s => el(s.replace(/^[#.]/, '').replace(/ .*/, '')),
  querySelectorAll: () => ['all', 'hit', 'partial', 'miss', 'unscored'].map(k => ({
    getAttribute: () => k, addEventListener: (_, fn) => { buttons[k] = fn; } })),
  addEventListener() {},
};
const fetch = () => Promise.resolve({json: () => Promise.resolve(d)});
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const ctx = {document, fetch, addEventListener() {}, window: {innerWidth: 860}, setTimeout, clearTimeout, console};
(async () => {
for (const w of [860, 375]) {
  ctx.window.innerWidth = w;
  for (const k in els) delete els[k];
  try { vm.runInNewContext(script, ctx); } catch (e) { errs.push(`script threw at ${w}px: ${e.message}`); }
  await new Promise(r => setTimeout(r, 50));
  for (const id of ['stats', 'cross', 'ratio', 'tol', 'bins', 'slices', 'list', 'filters'])
    if (!el(id).innerHTML || /undefined|NaN/.test(el(id).innerHTML)) errs.push(`#${id} empty or undefined/NaN at ${w}px`);
  for (const id of ['h1', 'kicker', 'crossnote', 'ratnote', 'tolnote', 'sure', 'betternote', 'how', 'lastid', 'audit'])
    if (!el(id).textContent || /undefined|NaN|null/.test(el(id).textContent)) errs.push(`#${id} bad at ${w}px`);
  const listed = (el('list').innerHTML.match(/class="call"/g) || []).length;
  if (listed !== S.n) errs.push(`list shows ${listed}, want ${S.n}`);
  for (const k of ['miss', 'hit', 'partial', 'unscored']) {
    if (!buttons[k]) { errs.push(`no handler for ${k}`); continue; }
    buttons[k]();
    const n = (el('list').innerHTML.match(/class="call"/g) || []).length;
    if (n !== S[k]) errs.push(`filter ${k} shows ${n}, want ${S[k]}`);
  }
  const pairs = d.rows.filter(r => r.said && r.got != null && r.said * r.got > 0).length;
  const dots = (el('ratio').innerHTML.match(/<circle/g) || []).length;
  if (dots !== pairs) errs.push(`ratio draws ${dots} dots, want ${pairs}`);
  if (pairs !== S.same_sign) errs.push(`same-sign count ${S.same_sign} differs from drawn ${pairs}`);
  for (const id of ['cross', 'ratio', 'tol', 'bins', 'slices']) {
    const vb = el(id).attrs.viewBox || '';
    if (+vb.split(' ')[2] < 300) errs.push(`${id} viewBox ${vb} at ${w}px`);
  }
  if (w === 860) for (const id of ['h1', 'crossnote', 'ratnote', 'tolnote', 'sure', 'betternote', 'how']) console.log(id + ':', el(id).textContent);
}
  errs.forEach(e => console.log('FAIL', e));
  console.log('check numbers', errs.length ? `${errs.length} problems` : 'OK', '| bytes', html.length, '| calls', S.n);
  process.exit(errs.length ? 1 : 0);
})();
