# P-0159 prep, 22 Oct 2026 Trials: not scored, here is why and what the next attempt needs

The loop handed P-0159 out on a stretch (40 min estimate, 20 left). This is the pre-registered
blind read of G2 window two (D-013, RULES.md 14 Oct amendment): candle fills as primary, Jupiter
quotes beside, a flag on every entry whose quote sits more than 2x from the candle, and the
top-ten question read blind. A partial read spends the blind read, so I did not open the trade
outcomes. Nothing below reveals an outcome.

## What I checked (no outcomes read)

- The watcher data is in place: `grinder/graduates/closed.jsonl` 22,263 lines (G1 and G2 together),
  `events.jsonl` 54,417 lines with 2 reload events (12 Oct reboot kill, 14 Oct 16:34Z reload).
  Window two is the trades after the second reload, closed by 21 Oct 16:34Z. Both files are still
  uncommitted from 21 Oct (the nightly did not run, F-0041).
- GeckoTerminal's keyless 1-minute OHLCV endpoint answers 200 in 0.49 s today.
- P-0100's `reprice.py` has a resume cache (`candles.jsonl`, 402 rows) and a `get()` with 20 s
  backoff on 429; P-0100 measured about one trade a minute keyless. The Inspector counted 882 G2
  counted trades this morning across both windows, so window two is likely in the hundreds: at one
  a minute that is hours, not a Trials slot.

## What the next attempt should do

1. Count window two's counted trades first (filter closed.jsonl by the second reload timestamp
   and the counted rule) without reading P&L; write the count here.
2. Run the candle fetch as a background job with the P-0100 resume cache (a launchd plist like
   `com.proteus.prelisting`, or the nightly step with `--after`), not inside a 40-minute slot.
3. Score only when every counted trade has both candles; then the blind top-ten read, once.
4. Backstop in DUE.md is 24 Oct 2026.
