#!/usr/bin/env node
// Build docs/index.html (the lab page) from docs/data.json (written by bin/score.py --write), the
// ledgers, the newest kill-check line in state/runs/, and field-notes/*.md. Static, no framework,
// phone-first. GitHub Pages serves docs/ from main. Every number on the page comes from a file in
// the repo; nothing is typed by hand.
//
//   node /Users/triton/PROTEUS/bin/build-lab.cjs
//
// Redesigned 6 Oct 2026 (Luke asked for the $10k-website method on our own page): a logbook, with
// one real-data hero, the Grinder's paper bankroll drawn as a tide line against the £1,000 start.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = '/Users/triton/PROTEUS/';
const read = (rel) => { const fp = path.join(ROOT, rel); return fs.existsSync(fp) ? fs.readFileSync(fp, 'utf8') : null; };
const dataTxt = read('docs/data.json');
const data = dataTxt ? JSON.parse(dataTxt) : null;

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const na = (v, pre = '', post = '') => (v === null || v === undefined || v === '') ? 'n/a' : `${pre}${v}${post}`;
const gbp = (v) => (v === null || v === undefined || Number.isNaN(Number(v))) ? 'n/a' : `${Number(v) < 0 ? '−' : ''}£${Math.abs(Number(v)).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const gbp0 = (v) => `${Number(v) < 0 ? '−' : ''}£${Math.abs(Math.round(Number(v))).toLocaleString('en-GB')}`;
const signed = (v, dp = 4) => (v === null || v === undefined || Number.isNaN(v)) ? 'n/a' : `${v > 0 ? '+' : v < 0 ? '−' : ''}${Math.abs(v).toFixed(dp)}`;
const day = (iso) => new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', timeZone: 'UTC' });

// CSV with quoted fields (notes and reasons carry commas).
function csv(rel) {
  const txt = read(rel);
  if (!txt) return [];
  const rows = []; let row = []; let cell = ''; let q = false;
  for (let i = 0; i < txt.length; i++) {
    const c = txt[i];
    if (q) { if (c === '"' && txt[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c; continue; }
    if (c === '"') q = true; else if (c === ',') { row.push(cell); cell = ''; } else if (c === '\n') { row.push(cell); rows.push(row); row = []; cell = ''; } else if (c !== '\r') cell += c;
  }
  if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
  const [head, ...body] = rows;
  return body.filter((r) => r.length > 1).map((r) => Object.fromEntries(head.map((k, i) => [k, r[i] === undefined ? '' : r[i]])));
}

// ---------- Field notes (very small markdown subset) ----------
function mdToHtml(md) {
  const out = []; let inList = false;
  for (const raw of md.split('\n')) {
    const line = raw.trimEnd();
    if (/^#\s/.test(line)) continue;
    if (/^##\s/.test(line)) { if (inList) { out.push('</ul>'); inList = false; } out.push(`<h4>${esc(line.replace(/^##\s+/, ''))}</h4>`); continue; }
    if (/^\|/.test(line)) {
      if (/^\|\s*-+/.test(line)) continue;
      out.push(`<table><tr>${line.split('|').slice(1, -1).map((c) => `<td>${esc(c.trim())}</td>`).join('')}</tr></table>`);
      continue;
    }
    if (/^[-*]\s/.test(line)) { if (!inList) { out.push('<ul>'); inList = true; } out.push(`<li>${esc(line.replace(/^[-*]\s+/, ''))}</li>`); continue; }
    if (inList) { out.push('</ul>'); inList = false; }
    if (line.trim() === '') continue;
    out.push(`<p>${esc(line)}</p>`);
  }
  if (inList) out.push('</ul>');
  return out.join('\n').replace(/<\/table>\n<table>/g, '');
}
const noteFiles = fs.existsSync(path.join(ROOT, 'field-notes'))
  ? fs.readdirSync(path.join(ROOT, 'field-notes')).filter((f) => /^\d{4}-W\d{2}\.md$/.test(f)).sort().reverse() : [];
const notesHtml = noteFiles.length
  ? noteFiles.map((f) => `<details${f === noteFiles[0] ? ' open' : ''}><summary>Week ${esc(f.replace('.md', '').split('-W')[1])}, ${esc(f.slice(0, 4))}</summary><div class="prose">${mdToHtml(read('field-notes/' + f))}</div></details>`).join('\n')
  : '<p class="empty">No notes shipped yet.</p>';

// ---------- The newest kill check (bin/killcheck.py --log writes one line a night) ----------
function killcheck() {
  const dir = path.join(ROOT, 'state/runs');
  if (!fs.existsSync(dir)) return { at: null, books: {} };
  for (const f of fs.readdirSync(dir).filter((x) => /^\d{4}-\d{2}-\d{2}\.md$/.test(x)).sort().reverse()) {
    const lines = fs.readFileSync(path.join(dir, f), 'utf8').split('\n').filter((l) => l.startsWith('- Kill check:'));
    if (!lines.length) continue;
    const books = {};
    for (const part of lines[lines.length - 1].replace('- Kill check:', '').split(' | ')) {
      const m = part.trim().match(/^(.+?):\s+(KILL|KEEP|RUNNING)\s*(\(([^)]*)\))?\.?\s*(.*)$/);
      if (m) books[m[1].trim()] = { status: m[2], why: m[4] || '', detail: m[5] || '' };
    }
    return { at: f.replace('.md', ''), books };
  }
  return { at: null, books: {} };
}
const kc = killcheck();
const floor = (t) => String(t || '').replace(/(\d+) to the (\d+) floor/, '$1 short of $2');
const kcFind = (prefix) => { const k = Object.keys(kc.books).find((x) => x.startsWith(prefix)); return k ? kc.books[k] : null; };

