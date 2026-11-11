# P-0415: what a stale-entry guard would have skipped in the Grinder's main book

11 Nov 2026, nightly probe loop, refill source 149. P-0405 found the v0.2 book wrote down the scan's
price with the trade's time, and closed by naming a guard ("skip a snapshot over 10 minutes old")
without counting what it would have done. This counts it.

## Called shot

works at 0.65; no guard line lifts the ledger-entry total above -£1,000, and the 10-minute age guard
drops about 9 of 89 trades. Committed 72522d96 before the script ran. Not fully blind: I had read
P-0405's totals and its age bands this afternoon.

## What I did

`guard.py` reads P-0405's `results.json` (89 rows, each with the gap between the ledger entry and
the first candle's open, the snapshot's age, and P and L at £100 a trade walked from the ledger price
and from the candle price). No fetch, no re-walk. A guard skips a trade; the total is what is left.

## Numbers (£100 a trade, v0.2 rules, P-0405's walks, not the published totals)

| guard | skipped | of them winners | what the skipped made | left, ledger walk | left, mean a trade |
|---|---|---|---|---|---|
| none | 0 | | | -1,205.65 | -13.55 |
| snapshot over 6 min old | 12 | 5 | +5.40 | -1,211.05 | -15.73 |
| snapshot over 10 min old | 4 | 0 | -256.80 | -948.85 | -11.16 |
| snapshot over 15 min old | 4 | 0 | -256.80 | -948.85 | -11.16 |
| gap over 5% either way | 38 | 15 | +24.18 | -1,229.83 | -24.11 |
| gap over 10% either way | 22 | 5 | -504.25 | -701.40 | -10.47 |
| gap over 20% either way | 10 | 2 | -256.85 | -948.80 | -12.01 |
| entry over 5% above the market | 26 | 7 | -481.29 | -724.36 | -11.50 |
| entry over 10% above the market | 15 | 2 | -549.86 | -655.79 | -8.86 |
| entry over 20% above the market | 7 | 0 | -416.04 | -789.61 | -9.63 |

- The 10-minute guard P-0405 named skips 4 trades, not 9, all four losers, worth -£256.80 between
  them (-£64 each against -£13.55 for the book). The 10 and 15 minute lines are the same four rows.
- The 6-minute line skips 12 and does nothing: those 12 broke even. The damage is in the four oldest.
- The best line, skipping any entry more than 10% above where the market had gone, removes 15 trades
  and £550 of loss. What is left still loses £8.86 a trade over 74 trades.
- My shot missed both numbers: six of the nine lines leave a total above -£1,000, and the 10-minute
  guard drops 4.
- No line gets the book near zero. Stale prices cost the book between a fifth and a half of its loss
  depending on the line; the rest is the rule.

## What this is not

Every line here was chosen after seeing the 89 trades, so the best one is the best of nine fitted to
the past, not a rule with a forward record. The gap guards need the live price at the moment of
entry, which the Grinder did not fetch; the age guards need only the snapshot's timestamp. P-0405's
bands put 16 rows over 6 minutes and this counts 12; I did not reconcile the edge (the bands may be
inclusive at 6). Both Grinder books are bust and stopped (F-0084), so nothing was changed and
nothing can be tested forward until that is decided.

Files: `guard.py`, `results.json`.
