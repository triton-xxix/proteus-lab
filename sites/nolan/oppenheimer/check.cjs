#!/usr/bin/env node
// Check the Oppenheimer deep page: every quote in calendar.json is in the fetched Wikipedia plot, every
// stated year appears in its own quote, the headline numbers are in the body, tags balance, nothing
// undefined. Usage: node check.cjs <index.html> [--live]
'use strict';
const fs = require('fs');
const path = require('path');
const { model } = require('../lib/oppenheimer.cjs');
const R = path.join(__dirname, 'research');
const r = JSON.parse(fs.readFileSync(path.join(R, 'calendar.json'), 'utf8'));
const wiki = JSON.parse(fs.readFileSync(path.join(R, 'wikipedia-2026-11-14.json'), 'utf8'));
const text = Object.values(wiki.query.pages)[0].extract.replace(/[‘’]/g, "'");
const html = fs.readFileSync(process.argv[2], 'utf8');
const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };
for (const e of r.events.concat(r.lookbacks)) {
  ok(text.includes(e.quote.replace(/[‘’]/g, "'")), `quote not in the fetched plot: ${e.id}`);
  if (typeof e.from === 'number') ok(e.quote.includes(String(e.from)), `year ${e.from} not in its own quote: ${e.id}`);
}
const m = model(r);
ok(m.span === 33 && m.hearingGap === 5, `span ${m.span} gap ${m.hearingGap}`);
ok(m.looks[0].years === 12 && m.looks[1].years === 16, `lookbacks ${m.looks.map(l => l.years)}`);
const body = html.replace(/<[^>]+>/g, ' ');
for (const s of ['Everything goes back to 1947', '33', 'years between the two hearings', '12', '16', '1930 to 1963']) ok(body.includes(s), `missing in body: ${s}`);
ok(!/undefined|NaN|\[object/.test(html), 'undefined or NaN in html');
for (const t of ['svg', 'section', 'ol', 'li', 'ul', 'figure', 'main', 'p']) {
  const open = (html.match(new RegExp(`<${t}[\\s>]`, 'g')) || []).length;
  const close = (html.match(new RegExp(`</${t}>`, 'g')) || []).length;
  ok(open === close, `<${t}> ${open} open, ${close} closed`);
}
ok((html.match(/class="op-cal__ev"/g) || []).length === m.dated.length, 'event marks != dated events');
ok((html.match(/class="op-ev[ "]/g) || []).length === r.events.length, 'list rows != events');
ok((html.match(/op-cal__arc--/g) || []).length === 2, 'two arcs');
if (fails.length) { console.log('FAIL\n- ' + fails.join('\n- ')); process.exit(1); }
console.log(`PASS ${r.events.length} events, ${m.dated.length} dated, span ${m.span}, gap ${m.hearingGap}, lookbacks ${m.looks.map(l => l.years).join(' and ')}, ${html.length} bytes`);