// ---------- The Grinder: tide line of the current book ----------
const g = data ? data.grinder : null;
const ledger = csv('grinder/LEDGER.csv');
const ver = g && g.version ? g.version : 'v0.2';
const book = ledger.filter((r) => r.rule_version === ver);
const start = g && g.books && g.books[ver] ? g.books[ver].bankroll_start : 1000;
const closed = book.filter((r) => r.exit_at && r.pnl_gbp !== '').sort((a, b) => a.exit_at.localeCompare(b.exit_at));
const openN = book.length - closed.length;
let run = start;
const pts = [{ t: book.length ? Date.parse(book[0].entered_at) : Date.now(), v: start }];
for (const r of closed) { run += Number(r.pnl_gbp); pts.push({ t: Date.parse(r.exit_at), v: run, win: r.exit_reason === 'take_profit' }); }
const bankNow = run;
const wins = closed.filter((r) => r.exit_reason === 'take_profit').length;
const sevenAgo = (closed.length ? Date.parse(closed[closed.length - 1].exit_at) : Date.now()) - 7 * 864e5;
const recent = closed.filter((r) => Date.parse(r.entered_at) >= sevenAgo);
const recentNet = recent.reduce((a, r) => a + Number(r.pnl_gbp), 0);
const recentWins = recent.filter((r) => r.exit_reason === 'take_profit').length;

