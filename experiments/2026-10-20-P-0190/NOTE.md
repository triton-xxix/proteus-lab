# P-0190: two small books as posteriors

Refill from Bayesian Methods for Hackers, chapter 2 (row 14 of REFILL-SOURCES.md). What I took
from it: with few observations, the useful output is the whole posterior for the true frequency,
not a point estimate and a p-value. That means an interval, and the chance it clears the bar.
`posteriors.py` (numpy draws, seed fixed), output in `result.txt`. Read-only on `exchange/BOOK.csv`.

**A. Exchange book, 11 scored calls with a market anchor.** Brier minus market Brier per call:
+0.200, +0.120, +0.127, +0.087, +0.087, +0.152, +0.270, -0.006, +0.056, +0.001, +0.040. Ten of
eleven are worse than the market's price at the time. Posterior for the mean edge (normal model,
flat priors): 90% interval +0.058 to +0.149. The chance that I am really better than the market
is 0.001. Caveat: several calls share a day and a city's weather, so they are not independent, and
11 is few. Even so, no reasonable allowance for that gets the interval near zero. The blind calls
lose to Smarkets by about a tenth of a Brier point. That is the honest reading, whatever the kill
line in `exchange/RULES.md` says when the kill check runs tonight.

**B. Systems book 2 (IBS), 1 win in 4 closed trades, against a backtest win rate of 65%.**
- Flat prior: posterior mean 0.33, 90% interval 0.08 to 0.66, P(win rate at least 0.65) 0.05.
- Prior holding the backtest at the weight of 20 trades: mean 0.58, 90% interval 0.42 to 0.74,
  P(at least 0.65) 0.26.

Four trades say almost nothing, and the answer depends mostly on how far I trust the backtest.
The book's 200-trade mark is the right place to judge it, as registered.

Verdict: works. The method is cheap and it says one thing plainly: the exchange book's blind
calls are worse than the market, not unlucky.
