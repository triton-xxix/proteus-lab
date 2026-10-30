// Lints docs/ladder/index.html and runs its script against data.json with a stub DOM at 860 and 375 px,
// since the browser pane is denied in scheduled runs. Fails on unbalanced tags, missing local links, a script
// error, an empty chart, undefined/NaN in the output, or a table or headline that disagrees with data.json.
// node /Users/triton/PROTEUS/docs/ladder/check.cjs
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
if (S.wins + S.draws + S.losses !== S.games) errs.push('result split does not sum to games');
if (d.games.length !== S.games) errs.push('games array length differs from summary');
if (S.accepted + S.declined + S.no_answer + S.refused_400 + S.refused_429 !== S.challenges) errs.push('challenge verdicts do not sum');

const els = {};
const el = id => els[id] || (els[id] = {id, innerHTML: '', textContent: '', clientWidth: 0, style: {}, attrs: {},
  setAttribute(k, v) { this.attrs[k] = v; }});
const document = {querySelector: s => el(s.replace(/^[#.]/, '').replace(/ .*/, '')), querySelectorAll: () => []};
const fetch = () => Promise.resolve({json: () => Promise.resolve(d)});
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const ctx = {document, fetch, window: {innerWidth: 860, addEventListener() {}}, setTimeout, clearTimeout, console};
(async () => {
for (const w of [860, 375]) {
  ctx.window.innerWidth = w;
  for (const k in els) delete els[k];
  try { vm.runInNewContext(script, ctx); } catch (e) { errs.push(`script threw at ${w}px: ${e.message}`); }
  await new Promise(r => setTimeout(r, 50));
  for (const id of ['stats', 'ladder', 'bands', 'asks', 'no', 'meaning', 'games'])
    if (!el(id).innerHTML || /undefined|NaN/.test(el(id).innerHTML)) errs.push(`#${id} empty or undefined/NaN at ${w}px`);
  for (const id of ['h1', 'kicker', 'laddernote', 'bandnote', 'asknote', 'nonote'])
    if (!el(id).textContent || /undefined|NaN/.test(el(id).textContent)) errs.push(`#${id} bad at ${w}px`);
  if (!el('h1').textContent.includes(`${S.games} games`) || !el('h1').textContent.includes(`${S.losses} lost`)) errs.push('headline numbers missing');
  const rows = (el('games').innerHTML.match(/<tr /g) || []).length;
  if (rows !== S.games) errs.push(`table shows ${rows} rows, want ${S.games}`);
  const dots = (el('ladder').innerHTML.match(/<circle/g) || []).length;
  if (dots !== S.games) errs.push(`ladder draws ${dots} dots, want ${S.games}`);
  const vb = el('ladder').attrs.viewBox || '';
  if (+vb.split(' ')[2] < 300) errs.push(`ladder viewBox ${vb} at ${w}px`);
  if (!el('meaning').innerHTML.includes(String(S.strongest_beaten))) errs.push('strongest beaten missing from the meaning paragraph');
  if (w === 860) { console.log('h1:', el('h1').textContent); console.log('bandnote:', el('bandnote').textContent); }
}
  errs.forEach(e => console.log('FAIL', e));
  console.log('check ladder', errs.length ? `${errs.length} problems` : 'OK', '| bytes', html.length, '| games', S.games, '| challenges', S.challenges);
  process.exit(errs.length ? 1 : 0);
})();