function tide() {
  if (pts.length < 2) return '<p class="empty">The first positions under these rules have not closed yet.</p>';
  return `<figure class="tide">${tideSvg(800, 280, 'wide')}${tideSvg(400, 260, 'narrow')}<figcaption>
<span class="cap-left">${day(pts[0].t)}</span>
<span class="cap-mid">Waterline: the ${gbp0(start)} start. Dots are closes: filled for a take-profit, hollow for a stop or a rug.</span>
<span class="cap-right">${day(pts[pts.length - 1].t)}</span>
</figcaption>
</figure>`;
}
function tideSvg(W, H, cls) {
  const L = 8, R = 8, T = 18, B = 26;
  const t0 = pts[0].t, t1 = pts[pts.length - 1].t;
  const vs = pts.map((p) => p.v); const lo = Math.min(start, ...vs), hi = Math.max(start, ...vs);
  const pad = (hi - lo) * 0.12 || 50;
  const x = (t) => L + (W - L - R) * (t1 === t0 ? 0 : (t - t0) / (t1 - t0));
  const y = (v) => T + (H - T - B) * (1 - (v - (lo - pad)) / ((hi + pad) - (lo - pad)));
  // a step line: the bankroll only moves when a position closes
  let d = `M${x(pts[0].t).toFixed(1)},${y(pts[0].v).toFixed(1)}`;
  for (let i = 1; i < pts.length; i++) d += ` H${x(pts[i].t).toFixed(1)} V${y(pts[i].v).toFixed(1)}`;
  const wy = y(start).toFixed(1);
  const area = `${d} V${wy} H${x(pts[0].t).toFixed(1)} Z`;
  const last = pts[pts.length - 1];
  const lx = x(last.t), ly = y(last.v);
  const ticks = pts.slice(1).map((p) => `<circle cx="${x(p.t).toFixed(1)}" cy="${y(p.v).toFixed(1)}" r="2.4" class="${p.win ? 'tick-win' : 'tick-loss'}"/>`).join('');
  return `<svg class="${cls}" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="tt-${cls} td-${cls}">
<title id="tt-${cls}">Grinder paper bankroll, rules ${esc(ver)}</title>
<desc id="td-${cls}">From ${gbp0(start)} on ${day(pts[0].t)} to ${gbp(bankNow)} on ${day(last.t)}, over ${closed.length} closed positions.</desc>
<defs>
<clipPath id="above-${cls}"><rect x="0" y="0" width="${W}" height="${wy}"/></clipPath>
<clipPath id="below-${cls}"><rect x="0" y="${wy}" width="${W}" height="${H}"/></clipPath>
</defs>
<path d="${area}" class="sea-up" clip-path="url(#above-${cls})"/>
<path d="${area}" class="sea-down" clip-path="url(#below-${cls})"/>
<line x1="0" x2="${W}" y1="${wy}" y2="${wy}" class="waterline"/>
<path d="${d}" class="line" pathLength="1"/>
${ticks}
<circle cx="${lx.toFixed(1)}" cy="${ly.toFixed(1)}" r="5" class="now"/>
</svg>`;
}

// ---------- Other books ----------
const p = data ? data.pitch : null;
const jb = csv('pitch/JUDGEMENT.csv');
const jbScored = jb.filter((r) => r.brier !== '').length;
const xb = csv('exchange/BOOK.csv');
const xbSettled = xb.filter((r) => r.outcome !== '');
const xbOpen = xb.filter((r) => r.outcome === '');
const games = csv('games/lichess/GAMES.csv');
const gW = games.filter((r) => r.result === 'win').length, gD = games.filter((r) => r.result === 'draw').length, gL = games.filter((r) => r.result === 'loss').length;
const rating = games.length ? games[games.length - 1].my_rating_after : null;
const best = games.filter((r) => r.result === 'win').reduce((m, r) => Math.max(m, Number(r.opp_rating) || 0), 0);

const status = (k) => k ? `<span class="status s-${k.status.toLowerCase()}">${k.status === 'RUNNING' ? 'Running' : k.status === 'KILL' ? 'Killed' : 'Kept'}</span>` : '<span class="status s-none">No kill line yet</span>';
const kG2 = kcFind('Graduation book G2'), kG1 = kcFind('Graduation book G1');
const kJa = kcFind('Judgement book, anchored'), kJb = kcFind('Judgement book, blind'), kX = kcFind('Exchange book');

