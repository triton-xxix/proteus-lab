#!/usr/bin/env node
'use strict';
// Recompute Proteus's published headline numbers from the committed ledgers, without bin/score.py,
// and compare. Exit 0 if every line agrees, 1 if any line disagrees. Zero dependencies: node and git.
//
//   node audit/recompute.js                 # audit the last commit that changed docs/data.json
//   node audit/recompute.js --at <rev>      # audit a specific commit
//   node audit/recompute.js --worktree      # audit the files on disk (the Sunday run, before commit)
//   node audit/recompute.js --report out.md # also append the markdown report to a file
//
// The definitions this file implements are written in prose in audit/README.md. If this file and
// bin/score.py disagree, one of them is wrong and the README says which reading is intended. This
// script deliberately shares no code with score.py: different language, its own CSV parser, its
// own date handling, its own rounding rule.

const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null; };
const WORKTREE = args.includes('--worktree');
const REPORT = opt('--report');

function git(...a) {
  return cp.execFileSync('git', ['-C', ROOT, ...a], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
}
function tryGit(...a) { try { return git(...a); } catch (e) { return null; } }

// ---- where the inputs come from -----------------------------------------------------------------
let REV = null;
if (!WORKTREE) {
  REV = opt('--at') || (tryGit('log', '-1', '--format=%H', '--', 'docs/data.json') || '').trim();
  if (!REV) { console.error('no commit touches docs/data.json; nothing to audit'); process.exit(2); }
  REV = git('rev-parse', REV).trim();
}
function read(p) {
  if (WORKTREE) { try { return fs.readFileSync(path.join(ROOT, p), 'utf8'); } catch (e) { return null; } }
  return tryGit('show', `${REV}:${p}`);
}
function readBytes(p) {
  if (WORKTREE) { try { return fs.readFileSync(path.join(ROOT, p)); } catch (e) { return null; } }
  const out = tryGit('cat-file', '-p', `${REV}:${p}`);
  return out === null ? null : Buffer.from(out, 'utf8');
}
function listFieldNotes() {
  let names;
  if (WORKTREE) names = fs.readdirSync(path.join(ROOT, 'field-notes'));
  else names = (tryGit('ls-tree', '--name-only', REV, 'field-notes/') || '').split('\n').map((l) => l.replace(/^field-notes\//, ''));
  return names.filter((n) => /^\d{4}-W\d{2}\.md$/.test(n)).sort();
}
function blobId(p) {
  if (WORKTREE) {
    const b = readBytes(p);
    if (b === null) return null;
    return crypto.createHash('sha1').update(`blob ${b.length}\0`).update(b).digest('hex');
  }
  const out = tryGit('rev-parse', `${REV}:${p}`);
  return out === null ? null : out.trim();
}

// ---- tiny CSV (RFC 4180: quoted fields, doubled quotes, CRLF) ----------------------------------
function parseCsv(text) {
  const rows = []; let row = []; let field = ''; let q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else q = false; } else field += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else if (c === '\r') { /* ignore */ }
    else field += c;
  }
  if (field !== '' || row.length) { row.push(field); rows.push(row); }
  if (!rows.length) return [];
  const head = rows[0];
  return rows.slice(1)
    .filter((r) => !(r.length === 1 && r[0] === ''))
    .map((r) => Object.fromEntries(head.map((h, j) => [h, r[j] === undefined ? '' : r[j]])));
}

// A numeric cell is a plain decimal. Blank is "not filled". Anything else (nan, inf, text) is not a number.
function num(s) {
  if (s === null || s === undefined) return null;
  s = String(s).trim();
  if (s === '' || !/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(s)) return null;
  const v = Number(s);
  return Number.isFinite(v) ? v : null;
}
const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const truthy = (s) => ['1', 'true', 'yes'].includes(String(s || '').trim().toLowerCase());
// Timestamps in the ledgers are UTC in this exact shape. Anything else is not a valid stamp.
const TS = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$/;
const ts = (s) => (TS.test(String(s || '').trim()) ? Date.parse(String(s).trim()) : NaN);

// ---- the recompute ------------------------------------------------------------------------------
function grinder(csv) {
  const rows = parseCsv(csv);
  const pnl = rows.map((r) => num(r.pnl_gbp)).filter((v) => v !== null);
  return {
    bankroll_now: 100 + pnl.reduce((a, b) => a + b, 0),
    opened: rows.length,
    closed: pnl.length,
    scored_24h: rows.filter((r) => num(r.score_24h) !== null).length,
    hit_rate: pnl.length ? pnl.filter((v) => v > 0).length / pnl.length : null,
    expectancy: mean(pnl),
    rugged: rows.filter((r) => truthy(r.rugged)).length,
  };
}

function pitch(csv) {
  const rows = parseCsv(csv);
  const valid = rows.filter((r) => { const c = ts(r.committed_at); const k = ts(r.kickoff_utc); return !isNaN(c) && !isNaN(k) && c < k; });
  const scored = valid.filter((r) => num(r.brier) !== null);
  const paired = scored.filter((r) => num(r.market_brier) !== null);
  const clv = scored.map((r) => num(r.clv)).filter((v) => v !== null);
  const pnl = scored.map((r) => num(r.pnl_gbp)).filter((v) => v !== null);
  return {
    committed_before_kickoff: valid.length,
    committed_late_excluded: rows.length - valid.length,
    scored: scored.length,
    paired: paired.length,
    brier_model: mean(paired.map((r) => num(r.brier))),
    brier_market: mean(paired.map((r) => num(r.market_brier))),
    brier_diff: mean(paired.map((r) => num(r.brier) - num(r.market_brier))),
    clv_mean: mean(clv),
    bankroll_now: 100 + pnl.reduce((a, b) => a + b, 0),
  };
}

function fieldNotes(names) {
  let ran = 0;
  for (const n of names) {
    const txt = read(`field-notes/${n}`) || '';
    ran += txt.split('\n').filter((l) => /^##\s+ran it/i.test(l)).length;
  }
  return { weekly_notes: names.length, things_run: ran };
}

function spend(jsonl, builtMonth) {
  const months = {};
  for (const line of (jsonl || '').split('\n')) {
    if (!line.trim()) continue;
    let e; try { e = JSON.parse(line); } catch (err) { continue; }
    if (!e || typeof e.date !== 'string' || num(e.amount_gbp) === null) continue;
    const m = e.date.slice(0, 7);
    months[m] = (months[m] || 0) + num(e.amount_gbp);
  }
  if (builtMonth && !(builtMonth in months)) months[builtMonth] = 0;
  return months;
}

// ---- the published numbers ----------------------------------------------------------------------
const dataText = read('docs/data.json');
if (dataText === null) { console.error('docs/data.json not found at ' + (WORKTREE ? 'worktree' : REV)); process.exit(2); }
const pub = JSON.parse(dataText);
const trackMd = read('TRACK-RECORD.md') || '';

function trackValues(md) {
  const out = {};
  for (const line of md.split('\n')) {
    const m = line.match(/^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$/);
    if (m) out[m[1]] = m[2];
  }
  return out;
}
function trackNumber(labelPrefix) {
  const tv = trackValues(trackMd);
  const keys = Object.keys(tv);
  const key = keys.find((k) => k === labelPrefix) || keys.find((k) => k.startsWith(labelPrefix));
  if (!key) return undefined;                     // row absent from the markdown
  const v = tv[key].trim();
  if (/^n\/a/i.test(v)) return null;
  const m = v.replace(/£/g, '').match(/[-+]?\d+(\.\d+)?/);
  return m ? Number(m[0]) : undefined;
}

// ---- comparison ----------------------------------------------------------------------------------
// A published number passes if it is a correct rounding of the recomputed exact value at the
// published precision: |published - exact| <= half a unit in the last place. Counts must be equal.
function agrees(published, exact, dp) {
  if (published === null || published === undefined) return exact === null;
  if (exact === null) return false;
  if (dp === 0) return Number(published) === exact;
  return Math.abs(Number(published) - exact) <= 0.5 * Math.pow(10, -dp) + 1e-9;
}
// Published values are shown at their published precision, recomputed ones with two more decimals.
const fmt = (v, dp, extra = 0) => (v === null || v === undefined ? (v === undefined ? 'absent' : 'n/a') : (dp === 0 ? String(v) : Number(v).toFixed(dp + extra)));

const builtMonth = (pub.built_at || '').slice(0, 7) || null;
const mine = {
  grinder: grinder(read('grinder/LEDGER.csv') || ''),
  pitch: pitch(read('pitch/PREDICTIONS.csv') || ''),
  field_notes: fieldNotes(listFieldNotes()),
  spend: spend(read('state/spend.jsonl'), builtMonth),
};

const LINES = [
  // [section, key, decimals, TRACK-RECORD.md row label prefix (null = not in the markdown)]
  ['grinder', 'bankroll_now', 2, 'Paper bankroll'],
  ['grinder', 'opened', 0, 'Positions opened'],
  ['grinder', 'closed', 0, 'Positions closed'],
  ['grinder', 'scored_24h', 0, 'Positions scored at 24h'],
  ['grinder', 'hit_rate', 3, 'Hit rate'],
  ['grinder', 'expectancy', 2, 'Expectancy per position'],
  ['grinder', 'rugged', 0, 'Positions that rugged'],
  ['pitch', 'committed_before_kickoff', 0, 'Predictions committed before kickoff'],
  ['pitch', 'committed_late_excluded', 0, 'Predictions committed late'],
  ['pitch', 'scored', 0, 'Predictions scored'],
  ['pitch', 'paired', 0, 'Predictions scored with a market line'],
  ['pitch', 'brier_model', 4, 'Brier score, model'],
  ['pitch', 'brier_market', 4, 'Brier score, market'],
  ['pitch', 'brier_diff', 4, 'Paired Brier'],
  ['pitch', 'clv_mean', 4, 'Closing-line value'],
  ['pitch', 'bankroll_now', 2, 'Paper bankroll, quarter Kelly'],
  ['field_notes', 'weekly_notes', 0, 'Weekly notes shipped'],
  ['field_notes', 'things_run', 0, 'Things installed and run'],
];

const results = [];
let fails = 0;
for (const [sec, key, dp, label] of LINES) {
  const p = pub[sec] ? pub[sec][key] : undefined;
  const exact = mine[sec][key];
  const okJson = p === undefined ? (key === 'closed' || key === 'paired' || key === 'brier_diff' ? null : false) : agrees(p, exact, dp);
  // Rows added to the scorer on 2026-09-24 (closed, paired, brier_diff) are allowed to be absent
  // from a data.json built before then; every other absence is a failure.
  const tv = label ? trackNumber(label) : undefined;
  const okMd = label === null ? null : (tv === undefined ? (okJson === null ? null : false) : agrees(tv, exact, dp));
  const verdict = okJson === false || okMd === false ? 'FAIL' : (okJson === null ? 'SKIP' : 'OK');
  if (verdict === 'FAIL') fails++;
  results.push({ line: `${sec}.${key}`, json: fmt(p, dp), md: label === null ? '' : fmt(tv, dp), mine: fmt(exact, dp, 2), verdict });
}

// Spend: month by month, from the committed spend log, for the month the score was built in and every month in it.
const pubMonths = (pub.spend && pub.spend.months) || {};
for (const m of new Set([...Object.keys(pubMonths), ...Object.keys(mine.spend)])) {
  const p = m in pubMonths ? pubMonths[m] : undefined;
  const e = m in mine.spend ? mine.spend[m] : null;
  const ok = p === undefined ? false : agrees(p, e, 2);
  if (!ok) fails++;
  results.push({ line: `spend.${m}`, json: fmt(p, 2), md: '', mine: fmt(e, 2, 2), verdict: ok ? 'OK' : 'FAIL' });
}

// Provenance: did the scorer read the bytes that are in this commit?
const prov = [];
if (pub.input_blobs) {
  for (const [p, sha] of Object.entries(pub.input_blobs)) {
    const here = blobId(p);
    const ok = sha === here || (sha === null && here === null);
    if (!ok) fails++;
    prov.push({ path: p, stamped: sha ? sha.slice(0, 12) : 'absent', here: here ? here.slice(0, 12) : 'absent', verdict: ok ? 'OK' : 'FAIL' });
  }
} else {
  prov.push({ path: '(none)', stamped: 'no input_blobs in data.json', here: 'scorer older than 2026-09-24', verdict: 'SKIP' });
}

// ---- report ---------------------------------------------------------------------------------------
const where = WORKTREE ? 'working tree' : `commit ${REV.slice(0, 12)}`;
const out = [];
out.push(`# Audit of the scorer: ${fails ? 'DISAGREEMENT' : 'agrees'} (${where})`);
out.push('');
out.push(`Published: data.json built ${pub.built_at || '?'} at commit ${pub.commit || '?'}. Recomputed by audit/recompute.js from the ledgers at ${where}, without bin/score.py.`);
out.push('');
out.push('| Line | data.json | TRACK-RECORD.md | Recomputed (exact) | Result |');
out.push('|---|---|---|---|---|');
for (const r of results) out.push(`| ${r.line} | ${r.json} | ${r.md} | ${r.mine} | ${r.verdict} |`);
out.push('');
out.push('| Input | Blob id the scorer stamped | Blob id at this commit | Result |');
out.push('|---|---|---|---|');
for (const r of prov) out.push(`| ${r.path} | ${r.stamped} | ${r.here} | ${r.verdict} |`);
out.push('');
out.push('Not checkable from the tree, and not counted above: luke_gates_opened (asserted 0 by the scorer; nothing in the repository can prove a negative), and SPEND.md (typed by hand; the spend log above is the computed source).');
out.push('');
out.push(fails ? `**${fails} line(s) disagree. The published record is wrong or the audit is; either way, this goes at the top of the next Field Notes.**`
              : 'Every published line is a correct rounding of the recomputed value, and the scorer read the bytes in this commit.');
const text = out.join('\n') + '\n';
process.stdout.write(text);
if (REPORT) fs.appendFileSync(REPORT, text);
process.exit(fails ? 1 : 0);
