#!/usr/bin/env node
// Check the career company page: recomputes handovers, the longest run and the repeat cast straight from
// films/*.json with its own name splitting (not through the page's model), checks the numbers and every
// handover film are in the body, one board row per person, tags balance, nothing undefined.
// Usage: node check.cjs <index.html>
'use strict';
const fs = require('fs');
const path = require('path');
const { model } = require('../lib/company.cjs');
const ROOT = path.join(__dirname, '..');
const reg = JSON.parse(fs.readFileSync(path.join(ROOT, 'films.json'), 'utf8'));
const html = fs.readFileSync(process.argv[2], 'utf8');
const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };
const split = v => (Array.isArray(v) ? v : [v]).flatMap(s => s.split('(')[0].split(', based on')[0].split(/ and |, /)).map(s => s.trim()).filter(Boolean);
const raw = reg.films.map(f => JSON.parse(fs.readFileSync(path.join(ROOT, 'films', f.slug + '.json'), 'utf8')))
  .sort((a, b) => a.year - b.year)
  .map(d => ({ title: d.title, camera: split(d.facts.dp.value), cut: split(d.facts.editor.value), score: split(d.facts.composer.value), cast: d.facts.cast_top5.value.map(x => x.name) }));
const m = model();
ok(m.n === raw.length, `films ${m.n} v ${raw.length}`);
let handovers = 0, longest = 0;
for (const k of ['camera', 'cut', 'score']) {
  const c = m.chairs.find(x => x.key === k);
  const mine = [];
  for (let i = 1; i < raw.length; i++) if (!raw[i][k].some(p => raw[i - 1][k].includes(p))) mine.push(i);
  ok(JSON.stringify(mine) === JSON.stringify(c.handovers), `${k} handovers ${mine} v ${c.handovers}`);
  handovers += mine.length;
  for (const p of new Set(raw.flatMap(r => r[k]))) {
    let run = 0;
    for (const r of raw) { run = r[k].includes(p) ? run + 1 : 0; longest = Math.max(longest, run); }
  }
  ok(new Set(raw.flatMap(r => r[k])).size === c.people.length, `${k} people count`);
}
ok(handovers === m.handoverTotal, `handover total ${handovers} v ${m.handoverTotal}`);
ok(longest === m.longest, `longest ${longest} v ${m.longest}`);
const castCount = {};
raw.forEach(r => r.cast.forEach(p => { castCount[p] = (castCount[p] || 0) + 1; }));
const repeat = Object.entries(castCount).filter(([, c]) => c >= 2);
ok(repeat.length === m.cast.people.length, `repeat cast ${repeat.length} v ${m.cast.people.length}`);
ok(Object.keys(castCount).length === m.cast.all, 'distinct cast');
const top = repeat.sort((a, b) => b[1] - a[1])[0];
ok(top[0] === m.castTop[0].name && top[1] === m.castTop[0].count, `top cast ${top} v ${m.castTop[0].name}`);
const body = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
for (const s of ['The company.', `${m.longest} films in a row`, `${m.handoverTotal} handovers`, `billed in the top five ${top[1]} times`, `${m.cast.people.length} of ${m.cast.all}`, `${m.cn.count} of ${m.n}`]) ok(body.includes(s), `missing in body: ${s}`);
for (const c of m.chairs) for (const i of c.handovers) ok(body.includes(`to ${raw[i].title}`), `handover film missing: ${raw[i].title}`);
ok(!/undefined|NaN|\[object|Infinity/.test(html), 'undefined, NaN or Infinity in html');
ok(!/—/.test(html), 'em dash in html');
for (const t of ['section', 'ol', 'li', 'ul', 'main', 'p', 'table', 'tr', 'td', 'th', 'span', 'a', 'b']) {
  const open = (html.match(new RegExp(`<${t}[\\s>]`, 'g')) || []).length;
  const close = (html.match(new RegExp(`</${t}>`, 'g')) || []).length;
  ok(open === close, `<${t}> ${open} open, ${close} closed`);
}
const people = m.chairs.reduce((t, c) => t + c.people.length, 0) + m.writing.people.length + m.cast.people.length;
ok((html.match(/class="cp-row[ "]/g) || []).length === people + 5, `board rows != people (${people}) + 5 heads`);
ok((html.match(/class="cp-row cp-row--head"/g) || []).length === 5, 'five boards');
ok((html.match(/class="cp-cell[ "]/g) || []).length === people * m.n, 'cells != people x films');
ok((html.match(/class="cp-tr"/g) || []).length === m.n, 'table rows != films');
if (fails.length) { console.log('FAIL\n- ' + fails.join('\n- ')); process.exit(1); }
console.log(`PASS ${m.n} films, ${people} board rows, ${handovers} handovers, longest run ${longest}, repeat cast ${repeat.length} of ${m.cast.all}, top ${top[0]} ${top[1]}, ${html.length} bytes`);
