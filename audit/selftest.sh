#!/usr/bin/env bash
# Prove the audit does its job before trusting it: on synthetic ledgers with real values, the
# scorer (bin/score.py) and the independent recompute (audit/recompute.js) must agree; then a
# tampered published number must make the recompute fail; then a ledger edited after scoring must
# make the provenance check fail. Runs in a throwaway git repository under mktemp. Needs bash,
# git, python3 and node. Exit 0 when all three hold.
#
#   bash audit/selftest.sh
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$(dirname "$HERE")"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/audit" "$T/bin" "$T/grinder" "$T/pitch" "$T/field-notes" "$T/state" "$T/docs"
cp "$HERE/recompute.js" "$T/audit/recompute.js"
# The scorer has its root fixed to the Proteus folder; point the copy at the fixture instead.
sed "s#/Users/triton/PROTEUS/#$T/#g" "$SRC/bin/score.py" > "$T/bin/score.py"

# Grinder: 5 positions; 3 closed (one a rug), 2 open; two scored at 24h; one name with a comma.
cat > "$T/grinder/LEDGER.csv" <<'EOF'
id,entered_at,token,mint,entry_price_usd,size_gbp,rule_version,entry_liq_usd,exit_at,exit_price_usd,exit_reason,pnl_gbp,score_24h,score_7d,rugged
G-0001,2026-09-01T00:00:00Z,"FOO, INC",mint1,0.001,5.0,v0.1,50000,2026-09-02T00:00:00Z,0.0021,take_profit,2.5,110.0,,0
G-0002,2026-09-01T00:00:00Z,BAR,mint2,0.002,5.0,v0.1,60000,2026-09-02T00:00:00Z,0.0001,rug,-3.1,-95.0,,1
G-0003,2026-09-01T00:00:00Z,BAZ,mint3,0.003,5.0,v0.1,70000,2026-09-02T00:00:00Z,0.0035,time_stop,0.12,,,0
G-0004,2026-09-03T00:00:00Z,QUX,mint4,0.004,5.0,v0.1,80000,,,,,,,
G-0005,2026-09-03T00:00:00Z,QUUX,mint5,0.005,5.0,v0.1,90000,,,,,,,
EOF

# Pitch: 4 rows; one committed after kickoff (late); two scored with both Briers; one scored with
# a model Brier only (must be dropped from the paired means but kept in "scored").
cat > "$T/pitch/PREDICTIONS.csv" <<'EOF'
id,committed_at,kickoff_utc,competition,home,away,p_home,p_draw,p_away,p_over25,market_home,market_draw,market_away,market_over25,backed,stake_gbp,odds_taken,result,home_goals,away_goals,brier,market_brier,clv,pnl_gbp
P-0001,2026-09-05T10:00:00Z,2026-09-05T14:00:00Z,E0,Arsenal,Chelsea,0.5,0.25,0.25,0.55,0.45,0.27,0.28,0.5,home,2.5,2.1,H,2,0,0.375,0.4234,0.05,2.75
P-0002,2026-09-05T10:00:00Z,2026-09-05T14:00:00Z,E0,Leeds,Burnley,0.4,0.3,0.3,0.5,0.42,0.28,0.30,0.5,,0,,A,0,1,0.74,0.7012,,0
P-0003,2026-09-05T10:00:00Z,2026-09-06T14:00:00Z,E1,Hull,Derby,0.35,0.3,0.35,0.5,,,,,,,,D,1,1,0.6151,,,0
P-0004,2026-09-05T15:00:00Z,2026-09-05T14:00:00Z,E0,Spurs,Everton,0.5,0.25,0.25,0.55,0.45,0.27,0.28,0.5,,0,,LATE,,,,,,
EOF

printf '# Field Notes 2026-W36\n\n## Ran it\n\nA thing. Verdict: works.\n\n## Score\n' > "$T/field-notes/2026-W36.md"
printf '# Field Notes 2026-W37\n\nNothing run this week.\n\n## Watched it\n' > "$T/field-notes/2026-W37.md"
printf '# not a weekly note\n\n## Ran it\n' > "$T/field-notes/SEEN.md"
cat > "$T/state/spend.jsonl" <<'EOF'
{"date": "2026-08-03", "service": "The Odds API", "amount_gbp": 12.5}
{"date": "2026-08-20", "service": "Helius", "amount_gbp": 0.01}
this line is not json and must be ignored
EOF

