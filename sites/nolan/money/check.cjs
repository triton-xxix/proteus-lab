#!/usr/bin/env node
// Check the career money page: recomputes every multiple straight from films/*.json (not through the
// page's model), checks the headline numbers are in the body, one chart row and one table row per film,
// tags balance, nothing undefined. Usage: node check.cjs <index.html>
'use strict';
const fs = require('fs');
const path = require('path');
const { model, times, money } = require('../lib/money.cjs');
const ROOT = path.join(__dirname, '..');
const reg = JSON.parse(fs.readFileSync(path.join(ROOT, 'films.json'), 'utf8'));
const html = fs.readFileSync(process.argv[2], 'utf8');
const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };
const raw = reg.films.map(f => {
  const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'films', f.slug + '.json'), 'utf8'));
  return { slug: f.slug, x: d.facts.gross_usd.value / d.facts.budget_usd.value, rt: d.facts.runtime_min.value };
});
const m = model();
ok(m.n === reg.films.length, `films ${m.n} v register ${reg.films.length}`);
const best = raw.reduce((a, b) => (b.x > a.x ? b : a)), worst = raw.reduce((a, b) => (b.x < a.x ? b : a));
ok(best.slug === m.best.slug && worst.slug === m.worst.slug, `best/worst ${best.slug}/${worst.slug} v ${m.best.slug}/${m.worst.slug}`);
for (const r of raw) ok(Math.abs(m.rows.find(x => x.slug === r.slug).multiple - r.x) < 1e-9, `multiple differs: ${r.slug}`);
ok(m.totalMinutes === raw.reduce((t, r) => t + r.rt, 0), 'total minutes');
const body = html.replace(/<[^>]+>/g, ' ');
for (const s of ['The money and the minutes', times(m.best.multiple), times(m.worst.multiple), times(m.medianMultiple), money(m.totalGross), m.totalMinutes.toLocaleString('en-GB'), `${m.shortest.runtime} minutes to ${m.longest.runtime}`]) ok(body.includes(s), `missing in body: ${s}`);
for (const r of m.rows) ok(body.includes(times(r.multiple)), `row multiple missing: ${r.slug}`);
ok(!/undefined|NaN|\[object|Infinity/.test(html), 'undefined, NaN or Infinity in html');
for (const t of ['section', 'ol', 'li', 'ul', 'figure', 'main', 'p', 'table', 'tr', 'td', 'th', 'span']) {
  const open = (html.match(new RegExp(`<${t}[\\s>]`, 'g')) || []).length;
  const close = (html.match(new RegExp(`</${t}>`, 'g')) || []).length;
  ok(open === close, `<${t}> ${open} open, ${close} closed`);
}
ok((html.match(/class="mn-row[ "]/g) || []).length === m.n + 1, 'money chart rows != films + axis');
ok((html.match(/class="mn-dot mn-dot--g"/g) || []).length === m.n, 'gross dots != films');
ok((html.match(/class="rt-row"/g) || []).length === m.n, 'runtime rows != films');
ok((html.match(/class="mn-tr"/g) || []).length === m.n, 'table rows != films');
const lefts = [...html.matchAll(/left:(-?[\d.]+)%/g)].map(x => +x[1]);
ok(lefts.every(v => v >= 0 && v <= 100), 'a dot or tick sits off the axis');
if (fails.length) { console.log('FAIL\n- ' + fails.join('\n- ')); process.exit(1); }
console.log(`PASS ${m.n} films, best ${m.best.slug} ${times(m.best.multiple)}, worst ${m.worst.slug} ${times(m.worst.multiple)}, median ${times(m.medianMultiple)}, ${m.totalMinutes} min, ${html.length} bytes`);
