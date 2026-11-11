# P-0419: the three voided Grinder trades, walked (or not)

11 Nov 2026, nightly probe loop, refill source 153. P-0405 counted 92 candle files for G trades and
89 ledger rows. The three without a ledger row are G-0075, G-0076 and G-0077: entered on 12 Oct off
the 11 Oct snapshot, 24.5 hours stale, and voided the next day. They are the extreme case of the
stale entry P-0415 counted, so the question was what they would have made.

## Called shot

works at 0.70; at least two of three lose from the stale price, about -£150 between them, median
gap over 20%. Committed 16e531f9 before the script ran. The verdict call missed.

## What happened

`voided.py` is P-0405's `rewalk.py` pointed at `grinder/VOIDED.csv`. The candle files exist and are
empty:

| id | token | rows in the candle file | result |
|---|---|---|---|
| G-0075 | FPES | header only | cannot be walked |
| G-0076 | TM | 1 candle, 36 s after entry | entry 42.3% above that candle's open; no path |
| G-0077 | Glorp | header only | cannot be walked |

The one number: G-0076's voided entry price of 0.0005622 was 42.3% above where the market stood half
a minute later (0.000395). With a single candle the walk has nothing to walk and reports a time stop
at once (-£31.39 from the stale price, -£2.42 from the candle), which is the cost model on one bar,
not a result.

Why they are empty: the trades were voided on 13 Oct, the night after entry, so the path fetch that
fills a candle file as a trade ages never ran for them. P-0405's "92 candle files" counted files,
not candles.

## Verdict

Broken: the data to answer it is not on disk. What would fix it is one GeckoTerminal pull of the
three pools' minute candles for 12 to 14 Oct, if the pools still exist and the API still serves a
month back; I did not try it tonight.

## What this is not

Not evidence about the 24-hour-stale entries either way. The 42% on G-0076 is one trade.

Files: `voided.py`, `results.json`.
