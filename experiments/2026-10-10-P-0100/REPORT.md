# P-0100 / DUE D-009: G2 fill realism, not finished tonight

Date: 2026-10-10, nightly probe loop.

## What is fixed
`reprice.py` carries the rules in its docstring, written before any candle came back: the first 403 G2
counted trades as `bin/killcheck.py` counts them, entry at the close of the first full 1-minute
GeckoTerminal candle after entry, the -50% stop and 20-minute exit re-run on candle closes with the
fill at the next close, costs by `paths.pnl_v02` unchanged, and the D-009 lines (expectancy at least
+£10 per £100 and best-10-removed at least zero).

## What happened
GeckoTerminal does have week-old 1-minute candles (the first trade, 3 Oct, came back with a full
window). But keyless it served about one trade a minute (two calls each: pool lookup and candles),
with 429 back-offs, against the 28 calls a minute I paced for. The full 403 is about seven hours.

The job could not be stopped from the scheduled run (TaskStop is not on the safe list), so it was left
running. It only reads public candles and appends to `candles.jsonl` in this folder, which is a resume
cache: a later run skips every trade already fetched.

## Verdict
Blocked, on time: the pre-registered test needs about seven hours of keyless pulls. A partial sample is
not D-009 and I have not looked at one. The G2 KEEP stands untested, not confirmed.

## Next
Run `reprice.py` as a long-running job under the charter's rules (launchd from this folder, stops at a
fixed time, HALT-aware), or halve the calls by taking pool addresses from DexScreener 30 at a time.
D-009's backstop is 11 Oct; it will be overdue, and the run log says so.
