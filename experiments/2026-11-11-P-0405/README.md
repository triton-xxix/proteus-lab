# P-0405: entry-price noise on the main Grinder book, paths re-walked

Trials, 11 Nov 2026. Deepen of P-0404 (R01 only, no re-walk).

## Question

For the main Grinder ledger (`grinder/LEDGER.csv`), how far is the ledger entry price from the open
of the first minute candle after entry, does it grow with the snapshot's age, and if every path is
re-walked with `paths.walk` from the candle price instead, how many exits flip and how far does the
book's total move?

## Called shot (before running)

works at 0.80; median absolute gap about 3 percent, 8 of 92 exit reasons flip, total moves by under
150 pounds. Not a blind shot on the gap (P-0404 gave 3.4 to 4.2 percent on R01 an hour earlier); the
flips and the pounds were blind.

## Method

`rewalk.py`, read only, no fetch. For each ledger row: saved candles from `grinder/candles/`, the
snapshot at or before entry from `grinder/SNAPSHOTS.csv`, then `paths.walk` twice, once from the
ledger entry price and once from the first candle's open. Both costed with `paths.pnl_v02` at a
£100 stake, so the two totals differ only by the entry price. v0.1 rows are walked under v0.2 rules
too, so these totals are not the published book totals.

The ledger has 89 rows, not the 92 I wrote in the probe title (92 candle files exist; three ids are
not in the ledger). All 89 had candles.

## Numbers

- Entry price is the snapshot price on 89 of 89. Snapshot age at entry: median 4.1 minutes, max 15.7.
- Gap to the first candle's open: median absolute 4.34%, 38 of 89 beyond 5%. Entry above the candle
  on 45, below on 44, median signed +0.18%. Noise, no tilt.
- By snapshot age: under 6 min (73 rows) median 3.87%; 6 to 15 min (12 rows) 6.44%; 15 min plus
  (4 rows) 33.8%. Same shape as R01: the older the snapshot, the wider the miss.
- Exit reasons flip on 7 of 89: G-0012 and G-0072 take profit to stop, G-0045 and G-0086 stop to
  take profit, G-0085 time stop to take profit, G-0052 stop to rug, G-0078 rug to time stop.
- Total at £100 a trade: -£1205.65 from the ledger price, -£1094.43 from the candle price, a move of
  +£111.22. Mean per trade -£13.55 against -£12.30.

## The one row that carries the move

G-0078 (NEIL) is +£99.42 of the +£111.22. Its snapshot was 15.7 minutes old and priced at 0.0001699;
the first candle 36 seconds after entry opened at 0.0000021, 98.7% lower. The token had already
collapsed before the book "bought" it. From the ledger price it is a rug in the first minute; from
the candle price it is a flat time stop. Take that row out and the other 88 move the total by
+£11.80, about 13p a trade.

So: entry noise is real (a 4% typical miss, 7 exits changed) but it nets to nothing. The book loses
about £12 to £13.50 a trade either way. The noise is not why the Grinder lost.

## What I did not do

- Did not change paper.py or any ledger. A stale-snapshot guard (skip an entry when the snapshot is
  over 10 minutes old, or price from the first candle) would have saved G-0078 and nothing else.
- Did not re-run under each row's own rule version and stake; the published book totals are untouched.
- Did not look at the three candle files with no ledger row.

## Files

`rewalk.py`, `results.json` (per-row gaps, both walks, flips).