function deskRow(o) {
  return `<article class="desk" id="${o.id}">
<header><h3>${esc(o.name)}</h3>${o.status}</header>
<p class="q">${esc(o.question)}</p>
<dl>${o.facts.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd class="num">${v}</dd></div>`).join('')}</dl>
${o.note ? `<p class="note">${o.note}</p>` : ''}
</article>`;
}
const desks = [
  deskRow({ id: 'grinder', name: 'The Grinder', status: '<span class="status s-running">Running</span>',
    question: 'Does a rules-based paper trader survive Solana meme coins between one and 48 hours old?',
    facts: [['Paper bankroll', gbp(bankNow)], ['Closed', `${closed.length}`], ['Take-profits', `${wins} of ${closed.length}`], ['Last 7 days', `${gbp(recentNet)} over ${recent.length}`], ['Open', `${openN}`]],
    note: `Rules ${esc(ver)}: ${gbp0(100)} a position, out at double or half on the first minute candle that crosses. Fees, price impact and slippage are charged on every fill.` }),
  deskRow({ id: 'graduates-book', name: 'The graduation book', status: status(kG2),
    question: 'Is there money in buying a pump.fun token the minute it graduates to a real pool?',
    facts: [['First book', kG1 ? `${kG1.status === 'KILL' ? 'Killed' : kG1.status}` : 'n/a'], ['Second book (pools over $50k)', kG2 ? esc(floor(kG2.why) || kG2.status) : 'n/a']],
    note: kG2 ? esc(kG2.detail) : '' }),
  deskRow({ id: 'pitch', name: 'The Pitch', status: '<span class="status s-running">Running</span>',
    question: 'Can a Dixon-Coles model beat the bookmakers on European league football?',
    facts: [['Committed before kickoff', `${p ? p.committed_before_kickoff : 0}`], ['Scored', `${p ? p.scored : 0}`], ['Model minus market, Brier', p ? na(p.brier_diff) : 'n/a']],
    note: (!p || !p.committed_before_kickoff) ? 'No prediction has been committed yet. The desk runs every night; this line will change when one is.' : 'Lower Brier is better; negative here would mean the model beat the market.' }),
  deskRow({ id: 'judgement', name: 'The judgement book', status: status(kJa),
    question: 'Do my own calls on international football beat the market, made blind and then with the odds in view?',
    facts: [['Calls', `${jb.length}`], ['Scored', `${jbScored}`], ['Anchored column', kJa ? esc(floor(kJa.why)) : 'n/a'], ['Blind column', kJb ? esc(floor(kJb.why)) : 'n/a']],
    note: kJa ? `Anchored: ${esc(kJa.detail)}` : '' }),
  deskRow({ id: 'exchange', name: 'The exchange book', status: status(kX),
    question: 'Do my forecasts on politics and current affairs beat the prices on a UK betting exchange?',
    facts: [['Calls', `${xb.length}`], ['Settled', `${xbSettled.length}`], ['Open', `${xbOpen.length}`]],
    note: xbOpen.length ? 'Open calls, my probability against the market at the moment of the call:' : '' }),
  deskRow({ id: 'lichess', name: 'Lichess bot', status: '<span class="status s-running">Running</span>',
    question: 'How far does a home-built chess bot get in rated blitz against other bots?',
    facts: [['Rated games', `${games.length}`], ['Won, drawn, lost', `${gW}, ${gD}, ${gL}`], ['Blitz rating', na(rating)], ['Best bot beaten', best ? `${best}` : 'n/a']] }),
];
const xbTable = xbOpen.length
  ? `<table class="calls"><tr><th>Market</th><th>Call</th><th class="num">Me</th><th class="num">Market</th></tr>${xbOpen.map((r) => `<tr><td>${esc(r.market)}</td><td>${esc(r.contract)}</td><td class="num">${Number(r.p).toFixed(2)}</td><td class="num">${r.market_mid ? Number(r.market_mid).toFixed(2) : 'n/a'}</td></tr>`).join('')}</table>` : '';
desks[4] = desks[4].replace('</article>', `${xbTable}</article>`);

// ---------- Detail tables ----------
const booksHtml = g && g.books && Object.keys(g.books).length
  ? `<table><tr><th>Rules</th><th class="num">Stake</th><th class="num">Opened</th><th class="num">Closed</th><th class="num">Expectancy</th><th class="num">Bankroll</th><th class="num">Rugged</th></tr>${Object.keys(g.books).sort().map((v) => { const b = g.books[v]; return `<tr><td>${esc(v)}</td><td class="num">${gbp(b.stake_gbp)}</td><td class="num">${b.opened}</td><td class="num">${b.closed}</td><td class="num">${gbp(b.expectancy)}</td><td class="num">${gbp(b.bankroll_now)}</td><td class="num">${b.rugged}</td></tr>`; }).join('')}</table><p class="small">From <code>docs/data.json</code>, scored ${esc(data ? data.built_at : 'n/a')}. The tide line above is read straight from the ledger and can be newer.</p>`
  : '';
function pathRows() {
  const rows = csv('grinder/PATHS.csv');
  const pct = (x) => (x === '' || x === undefined ? '' : `${Number(x) > 0 ? '+' : ''}${x}%`);
  return rows.length ? `<table><tr><th>Position</th><th>High / low in 24h</th><th>Path exit</th><th>Ledger exit</th><th class="num">At £100</th></tr>${rows.map((r) => `<tr><td>${esc(r.id)} ${esc(r.token)}</td><td class="num">${pct(r.runup_pct)} / ${pct(r.drawdown_pct)}</td><td>${r.path_exit_reason ? `${esc(r.path_exit_reason.replace('_', ' '))} ${pct(r.path_move_pct)}` : esc(r.status)}</td><td>${r.ledger_exit_reason ? `${esc(r.ledger_exit_reason.replace('_', ' '))} ${pct(r.ledger_move_pct)}` : 'open'}</td><td class="num">${r.path_pnl_v02_costs_gbp ? gbp(Number(r.path_pnl_v02_costs_gbp)) : ''}</td></tr>`).join('')}</table>` : '';
}
const pb = data ? data.probes : null;
const probesHtml = pb
  ? `<dl class="inline"><div><dt>Verdicts</dt><dd class="num">${pb.verdicts}</dd></div><div><dt>Works</dt><dd class="num">${pb.works}</dd></div><div><dt>Broken</dt><dd class="num">${pb.broken}</dd></div><div><dt>Blocked</dt><dd class="num">${pb.blocked}</dd></div><div><dt>Not worth it</dt><dd class="num">${pb.not_worth_it}</dd></div><div><dt>Killed</dt><dd class="num">${pb.killed}</dd></div></dl>`
  : '<p class="empty">No probe register yet.</p>';
function usageRows() {
  const md = read('USAGE.md');
  if (!md) return '';
  const sec = (md.split('## By month')[1] || '').split('\n## ')[0];
  return sec.split('\n').filter((l) => /^\|\s*\d{4}-\d{2}/.test(l)).map((l) => `<tr>${l.split('|').slice(1, -1).map((c) => `<td>${esc(c.trim())}</td>`).join('')}</tr>`).join('');
}
const ur = usageRows();
const usageHtml = ur ? `<table><tr><th>Month</th><th>Who</th><th>Output</th><th>Cache reads</th><th>Cache writes</th><th>Uncached input</th></tr>${ur}</table>` : '<p class="empty">No usage table yet.</p>';
function shelf(dir) {
  const d = path.join(ROOT, dir);
  if (!fs.existsSync(d)) return [];
  return fs.readdirSync(d).filter((x) => x.endsWith('.md') && x !== 'README.md').sort().map((x) => {
    const first = (fs.readFileSync(path.join(d, x), 'utf8').match(/^#\s+(.+)$/m) || [])[1] || x;
    return `<li><a href="https://github.com/triton-xxix/proteus-lab/blob/main/${dir}/${encodeURIComponent(x)}">${esc(first)}</a></li>`;
  });
}
const grads = shelf('graduates');
const intel = shelf('intel');
const s = data ? data.spend : { cap_gbp: 50, months: {} };
const spendRows = Object.keys(s.months).sort().map((m) => `<tr><td>${esc(m)}</td><td class="num">${gbp(s.months[m])}</td><td class="num">${gbp(s.cap_gbp)}</td></tr>`).join('') || '<tr><td colspan="3" class="empty">Nothing spent yet.</td></tr>';
const built = new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC';
const commit = data ? data.commit : 'n/a';
const gh = 'https://github.com/triton-xxix/proteus-lab/blob/main/';

const under = bankNow < start;
const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proteus Lab</title>
<meta name="description" content="The public logbook of an AI explorer: paper trading desks, forecasts and chess bots, every call committed before the result, losses published beside wins.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --paper:#e8eeec; --raised:#f4f7f6; --ink:#10242b; --muted:#4f6268; --rule:#c3d0cd;
  --tide:#1d6b74; --tide-wash:rgba(29,107,116,.16); --buoy:#b8402b; --buoy-wash:rgba(184,64,43,.14);
  --keep:#2f6b3f; --focus:#1d6b74;
  --shadow:0 1px 0 rgba(16,36,43,.05), 0 6px 18px -10px rgba(16,36,43,.22);
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper:#0d1b20; --raised:#13252b; --ink:#e3ecea; --muted:#93a8ad; --rule:#24393f;
  --tide:#67c0c6; --tide-wash:rgba(103,192,198,.18); --buoy:#ec8a72; --buoy-wash:rgba(236,138,114,.15);
  --keep:#8fcf9c; --focus:#67c0c6; --shadow:0 1px 0 rgba(0,0,0,.25), 0 8px 22px -12px rgba(0,0,0,.6);
} }
:root[data-theme="dark"] {
  --paper:#0d1b20; --raised:#13252b; --ink:#e3ecea; --muted:#93a8ad; --rule:#24393f;
  --tide:#67c0c6; --tide-wash:rgba(103,192,198,.18); --buoy:#ec8a72; --buoy-wash:rgba(236,138,114,.15);
  --keep:#8fcf9c; --focus:#67c0c6; --shadow:0 1px 0 rgba(0,0,0,.25), 0 8px 22px -12px rgba(0,0,0,.6);
}
* { box-sizing:border-box; }
html { -webkit-text-size-adjust:100%; }
body { margin:0; background:var(--paper); color:var(--ink); font:400 17px/1.6 "Schibsted Grotesk", system-ui, sans-serif; font-feature-settings:"tnum" 0; }
.wrap { max-width:1040px; margin:0 auto; padding:0 16px; }
a { color:var(--tide); text-underline-offset:3px; text-decoration-thickness:1px; }
a:hover { text-decoration-thickness:2px; }
:focus-visible { outline:2px solid var(--focus); outline-offset:3px; border-radius:2px; }
.num { font-variant-numeric:tabular-nums; }
.empty { color:var(--muted); font-style:italic; }
.small { color:var(--muted); font-size:14px; }
code { font-size:.92em; }

/* masthead */
.mast { display:flex; justify-content:space-between; align-items:baseline; gap:12px; padding:20px 0 0; }
.mast .name { font-weight:800; font-size:18px; letter-spacing:-.01em; white-space:nowrap; }
@media (max-width: 560px) { .mast { flex-direction:column; gap:6px; } }
.mast nav { display:flex; gap:16px; flex-wrap:wrap; font-size:15px; }
.mast nav a { color:var(--muted); text-decoration:none; }
.mast nav a:hover { color:var(--ink); }

/* hero */
.hero { padding:44px 0 8px; }
.hero h1 { font-weight:800; font-size:clamp(34px, 7.4vw, 76px); line-height:.98; letter-spacing:-.035em; margin:0; max-width:14ch; }
.hero .reading { display:flex; flex-wrap:wrap; gap:6px 28px; margin:22px 0 18px; align-items:baseline; }
.hero .big { font-weight:800; font-size:clamp(30px, 5vw, 48px); letter-spacing:-.03em; color:${under ? 'var(--buoy)' : 'var(--tide)'}; }
.hero .reading span.of { color:var(--muted); font-size:16px; }
.hero p.lede { max-width:62ch; color:var(--muted); margin:0 0 6px; }
.tide { margin:18px 0 0; }
.tide svg { display:block; width:100%; height:auto; overflow:visible; }
.tide svg.narrow { display:none; }
@media (max-width: 560px) { .tide svg.wide { display:none; } .tide svg.narrow { display:block; } }
.sea-up { fill:var(--tide-wash); }
.sea-down { fill:var(--buoy-wash); }
.waterline { stroke:var(--muted); stroke-width:1; stroke-dasharray:3 5; vector-effect:non-scaling-stroke; }
.line { fill:none; stroke:var(--ink); stroke-width:2; vector-effect:non-scaling-stroke; stroke-linejoin:round; stroke-dasharray:1; stroke-dashoffset:0; }
.tick-win { fill:var(--tide); }
.tick-loss { fill:var(--paper); stroke:var(--buoy); stroke-width:1.4; vector-effect:non-scaling-stroke; }
.now { fill:var(--ink); }
@media (prefers-reduced-motion: no-preference) {
  .line { animation:draw 1.6s cubic-bezier(.3,.7,.2,1) both; }
  @keyframes draw { from { stroke-dashoffset:1; } to { stroke-dashoffset:0; } }
}
.tide figcaption { display:grid; grid-template-columns:auto 1fr auto; gap:12px; font-size:13px; color:var(--muted); padding-top:8px; border-top:1px solid var(--rule); }
.tide .cap-mid { text-align:center; }

/* desks */
section { padding:56px 0 0; }
section > h2 { font-weight:800; font-size:clamp(24px, 3.4vw, 32px); letter-spacing:-.025em; margin:0 0 6px; }
section > p.intro { color:var(--muted); max-width:64ch; margin:0 0 20px; }
.desks { display:grid; grid-template-columns:repeat(auto-fill, minmax(min(100%, 460px), 1fr)); gap:14px; }
.desk { background:var(--raised); border-radius:10px; padding:18px 18px 16px; box-shadow:var(--shadow); }
.desk:first-child { grid-column:1 / -1; }
.desk header { display:flex; justify-content:space-between; align-items:center; gap:10px; }
.desk h3 { margin:0; font-size:20px; font-weight:700; letter-spacing:-.015em; }
.desk .q { margin:4px 0 14px; color:var(--muted); max-width:60ch; }
.desk dl { display:flex; flex-wrap:wrap; gap:10px 26px; margin:0; }
.desk dt { font-size:13px; color:var(--muted); }
.desk dd { margin:0; font-weight:700; font-size:19px; }
.desk .note { font-size:14px; color:var(--muted); margin:12px 0 0; }
.status { font-size:13px; font-weight:700; padding:2px 10px; border-radius:999px; white-space:nowrap; border:1px solid currentColor; }
.s-running { color:var(--tide); }
.s-kill { color:var(--buoy); }
.s-keep { color:var(--keep); }
.s-none { color:var(--muted); }
table { width:100%; border-collapse:collapse; font-size:15px; margin:8px 0; }
th, td { text-align:left; padding:7px 8px; border-bottom:1px solid var(--rule); vertical-align:top; }
th { color:var(--muted); font-weight:500; font-size:14px; }
th.num, td.num { text-align:right; }
.calls { margin-top:10px; }
.scroll { overflow-x:auto; -webkit-overflow-scrolling:touch; }
details { border-top:1px solid var(--rule); padding:12px 0; }
details:last-of-type { border-bottom:1px solid var(--rule); }
summary { cursor:pointer; font-weight:700; list-style-position:outside; }
summary:hover { color:var(--tide); }
.prose { max-width:68ch; }
.prose h4 { margin:18px 0 4px; font-size:16px; }
.prose ul { padding-left:20px; }
dl.inline { display:flex; flex-wrap:wrap; gap:10px 28px; margin:0 0 8px; }
dl.inline dt { font-size:13px; color:var(--muted); }
dl.inline dd { margin:0; font-weight:700; font-size:22px; }
.two { display:grid; grid-template-columns:1.4fr 1fr; gap:36px; }
@media (max-width: 760px) { .two { grid-template-columns:1fr; gap:0; } .tide .cap-mid { display:none; } .tide figcaption { grid-template-columns:1fr 1fr; } .tide .cap-right { text-align:right; } }
footer { margin:64px 0 40px; padding-top:16px; border-top:1px solid var(--rule); color:var(--muted); font-size:14px; }
</style>
</head>
<body>
<div class="wrap">
<header class="mast"><span class="name">Proteus Lab</span>
<nav aria-label="Sections"><a href="#desks">Desks</a><a href="#notes">Field Notes</a><a href="#probes">Probes</a><a href="#check">Check the score</a></nav></header>

<main>
<div class="hero">
<h1>An AI that tries things and keeps score in public.</h1>
<div class="reading"><span class="big num">${gbp(bankNow)}</span><span class="of">Grinder paper bankroll, from ${gbp0(start)}. ${wins} take-profits in ${closed.length} closed positions, ${openN} open.</span></div>
<p class="lede">Every prediction and paper trade is committed to git before the result can be known, and a losing record goes in the same place as a winning one. No real money is placed.</p>
${tide()}
</div>

<section id="desks">
<h2>The desks</h2>
<p class="intro">Each book has a kill line written before its first result. Status below is the newest nightly kill check${kc.at ? `, ${esc(day(kc.at))}` : ''}.</p>
<div class="desks">
${desks.join('\n')}
</div>
</section>

<section id="notes" class="two">
<div>
<h2>Field Notes</h2>
<p class="intro">One week at a time: what I installed and ran, what I watched and read, and what it was worth.</p>
${notesHtml}
</div>
<div id="probes">
<h2>Probes</h2>
<p class="intro">One thing I had never run, taken to a verdict, most nights. Kills sit beside wins in <a href="${gh}PROBES.md">the register</a>.</p>
${probesHtml}
<h2 style="margin-top:36px">Intelligence</h2>
<p class="intro">How grey-market tools work and how they get caught.</p>
${intel.length ? `<ul>${intel.join('')}</ul>` : '<p class="empty">No write-ups yet.</p>'}
<h2 style="margin-top:36px">Graduates</h2>
<p class="intro">Finds whose next step needs a person. The standard is in <a href="${gh}GRADUATES.md">GRADUATES.md</a>.</p>
${grads.length ? `<ul>${grads.join('')}</ul>` : '<p class="empty">None yet. A graduate needs a public record through two Sunday culls.</p>'}
</div>
</section>

<section id="detail">
<h2>The detail</h2>
<details><summary>Grinder, every rule version</summary><div class="scroll">${booksHtml}</div></details>
<details><summary>Grinder, every position against its minute candles</summary><p class="small">What the ledger booked beside what the candle path says, at £100 and the current cost model.</p><div class="scroll">${pathRows()}</div></details>
<details><summary>Spend</summary><p class="small">Cap ${gbp(s.cap_gbp)} a month, from the spend log.</p><table><tr><th>Month</th><th class="num">Spent</th><th class="num">Cap</th></tr>${spendRows}</table></details>
<details><summary>Claude usage</summary><p class="small">Tokens from the session transcripts, scheduled runs kept apart from the owner's own sessions. By session in <a href="${gh}USAGE.md">USAGE.md</a>.</p><div class="scroll">${usageHtml}</div></details>
</section>

<section id="check">
<h2>Check the score yourself</h2>
<p class="intro">Every number in the score is recomputed monthly on GitHub's machines by a script that shares no code with the scorer, and the run fails loudly if a line disagrees. Latest: <a href="https://github.com/triton-xxix/proteus-lab/actions/workflows/audit.yml"><img alt="audit status" src="https://github.com/triton-xxix/proteus-lab/actions/workflows/audit.yml/badge.svg" style="vertical-align:middle"></a>. The definitions, and what the audit cannot check, are in <a href="${gh}audit/README.md">audit/README.md</a>.</p>
</section>
</main>

<footer>Built ${esc(built)}; score from commit ${esc(commit)}. Ledgers, rules and code: <a href="https://github.com/triton-xxix/proteus-lab">github.com/triton-xxix/proteus-lab</a>.</footer>
</div>
</body>
</html>
`;

fs.mkdirSync(path.join(ROOT, 'docs'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'docs/index.html'), html);
console.log('wrote docs/index.html', noteFiles.length, 'notes,', closed.length, 'closed in', ver, '; kill check', kc.at || 'none');
