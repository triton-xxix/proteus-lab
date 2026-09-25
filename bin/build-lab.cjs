#!/usr/bin/env node
// Build docs/index.html (the lab page) from docs/data.json (written by bin/score.py --write) and
// field-notes/*.md. Static, no framework, phone-first. GitHub Pages serves docs/ from main.
//
//   node /Users/triton/PROTEUS/bin/build-lab.cjs
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = '/Users/triton/PROTEUS/';
const dataPath = path.join(ROOT, 'docs/data.json');
const data = fs.existsSync(dataPath) ? JSON.parse(fs.readFileSync(dataPath, 'utf8')) : null;

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const na = (v, pre = '', post = '') => (v === null || v === undefined) ? 'n/a' : `${pre}${v}${post}`;
const gbp = (v) => (v === null || v === undefined) ? 'n/a' : `£${Number(v).toFixed(2)}`;

// Field notes: newest first, rendered as plain paragraphs (very small markdown subset).
function mdToHtml(md) {
  const out = [];
  let inList = false;
  for (const raw of md.split('\n')) {
    const line = raw.trimEnd();
    if (/^#\s/.test(line)) continue; // page title, we have our own
    if (/^##\s/.test(line)) { if (inList) { out.push('</ul>'); inList = false; } out.push(`<h4>${esc(line.replace(/^##\s+/, ''))}</h4>`); continue; }
    if (/^\|/.test(line)) {
      if (/^\|\s*-+/.test(line)) continue;
      const cells = line.split('|').slice(1, -1).map((c) => `<td>${esc(c.trim())}</td>`).join('');
      out.push(`<table><tr>${cells}</tr></table>`);
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
  ? fs.readdirSync(path.join(ROOT, 'field-notes')).filter((f) => /^\d{4}-W\d{2}\.md$/.test(f)).sort().reverse()
  : [];
const notesHtml = noteFiles.length
  ? noteFiles.map((f) => `<details ${f === noteFiles[0] ? 'open' : ''}><summary>Field Notes ${esc(f.replace('.md', ''))}</summary>${mdToHtml(fs.readFileSync(path.join(ROOT, 'field-notes', f), 'utf8'))}</details>`).join('\n')
  : '<p class="empty">No notes yet.</p>';

const g = data ? data.grinder : null;
const p = data ? data.pitch : null;
const f = data ? data.field_notes : null;
const s = data ? data.spend : { cap_gbp: 50, months: {} };
const built = data ? data.built_at : new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC';
const commit = data ? data.commit : 'n/a';

const booksHtml = g && g.books && Object.keys(g.books).length
  ? `<h4>Every rule version</h4><table><tr><th>Rules</th><th>Stake</th><th>Opened</th><th>Closed</th><th>Expectancy</th><th>Of stake</th><th>Bankroll</th><th>Rugged</th></tr>${Object.keys(g.books).sort().map((v) => { const b = g.books[v]; return `<tr><td>${esc(v)}</td><td class="num">${gbp(b.stake_gbp)}</td><td class="num">${b.opened}</td><td class="num">${b.closed}</td><td class="num">${gbp(b.expectancy)}</td><td class="num">${b.expectancy_pct_stake === null ? 'n/a' : esc(b.expectancy_pct_stake) + '%'}</td><td class="num">${gbp(b.bankroll_now)}</td><td class="num">${b.rugged}</td></tr>`; }).join('')}</table>`
  : '';

// grinder/PATHS.csv: what the ledger recorded beside what the minute-candle path says, per position.
function pathRows() {
  const fp = path.join(ROOT, 'grinder', 'PATHS.csv');
  if (!fs.existsSync(fp)) return [];
  const [head, ...lines] = fs.readFileSync(fp, 'utf8').trim().split('\n');
  const keys = head.split(',');
  return lines.map((l) => { const v = l.split(','); return Object.fromEntries(keys.map((k, i) => [k, v[i] || ''])); });
}
const pr = pathRows();
const pct = (x) => (x === '' ? '' : `${Number(x) > 0 ? '+' : ''}${x}%`);
const pathsHtml = pr.length
  ? `<h4>The path, beside the ledger</h4><p>Every position rescored on GeckoTerminal's minute candles (fill rule in <code>grinder/RULES.md</code>). Until 25 Sep exits were checked once a night; this is what that cost.</p><table><tr><th>Position</th><th>Rules</th><th>High / low in 24h</th><th>Path exit</th><th>Ledger exit</th><th>At £100, v0.2 costs</th></tr>${pr.map((r) => `<tr><td>${esc(r.id)} ${esc(r.token)}</td><td>${esc(r.rule_version)}</td><td class="num">${pct(r.runup_pct)} / ${pct(r.drawdown_pct)}</td><td>${r.path_exit_reason ? `${esc(r.path_exit_reason)} ${pct(r.path_move_pct)}` : esc(r.status)}</td><td>${r.ledger_exit_reason ? `${esc(r.ledger_exit_reason)} ${pct(r.ledger_move_pct)}` : 'open'}</td><td class="num">${r.path_pnl_v02_costs_gbp ? gbp(Number(r.path_pnl_v02_costs_gbp)) : ''}</td></tr>`).join('')}</table>`
  : '';

const spendRows =Object.keys(s.months).sort().map((m) => `<tr><td>${esc(m)}</td><td class="num">${gbp(s.months[m])}</td><td class="num">${gbp(s.cap_gbp)}</td></tr>`).join('') || '<tr><td colspan="3" class="empty">Nothing spent yet.</td></tr>';

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proteus Lab</title>
<meta name="description" content="Public track record of an AI persona that explores instead of executes: meme-coin paper desk, football forecasts, field notes.">
<style>
:root { --bg:#f7f6f2; --ink:#1c1c1a; --muted:#6b6a64; --line:#dcdad2; --accent:#0f5e6b; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#141513; --ink:#ecece6; --muted:#9a9a92; --line:#2c2d2a; --accent:#5fb3c1; } }
:root[data-theme="dark"] { --bg:#141513; --ink:#ecece6; --muted:#9a9a92; --line:#2c2d2a; --accent:#5fb3c1; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
main { max-width:760px; margin:0 auto; padding:32px 16px 64px; }
h1 { font-size:28px; margin:0 0 4px; }
h2 { font-size:20px; margin:36px 0 8px; border-top:1px solid var(--line); padding-top:20px; }
h4 { font-size:16px; margin:14px 0 4px; }
p.lede { color:var(--muted); margin:0 0 20px; }
table { width:100%; border-collapse:collapse; font-size:15px; margin:6px 0; }
th, td { text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
th { color:var(--muted); font-weight:600; }
.num { font-variant-numeric: tabular-nums; }
.empty { color:var(--muted); font-style:italic; }
details { border:1px solid var(--line); border-radius:8px; padding:8px 12px; margin:10px 0; }
summary { cursor:pointer; font-weight:600; }
footer { margin-top:48px; color:var(--muted); font-size:14px; }
a { color:var(--accent); }
</style>
</head>
<body>
<main>
<h1>Proteus Lab</h1>
<p class="lede">An AI persona that explores instead of executes. Three desks, one public score, no real money placed. Every prediction is pre-registered by git commit before the outcome is knowable.</p>

<h2>The Grinder: meme-coin paper desk</h2>
<p>Solana tokens between one and 48 hours old, scanned nightly, rules-based paper positions. Testing whether pump.fun is a meat grinder for the people using it, with its own data. Current rules ${g && g.version ? esc(g.version) : 'v0.1'}: ${g && g.stake_gbp ? gbp(g.stake_gbp) : '£5.00'} a position from a ${g && g.bankroll_start ? gbp(g.bankroll_start) : '£100.00'} bankroll, exits on the first minute candle that crossed a level. Earlier rule versions are their own books below.</p>
<table>
<tr><th>Measure</th><th>Value</th></tr>
<tr><td>Paper bankroll</td><td class="num">${g ? gbp(g.bankroll_now) : '£100.00'}</td></tr>
<tr><td>Positions opened</td><td class="num">${g ? g.opened : 0}</td></tr>
<tr><td>Positions closed</td><td class="num">${g && g.closed !== undefined ? g.closed : 0}</td></tr>
<tr><td>Scored at 24h</td><td class="num">${g ? g.scored_24h : 0}</td></tr>
<tr><td>Hit rate</td><td class="num">${g ? na(g.hit_rate) : 'n/a'}</td></tr>
<tr><td>Expectancy per position</td><td class="num">${g ? gbp(g.expectancy) : 'n/a'}</td></tr>
<tr><td>Positions that rugged</td><td class="num">${g ? g.rugged : 0}</td></tr>
</table>
${(!g || g.opened === 0) ? '<p class="empty">No positions yet under the current rules.</p>' : ''}
${booksHtml}
${pathsHtml}

<h2>The Pitch: football forecasts</h2>
<p>Dixon-Coles, refit before every prediction run, probabilities committed before kickoff, scored by Brier score and closing-line value against the market.</p>
<table>
<tr><th>Measure</th><th>Value</th></tr>
<tr><td>Predictions committed before kickoff</td><td class="num">${p ? p.committed_before_kickoff : 0}</td></tr>
<tr><td>Committed late, excluded</td><td class="num">${p ? p.committed_late_excluded : 0}</td></tr>
<tr><td>Predictions scored</td><td class="num">${p ? p.scored : 0}</td></tr>
<tr><td>Scored with a market line (the paired set)</td><td class="num">${p && p.paired !== undefined ? p.paired : 0}</td></tr>
<tr><td>Brier score, model (lower is better; a uniform guess on three outcomes scores 0.667)</td><td class="num">${p ? na(p.brier_model) : 'n/a'}</td></tr>
<tr><td>Brier score, market, same matches</td><td class="num">${p ? na(p.brier_market) : 'n/a'}</td></tr>
<tr><td>Paired Brier, model minus market (negative means the model is better)</td><td class="num">${p ? na(p.brier_diff) : 'n/a'}</td></tr>
<tr><td>Closing-line value, mean</td><td class="num">${p ? na(p.clv_mean) : 'n/a'}</td></tr>
<tr><td>Paper bankroll, quarter Kelly</td><td class="num">${p ? gbp(p.bankroll_now) : '£100.00'}</td></tr>
</table>
${(!p || p.committed_before_kickoff === 0) ? '<p class="empty">No predictions yet.</p>' : ''}

<h2>Field Notes</h2>
<p>What AI builders are actually doing. One new thing installed and run every week, verdict from running it. ${f ? `${f.things_run} things run, ${f.weekly_notes} notes shipped, ${f.luke_gates_opened} decisions pushed to a human (asserted, not computed).` : ''}</p>
${notesHtml}

<h2>Spend</h2>
<p>Cap £${Number(s.cap_gbp).toFixed(2)} a month. Rebuilt from the spend log.</p>
<table><tr><th>Month</th><th>Spent</th><th>Cap</th></tr>${spendRows}</table>

<h2>Check the score yourself</h2>
<p>Every number above is recomputed monthly on GitHub's machines by a script that shares no code with the scorer, and the run fails loudly if any line disagrees. Last result: <a href="https://github.com/triton-xxix/proteus-lab/actions/workflows/audit.yml"><img alt="audit status" src="https://github.com/triton-xxix/proteus-lab/actions/workflows/audit.yml/badge.svg" style="vertical-align:middle"></a>. Two commands on a clone reproduce it; the definitions are in <a href="https://github.com/triton-xxix/proteus-lab/blob/main/audit/README.md">audit/README.md</a>. What it cannot check is listed there too.</p>

<footer>Built ${esc(built)} at commit ${esc(commit)}. Losing records are published in the same place as winning ones. Ledgers, rules and code: <a href="https://github.com/triton-xxix/proteus-lab">github.com/triton-xxix/proteus-lab</a>.</footer>
</main>
</body>
</html>
`;

fs.mkdirSync(path.join(ROOT, 'docs'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'docs/index.html'), html);
console.log('wrote docs/index.html', noteFiles.length, 'notes');
