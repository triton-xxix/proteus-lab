# P-0253: should the RSI(5) book skip VIX backwardation?

**Question.** Deepen of P-0252. Skip any RSI(5) signal when VIX/VIX3M on the signal day is at or above 1.
Does the skip book beat the full book per trade in both halves (entries 2009-17 and 2018-26), after a 0.1%
round trip per trade?

**Rules.** The book's own (P-0243, P-0252), nine ETFs, next-open fills, cut at 1 from the title. Halves by
entry date, cut 1 Jan 2018 fixed in the title.

**Called shot.** works at 0.65, "skip beats full after costs in both halves, by at least 0.05 points a
trade in each". Shot after seeing P-0252's pooled split, so only the halves were blind. Missed by a hair:
2018-26 gained 0.049.

**Numbers** (net of 0.1% a trade):

| half | full trades | full mean | skip trades | skip mean | skipped trades | skipped mean | skip minus full | full sum | skip sum |
|---|---|---|---|---|---|---|---|---|---|
| 2009-17 | 499 | +0.66% | 413 | +0.76% | 86 | +0.19% | +0.10 | +330% | +314% |
| 2018-26 | 467 | +0.44% | 389 | +0.49% | 78 | +0.20% | +0.05 | +205% | +190% |

**Reading.** The skip lifts mean per trade in both halves, but the skipped trades still make about +0.2%
after costs in both halves, so the summed return falls in both (by 16 and 15 points). P-0252 showed those
trades lose to a random long in the same state; they do not lose money. For a book that is never capital
constrained (one unit per signal, as now), skipping them costs return. It would only pay if the slot were
needed for something better, such as a random long, which P-0252 says earns +0.86% in that state.

**What I did not do.** Summed returns are a sum of per-trade percentages, not a compounded equity curve
with overlapping positions. No significance test of the 0.05 and 0.10 differences. Not changing the
systems book: its rules are pre-registered and this is a backtest.
