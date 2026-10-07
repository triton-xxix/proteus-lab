# P-0088: Kaufman's efficiency ratio on the 28-ETF trend portfolio

Run 7 Oct 2026 23:50 BST, `p0088.py` on P-0084's harness, 28 ETFs, evaluation from 2008-05-01 to
2026-10-07. Definitions fixed in the docstring before the run; results in `results.json`.

## Which markets trend (one-year efficiency ratio, mean over the span, in-sample)

Top: HYG 0.096, QQQ 0.096, SPY 0.094, LQD 0.085, TIP 0.078, DBC 0.078, UNG 0.077, IEF 0.075.
Bottom: FXA 0.060, TLT 0.058, EWZ 0.057, FXC 0.053, FXI 0.051. By class: the ranking puts credit
and US equities at the top and currencies and emerging equities at the bottom. All the numbers
are small: a year of SPY covers about a tenth of the path it walked.

## Does picking the trendiest half help?

Selection at each 5-day rebalance by the trailing two-year mean ER, past data only, 14 of 28,
12-month time-series momentum on the chosen markets, same sizing and costs as P-0084.

| portfolio | CAGR | vol | Sharpe | max drawdown | joint-shuffle p (500) |
|---|---|---|---|---|---|
| all 28 | 4.2% | 15.3% | 0.35 | 35% | 0.16 |
| trendiest 14 | 2.5% | 16.6% | 0.23 | 44% | 0.34 |
| least trendy 14 (control) | 4.7% | 16.8% | 0.36 | 36% | 0.11 |

Top minus bottom Sharpe: -0.13, and 77% of the joint shuffles produced a gap at least that large,
so the sign is not even reliable. The efficiency ratio ranks markets by how smooth their recent
year was, and that smoothness does not carry forward into the next year's momentum profit.
Picking the trendiest half costs about 1.7 points of CAGR and 9 points of drawdown.

## A number that moved

The all-28 baseline here has Sharpe 0.35 where P-0084 recorded 0.28 on the same code earlier the
same day. My first guess, a refetched price cache, is wrong: the CSVs under `sandbox/p0082/data/`
are dated 02:23 and 03:11 and P-0084's results 03:16, so both runs read the same files. The gap is
unexplained tonight. The likely cause is an edit to `p0084.py` after its results were written (its
docstring records a fix to the shuffle offset); the committed script, run again, gives 0.35. The
comparison inside this run is on one series and one script and stands. P-0084's headline Sharpe
should be re-read from a fresh run before it is quoted again.

## Verdict

**not worth it** as a selection rule: trendiest-half picking is worse than all 28 and worse than its
own control, under the same shuffle. The ranking itself is the artefact. Nothing queued.
