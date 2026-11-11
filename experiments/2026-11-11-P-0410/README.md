# P-0410: E-017 (Gap and go 0.5%) with its best trades removed

11 Nov 2026, nightly probe loop. Queued by Trials after P-0409, where the one gap-and-go video with
a sample (537 trades in seven months) said three trades made 92% of its profit.

## Called shot

works at 0.70; the top three trades carry about 35% of E-017's total, and the total stays above zero
with the best five removed. Committed 707a535e before the trade list was rebuilt.

## What I did

The scanner keeps totals, not trades, so `top_removed.py` imports `edges/scan/scan.py` (not edited),
pulls the same Yahoo 5-minute bars for the 12 names, runs the scanner's own `gap(D, 0.005, go=True)`
and keeps the trades on the 15 sessions E-017 was admitted on (19 to 23 Oct, 26 to 30 Oct, and 2, 3,
4, 6, 9 Nov). It rebuilt 121 trades summing to +36.896% after 0.03% costs, against 121 and
+36.89% in the register, so the list is the admission list.

## Numbers, admission window (121 trades)

| | total | mean a trade |
|---|---|---|
| all 121 | +36.90% | +0.305% |
| best 1 removed | +29.40% | +0.245% |
| best 3 removed | +20.58% | +0.174% |
| best 5 removed | +13.73% | +0.118% |
| best 10 removed | -0.31% | -0.003% |

- The top three carry 44.2% of the total (shot: about 35%). The top five 62.8%, the top ten 100.8%.
- Ten trades are the whole profit. The other 111 sum to nothing.
- The best is AMD on 9 Nov, +7.49% on a 5.4% gap up. Seven of the top ten are AMD, TSLA or AMZN.
- By day: three sessions (22 Oct +14.5, 9 Nov +15.7, 27 Oct +9.6) make +39.7 of the +36.9; 2 Nov
  alone was -13.6. It is a rule that has a few very good mornings.
- Against the video's 92% from three trades: mine is 44%, on 121 trades not 537. Less lopsided, same
  shape.

## The number I did not ask for

On every session in the 60-day feed, not just the 15 it was admitted on, the same rule made 393
trades for +19.80%, mean +0.050% a trade, 46% winners. Take out the best three and it is -1.95%.
So the 272 trades outside the admission window lost about 17.1% between them: the ladder admitted
the rule on its best three weeks of the last twelve, which is what a ladder does, and the luck figure
(6 climbers against about 7.6 by chance) already said so.

## What this is not

It changes nothing about E-017: the forward week (11, 12, 13, 16, 17 Nov, D-026) and its pass line
stand, and no parameter was touched. Removing the best trades is a description of a sample already
seen, not a test. The 60-day figure was pulled about 23:50 UK on 11 Nov; the scanner's own rule
drops the current UTC day, so the 11 Nov forward session should not be in it, and I did not check
that by hand. The 1% and 2% thresholds are in `results.json` and not read here.

Files: `top_removed.py`, `results.json`.
