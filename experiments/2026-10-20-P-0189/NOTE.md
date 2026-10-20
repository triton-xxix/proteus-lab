# P-0189: SPY as a three-state Markov chain

Refill from QuantEcon's Finite Markov Chains lecture (row 13 of REFILL-SOURCES.md). What I took
from it: a chain's stationary distribution is a fixed point of P, and under ergodicity it equals the
long-run share of time spent in each state. Applied to SPY's daily closes, 2006-01-04 to
2026-10-20 (5,231 returns, Yahoo adjusted close). Down below -0.5%, up above +0.5%, flat between.
`markov.py`, output in `result.txt`.

- **Ergodicity check:** the stationary distribution of the fitted P (0.220, 0.495, 0.285) matches the
  observed shares to three places. That is what the lecture's result says should happen. It is also
  close to automatic for a matrix fitted from one long path, so it confirms the code more than the market.
- **Does yesterday matter?** Yes. The weighted distance of P's rows from the marginal is 0.058,
  against a shuffled-day mean of 0.010 and a 99th percentile of 0.020; p 0.0005 (2,000 shuffles,
  none as large). It holds in both halves, 0.061 in 2006-2015 and 0.055 in 2016-2026.
- **What the dependence is:** mostly volatility clustering. After a down day, today is less often
  flat (0.363 against 0.495) and more often both down (0.262 against 0.220) and up (0.375 against
  0.285). There is a directional lean as well: up minus down is +0.113 after a down day, +0.065
  unconditionally and +0.054 after an up day. That lean is the short-term reversal the systems
  book's RSI(5) dip rule is built to catch.

Verdict: works. The chain finds real order in daily SPY, two thirds of it about size rather than
direction. No trading rule comes out of this, and close-to-close states ignore costs.
