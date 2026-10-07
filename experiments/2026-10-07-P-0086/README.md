# P-0086: the Darvas box breakout on SPY (Quantified Strategies, A-01)

Run 7 Oct 2026 23:58 BST, `p0086.py` on `sandbox/py312-venv`, data Yahoo daily as traded (not
dividend-adjusted, the channel's convention), SPY 1993-01-29 to 2026-10-07. Rules fixed in the
script's docstring before the run. Results in `results.json`.

## Does it replicate?

| | claimed | vol average excl. signal day | vol average incl. signal day |
|---|---|---|---|
| trades | 279 | 277 | 282 |
| winners | 74.2% | 71.5% | 73.0% |
| avg trade | +0.34% | +0.28% | +0.31% |
| profit factor | 3.08 | 2.34 | 2.61 |
| era PF 1993-2004 / 2005-2015 / 2016-2026 | 2.70 / 2.78 / 3.94 | 1.71 / 2.43 / 3.56 | 1.77 / 3.23 / 3.93 |

The trade count replicates to within five either way. The profit factor does not: 2.3 to 2.6
against 3.08, and the first era is far weaker than claimed (1.7 against 2.7). Their lookback
sweep does not reproduce either: here 16 days is the best of the six (2.61), 12 days the second
worst (2.34), where they have 12 best at 3.08. Data vendor and the unstated volume convention
could explain some of the gap; not all of it.

## Is it luck?

Bar permutation with volume carried on the same shuffle, 1000 draws: p 0.011 on the full sample,
p 0.014 from 2009. So the rule beats shuffled SPY bars. Random entries with the same exit and
the same trade count (500 draws): the real profit factor beats 97% of them, but the real average
trade (+0.28%) beats only 60% of them (random median +0.25%). The exit, sell the open after a close
above the prior high, does most of the work, as reader A's red flag said. Without the chase cap
and volume filter the plain 12-day-high entry makes 686 trades at +0.13% and PF 1.38.

## Does it travel?

Nine index ETFs from 2009, same rule: SPY +0.36% a trade (p 0.01) and nothing else passes. QQQ
+0.24% (p 0.27), DIA +0.20%, EWU +0.14%, the rest within a tenth of zero, IWM and EEM negative.
Pooled 1,209 trades, +0.11%, 64% winners, 1 of 9 markets under p 0.05, 6 of 9 positive.

## Verdict

**works**, as a replication: the trade count is right and the SPY edge survives the shuffle. Not a
systems-book candidate: the profit factor is a third below the claim, the edge is SPY only, and the
same exit from random days earns almost the same per trade. Nothing queued.
