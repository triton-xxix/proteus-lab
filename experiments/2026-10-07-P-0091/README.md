# P-0091: IBS as a second systems book, the rule you could actually trade

Run 7 Oct 2026, interactive, at Luke's request ("run P-0091 now"). P-0085 found that IBS trades
average +0.51% when no RSI(5) trade overlaps them and -0.49% when one does. That split used
hindsight: it looked at RSI(5)'s position across the whole IBS trade. This probe tests what a trader
could actually do. Take IBS below 0.2 only when the RSI(5) book is flat at that close. The script and
the pass mark were committed before the first run (6653a42).

## Result

| Nine-ETF basket, 2009 to 2026, next-open fills | Trades | Per year | Avg trade | Win | Luck test, pooled |
|---|---|---|---|---|---|
| RSI(5), book 1 | 931 | 52 | +0.64% | 75% | p = 0.011 |
| IBS, gated by book 1 being flat | 3,943 | 222 | +0.27% | 65% | **p = 0.044** |
| IBS, no gate | 4,431 | 250 | +0.27% | 65% | p = 0.026 |

The pooled luck test uses one shuffle for all nine markets (dates aligned), so dips still arrive
together, as they do in reality. 1,000 shuffles.

**Pass mark** (fixed in advance: pooled p < 0.05, mean > 0, positive in 5 of 9): **passes**. p is
0.044, the mean is positive, and all nine markets are positive.

**By market** (gated IBS): SPY +0.40% a trade (p 0.020), DIA +0.37% (0.033), IWM +0.45% (0.016),
QQQ +0.46% (0.12). EFA, EEM, EWU, EWJ and EWG all average +0.09% to +0.21% with p between 0.12 and
0.56. **It is a US effect.**

## What P-0085 got wrong

The gate changes almost nothing. Gated and ungated IBS both average +0.27%. P-0085's +0.51% came
from leaving out IBS trades that started before RSI(5) bought. Those are the losers: IBS buys the
first weak close, the dip deepens, RSI(5) joins in. Nobody can know at the time that the dip will
deepen. So the real-time edge is half what the hindsight split showed. That is why this probe was
run instead of trusting it.

## As a portfolio (1/9 of capital a market; "both" splits each slice half and half)

| | Yearly return | Volatility | Sharpe | Worst drawdown | Time in market |
|---|---|---|---|---|---|
| RSI(5) alone | 3.8% | 5.5% | 0.71 | 11.3% | 15% |
| Gated IBS alone | 6.5% | 10.6% | 0.65 | 24.7% | 44% |
| Both | 5.3% | 7.0% | **0.77** | 17.7% | |
| SPY, price only | 12.7% | 17.8% | 0.76 | 34.1% | 100% |

The two books' daily returns correlate at 0.46. Together they have the best Sharpe of anything we
have tested, a little above SPY, with half its drawdown. That is still well under half its return.
Before costs.

## Decision

The pass mark was met, so it becomes **book 2** of the systems book (`systems/RULES.md`), from the
7 Oct close. The marks are set for a small edge: judged after a 0.05% cost per round trip, KILL if the
mean is below zero once 200 trades have closed, and the verdict at 500. About 220 trades a year makes
that roughly eleven months and two and a third years. The tracker's replay from November 2025
matched this backtest trade for trade, apart from the trade already open when the replay began.

## Caveats

p = 0.044 after a night of more than 150 luck tests is weak evidence on its own. The forward book is
the real test. Costs are left out of the backtest. At about 0.3% a trade, 0.05% a round trip takes
roughly a fifth of it, which is why book 2 is judged after costs.

## Reproduce

```
/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0091/p0091.py
```
About two minutes. Results in `results.json`.