git -C "$T" init -q
git -C "$T" -c user.name=selftest -c user.email=selftest@example.invalid add -A
git -C "$T" -c user.name=selftest -c user.email=selftest@example.invalid commit -q -m "fixture ledgers"
python3 "$T/bin/score.py" --write > /dev/null
git -C "$T" -c user.name=selftest -c user.email=selftest@example.invalid add -A
git -C "$T" -c user.name=selftest -c user.email=selftest@example.invalid commit -q -m "score"

echo "1. scorer and recompute must agree on the fixture"
if ! node "$T/audit/recompute.js" > "$T/run1.md"; then cat "$T/run1.md"; echo "FAIL: they disagree"; exit 1; fi
# Spot-check the recompute against hand-worked values so a shared misreading cannot hide.
grep -q '| grinder.bankroll_now | 99.52 | 99.52 | 99.5200 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: bankroll line not as hand-worked"; exit 1; }
grep -q '| grinder.expectancy | -0.16 | -0.16 | -0.1600 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: expectancy line not as hand-worked"; exit 1; }
grep -q '| grinder.hit_rate | 0.667 | 0.667 | 0.66667 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: hit rate line not as hand-worked"; exit 1; }
grep -q '| grinder.rugged | 1 | 1 | 1 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: rug count not 1"; exit 1; }
grep -q '| pitch.paired | 2 | 2 | 2 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: paired count not 2"; exit 1; }
grep -q '| pitch.brier_diff | -0.0048 | -0.0048 | -0.004800 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: paired Brier difference not as hand-worked"; exit 1; }
grep -q '| pitch.committed_late_excluded | 1 | 1 | 1 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: late count not 1"; exit 1; }
grep -q '| field_notes.things_run | 1 | 1 | 1 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: things_run not 1"; exit 1; }
grep -q '| spend.2026-08 | 12.51 |  | 12.5100 | OK |' "$T/run1.md" || { cat "$T/run1.md"; echo "FAIL: August spend not 12.51"; exit 1; }
echo "   agreed, and the hand-worked lines match"

echo "2. a tampered published number must be caught"
node -e "const fs=require('fs');const p='$T/docs/data.json';const d=JSON.parse(fs.readFileSync(p));d.grinder.bankroll_now=Math.round((d.grinder.bankroll_now+0.01)*100)/100;fs.writeFileSync(p,JSON.stringify(d,null,1))"
git -C "$T" -c user.name=selftest -c user.email=selftest@example.invalid commit -q -am "one penny in the record's favour"
if node "$T/audit/recompute.js" > "$T/run2.md"; then cat "$T/run2.md"; echo "FAIL: a one-penny lie went unnoticed"; exit 1; fi
grep -q '| grinder.bankroll_now | .* | FAIL |' "$T/run2.md" || { cat "$T/run2.md"; echo "FAIL: wrong line blamed"; exit 1; }
echo "   caught"

echo "3. a ledger edited after scoring must fail provenance"
git -C "$T" checkout -q HEAD~1 -- docs/data.json
printf 'G-0006,2026-09-04T00:00:00Z,SIX,mint6,0.006,5.0,v0.1,10000,2026-09-05T00:00:00Z,0.0001,rug,-4.9,,,1\n' >> "$T/grinder/LEDGER.csv"
git -C "$T" -c user.name=selftest -c user.email=selftest@example.invalid commit -q -am "ledger row added without rescoring"
if node "$T/audit/recompute.js" > "$T/run3.md"; then cat "$T/run3.md"; echo "FAIL: stale score not noticed"; exit 1; fi
grep -q '| grinder/LEDGER.csv | .* | FAIL |' "$T/run3.md" || { cat "$T/run3.md"; echo "FAIL: provenance line did not fail"; exit 1; }
echo "   caught"
echo "selftest passed: agreement on real values, tampering caught, stale inputs caught"
