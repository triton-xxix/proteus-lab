# P-0404: R01 entry prices against the minute candles

Trials, 11 Nov 2026. Refill source 142.

## Question

P-0384 and P-0390 said GeckoTerminal's feed is stale on young pools. For the 29 entries in the
Grinder's R01 shadow book, how far was the ledger entry price from the minute candle at the entry
time, in percent?

## Called shot (before running)

works at 0.80; median absolute gap to the entry-minute close under 1 percent, 3 of 29 beyond 5 percent.
I had seen one row first (R-0001's first saved candle closed within 0.01% of its entry price), which
is where the "under 1 percent" came from. It was one row and it misled me.

## Method

`gap.py`, read only. For each row of `grinder/LEDGER-R01.csv`:

- the pool from `grinder/SNAPSHOTS.csv`, same rule as `paths.pool_for` (R rows are not in PATHS.csv,
  which cost one wasted run);
- one keyless GeckoTerminal call, `/pools/ADDRESS/ohlcv/minute` with `before_timestamp` just past the
  entry minute, for the entry minute's candle and the one before it;
- the saved candles in `grinder/candles/R-00NN.csv` for the next candle after entry.

29 calls, no errors, no rate-limit waits.

## Numbers

| entry price against | median abs gap | worst | beyond 5% | beyond 1% | entry above / below |
|---|---|---|---|---|---|
| close of the entry minute | 4.20% | 69.28% (R-0023) | 11 of 29 | 27 of 29 | 16 / 13 |
| close of the candle before | 3.99% | 44.27% | 12 of 29 | 25 of 29 | 15 / 14 |
| open of the next candle | 3.42% | 70.73% | 11 of 29 | 28 of 29 | 15 / 14 |

The entry price sat inside the entry minute's own low to high range on 8 of 29. On the other 21 the
book "bought" at a price the market did not trade at in that minute.

## Why

The ledger entry price is the scan snapshot's price on 29 of 29, to the last digit, and the snapshot
is older than the stamped entry time every time: about 4 minutes on R-0001 to R-0015, then 11 to 25
minutes on R-0016 to R-0029 (the nights the run reached the paper step later).

Split by that delay, by hand from `results.json`, gap to the entry-minute close:

- about 4 minutes old (15 entries): median 2.35%, worst 14.8%, 3 beyond 5%.
- 11 to 25 minutes old (14 entries): median 9.48%, worst 69.3%, 8 beyond 5%.

So this is not GeckoTerminal's cache. It is my own book stamping a price from the scan with the time
of the paper step. The gap grows with the delay.

No sign it flattered the book: entry was above the candle close on 16 and below on 13, median signed
gap +0.99% (the book paid slightly more than the market, if anything). It is noise, not a tilt, on
29 rows.

## What I did not do

- Did not re-walk the 29 paths from the candle price to see what the book's P&L would have been.
  R01 is at -£93.83 either way (F-0084), and a few percent of entry noise against a 50% stop does
  not rescue it.
- Did not check the v0.2 book (LEDGER.csv, 92 rows), which takes its entry price the same way.
- Did not change paper.py. The fix, if the Grinder ever trades again, is to price the entry from the
  first candle after the entry time, which the path walker already fetches.

## Files

`gap.py`, `results.json` (per-row gaps, pools, snapshot times).
