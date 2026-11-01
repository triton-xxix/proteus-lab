# P-0280: the systems book's RSI(5) rule before every MPC decision (P-0274 with n)

1 Nov 2026, Trials 12:31, refill row 58. Source: the Bank of England's upcoming-MPC-dates page links `mpcvoting.xlsx` (the committee's voting history). Its Bank Rate sheet carries every meeting date since 6 June 1997: 315 in all, 175 since 2009 (twelve a year to 2015, eight a year from 2016, ten in 2020). Pulled keyless and parsed with zipfile and xml only (`boe-mpcvoting-parse.py`); the dates are in `mpc-decision-dates-since-2009.txt`. The old summary-and-minutes index URL is a 404 now.

Called shot before running: works, about 180 of the 966 trades in the 5-day pre-decision window (EWU about 20), pre minus rest inside plus or minus 0.5 points, permutation p above 0.05.

## What I did

`mpc_split.py` is P-0274's script with the 28 rate-change days swapped for the 175 decision days and a permutation test added. The book's RSI(5) simple rule, next-open fills, 2009 on, `sandbox/p0082` data. Each trade is labelled "pre" if its signal day sits in the 5 trading days before a decision day. Two tests per symbol set: the random-entry control from P-0243 (2,000 draws of random signal days from the same bucket's pool of days with the close above the 200-day average, holds drawn from the bucket's real trades), and a label permutation (5,000 shuffles of which trades carry "pre", two-sided p on the pre-minus-rest mean).

## Measured

The pre window covers 19.6% of trading days and catches 230 of 966 trades (23.8%).

| bucket | trades | mean | win | control | excess | p v control |
|---|---|---|---|---|---|---|
| EWU, pre | 21 | +0.54% | 71.4% | +0.07% | +0.47% | 0.186 |
| EWU, rest | 75 | +0.54% | 69.3% | +0.11% | +0.43% | 0.038 |
| SPY, pre | 28 | +1.20% | 75.0% | +0.32% | +0.88% | 0.006 |
| SPY, rest | 90 | +0.65% | 78.9% | +0.23% | +0.43% | 0.012 |
| all nine, pre | 230 | +0.80% | 73.9% | +0.22% | +0.58% | 0.0005 |
| all nine, rest | 736 | +0.61% | 75.7% | +0.20% | +0.41% | 0.000 |

Permutation on the label (pre minus rest): EWU -0.00 points, p 1.00; SPY +0.55 points, p 0.17; all nine +0.19 points, p 0.30.

## What it says

On EWU, the UK fund the question was about, the rule does exactly the same before a decision as at any other time: 21 v 75 trades, both +0.54%. Across the basket the pre-window trades are 0.19 points better, which the permutation test calls noise at p 0.30. SPY's +0.55 points at p 0.17 is the only hint, and SPY has no reason to care about the MPC. P-0274's "twice as good" on 26 trades was the small-n story it looked like.

Shot: hit on the verdict and the gap and the p; the count was 230, not 180 (I took the pre share of days as the share of trades, and signals cluster a little, 23.8% v 19.6%).

## What I did not do

No split by hike, cut or hold (the sheet has the votes, so that is one more column). No after-decision window. Nothing here changes the book.
