# P-0089: two stricter luck tests for the RSI(5) systems book

Run 7 Oct 2026 23:54 BST, `p0089.py`, nine index ETFs from 2009 as traded. Designs fixed in the
docstring before the run; results in `results.json`. The in-sample column is P-0083's bar
permutation for the book's rule (simple, next-open fills).

The book's rule has no fitted parameter, so the thing that was optimised is the choice of rule
from a family. The walk-forward here re-makes that choice every year from 2012 on, picking the
best training profit factor among five dip-buying candidates (RSI(5) simple and triple, Williams
%R(7), stochastic, IBS), trades the pick out of sample, and permutes the whole series 1,000 times
with the selection re-run each time. The random-entry control keeps the book's trend filter and
exit (RSI(5) above 50, next open), draws the same number of entry days at random from sessions
above the 200-day average, 10,000 times, and asks how often random timing matches the real mean.

| market | in-sample p (P-0083) | walk-forward OOS bar PF | walk-forward p | real mean a trade | random median | random p |
|---|---|---|---|---|---|---|
| SPY | 0.041 | 1.37 | 0.085 | +0.63% | +0.19% | 0.0001 |
| QQQ | 0.088 | 1.32 | 0.13 | +0.86% | +0.28% | 0.0001 |
| DIA | 0.055 | 1.26 | 0.16 | +0.54% | +0.16% | 0.0002 |
| IWM | 0.24 | 1.58 | 0.001 | +0.77% | +0.22% | 0.0002 |
| EFA | 0.048 | 1.47 | 0.013 | +0.64% | +0.14% | 0.0002 |
| EEM | 0.076 | 1.05 | 0.51 | +0.60% | +0.17% | 0.002 |
| EWU | 0.12 | 1.48 | 0.010 | +0.52% | +0.11% | 0.003 |
| EWJ | 0.57 | 0.98 | 0.77 | +0.32% | +0.13% | 0.11 |
| EWG | 0.068 | 1.33 | 0.024 | +0.80% | +0.18% | 0.0002 |

## What it says

- **The dip timing is not random-entry luck.** In eight of nine markets fewer than 0.3% of 10,000
  random-timed books with the same filter, exit and trade count reach the real mean; the real
  trades earn three to five times the random median. Japan is the exception again (p 0.11), as
  it was the weakest market in P-0083.
- **Choosing the rule from a family costs about half the evidence.** Walked forward, the family's
  out-of-sample profit factor is 1.0 to 1.6 and only four of nine markets clear p 0.05 (IWM, EFA,
  EWU, EWG), against four of nine in sample for the book's rule itself (different four: SPY, DIA
  just, EFA, and none of the small ones). The picks were nearly always an RSI(5) variant, so the
  walk-forward is mostly the book's own rule out of sample with a yearly chance to swap.
- **What this does not do:** it does not test the exit, and the random control keeps the trend
  filter, so a "buy any day above the 200-day average" edge is inside the random median, not
  outside it. The book's pass marks (KILL at 30 if the mean is under zero, verdict at 60) stay
  as pre-registered; this run changes no rule.

A correction found on the way: my first pass counted the book's trade ids from 1993 in the 2009
denominator and understated the real mean by half; the bug was in this script, not the book.

## Verdict

**works**: the book survives a same-exit random-entry control in eight of nine markets at
p under 0.003, and the harder walk-forward selection test leaves four of nine standing with
Japan and emerging markets as the weak legs. In-sample p-values flattered the book by about
half; the forward record is still the test that counts.
