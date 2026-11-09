#!/usr/bin/env node
// Lint for The Prestige deep page. Reads the built HTML (default sites/builds/nolan/the-prestige/index.html,
// or a saved live body passed as argv[2]) and the data it was built from, and fails if: the computed
// counts are missing, a beat line is missing, a tag pair is unbalanced, "undefined" or "NaN" leaked in,
// the viewport meta or data link is missing, a long passage looks quoted, or the scrubber and the order
// toggle do not run on a stub DOM.
'use strict';
const fs = require('fs');
const path = require('path');
const { model, down } = require('../lib/prestige.cjs');
const { esc } = require('../lib/render.cjs');

const file = process.argv[2] || path.resolve(__dirname, '..', '..', 'builds', 'nolan', 'the-prestige', 'index.html');
const html = fs.readFileSync(file, 'utf8');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'research', 'layers.json'), 'utf8'));
const m = model(data);
const fails = [];

const want = [`${m.n} beats`, `${m.shifts} changes of layer in this list`, `${m.inferred} of ${m.n} have a layer or story place that is a guess`, `${m.inPlace} of ${m.n} beats`];
for (const w of want) if (!html.includes(w)) fails.push(`missing from body: ${w}`);
for (const b of m.beats) if (!html.includes(esc(b.what))) fails.push(`beat missing: ${b.what}`);
for (const tag of ['main', 'section', 'ol', 'ul', 'li', 'svg', 'figure', 'script', 'article', 'label', 'output']) {
  const open = (html.match(new RegExp(`<${tag}[\\s>]`, 'g')) || []).length;
  const close = (html.match(new RegExp(`</${tag}>`, 'g')) || []).length;
  if (open !== close) fails.push(`unbalanced <${tag}>: ${open} open, ${close} close`);
}
if (/undefined|NaN|\[object/.test(html)) fails.push('undefined, NaN or [object leaked into the page');
if (!/<meta name="viewport"/.test(html)) fails.push('no viewport meta');
if (!/data\/the-prestige-layers\.json/.test(html)) fails.push('no link to the data');
const dots = (html.match(/<circle /g) || []).length;
const wantDots = m.n + 1 + m.n * 2;
if (dots !== wantDots) fails.push(`circles: ${dots} v ${wantDots}`);
const rows = (html.match(/class="seq"/g) || []).length;
if (rows !== m.n) fails.push(`list rows: ${rows} v ${m.n}`);

const script = (html.match(/<script>([\s\S]*?)<\/script>/) || [])[1];
if (!script) fails.push('no inline script');
else {
  const handlers = {};
  const node = extra => Object.assign({ textContent: '', attrs: {}, setAttribute(k, v) { this.attrs[k] = v; }, addEventListener(e, f) { handlers[(this.id || '') + e] = f; } }, extra);
  const els = { 'sc-n': node({ id: 'n', value: '1' }), 'sc-film': node(), 'sc-story': node(), 'sc-what': node(), 'sc-depth': node(), 'sc-where': node(), 'pf-cur': node() };
  const layers = m.layers.map(l => ({ dataset: { depth: String(l.depth) }, on: {}, classList: { toggle(c, v) { this.owner.on[c] = v; } } }));
  layers.forEach(l => { l.classList.owner = l; });
  const shuffled = [{ dataset: { screen: '2', story: '1' } }, { dataset: { screen: '1', story: '2' } }];
  const list = { children: shuffled.slice(), dataset: {}, appendChild(x) { this.children.splice(this.children.indexOf(x), 1); this.children.push(x); } };
  els.seqs = list;
  const btns = ['screen', 'story'].map(o => ({ dataset: { order: o }, pressed: null, setAttribute(k, v) { this.pressed = v; }, addEventListener(e, f) { this.click = f; } }));
  const document = {
    getElementById: id => els[id],
    querySelectorAll: q => (q === '.nest__l' ? layers : q === '.mem__toggle button' ? btns : []),
  };
  try {
    new Function('document', script)(document);
    for (const b of m.beats) {
      els['sc-n'].value = String(b.film);
      handlers.ninput();
      if (els['sc-what'].textContent !== b.what) fails.push(`scrub ${b.film}: wrong line`);
      if (els['sc-story'].textContent !== String(b.story)) fails.push(`scrub ${b.film}: story ${els['sc-story'].textContent} v ${b.story}`);
      if (els['sc-depth'].textContent !== down(b.depth)) fails.push(`scrub ${b.film}: depth word`);
      const on = layers.filter(l => l.on['is-on']).length;
      const wantOn = m.layers.filter(l => l.depth <= b.depth).length;
      if (on !== wantOn) fails.push(`scrub ${b.film}: ${on} layers open v ${wantOn}`);
    }
    btns[1].click();
    if (list.dataset.order !== 'story' || list.children[0].dataset.story !== '1') fails.push('toggle did not sort by story');
    if (btns[1].pressed !== 'true' || btns[0].pressed !== 'false') fails.push('toggle aria-pressed wrong');
  } catch (e) { fails.push('inline script threw: ' + e.message); }
}

const visible = html.replace(/<head>[\s\S]*?<\/head>/, '').replace(/<script>[\s\S]*?<\/script>/, '').replace(/<[^>]+>/g, ' ');
const longQuote = visible.match(/[“"][^“”"]{90,}[”"]/g) || [];
if (longQuote.length) fails.push(`possible long quote: ${longQuote[0].slice(0, 60)}`);

if (fails.length) { console.error('FAIL\n' + fails.map(f => ' - ' + f).join('\n')); process.exit(1); }
console.log(`OK ${path.basename(file)}: ${html.length} bytes, ${want.length} counts and ${m.n} beats found, scrubber walked all ${m.n} on a stub DOM, toggle sorted (${m.shifts} layer changes, deepest ${m.deepest}, ${m.sourced} sourced, ${m.inferred} inferred)`);
