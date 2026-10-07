# P-0085: the dip-buying family, one edge or several?

Run 7 Oct 2026, interactive, at Luke's request ("run P-0085 now"). Five rules from Quantified
Strategies videos, read by the 7 Oct reader (TRADING-IDEAS.md). Each was replicated on SPY,
luck-tested, run on the nine-ETF basket, and measured against the RSI(5) systems book. Reader A had
warned the five might be one trade seen five ways, and that is what this probe checks.

Rules as the videos give them: Williams %R(7) below -95; slow stochastic (7,3) below 25; internal
bar strength (IBS) below 0.2, a threshold the video does not state, so I fixed it before running;
SPY down 5% in 5 days; three lower closes. The first three buy the next open and sell the next open
after a close above yesterday's high. The last two hold 5 and 3 sessions. No trend filter, no costs.
Data as traded, which is what the channel uses (P-0082). Declared before the full run and added
after the smoke run: each rule again with RSI(5)'s 200-day filter (the `_trend` rows), and no
re-entry on the bar of a close exit, which their identical stochastic trade counts require.

## 1. Replication: their numbers come out again

| Rule (SPY, 1993 to 2026) | Theirs | Mine |
|---|---|---|
| Williams %R(7) | 288 trades, 76.4% win, avg 0.82%, PF 2.61 | 289, 76.5%, 0.82%, 2.63 |
| Stochastic, next-open fills | 394, 73.6%, 0.65%, 2.47 | 394, 72.8%, 0.68%, 2.54 |
| Stochastic, close fills | 394, 77.7%, 0.68%, 2.58 | 394, 77.4%, 0.72%, 2.69 |
| SPY down 5% in 5 days | 81 cases, +1.24% vs +0.20% any 5 days | 82, +1.15% vs +0.197% |
| Three lower closes | 459 cases, +0.23% vs +0.12% any 3 days | 460, +0.18% vs +0.119% |
| IBS | 631 trades, PF 2.12, threshold unstated | 911 at 0.2 (PF 1.85); 639 at 0.1 |

Their IBS threshold was probably 0.1. My drawdowns are marked to market daily and run higher than
theirs. That makes Quantified Strategies 5 for 5 on rules they publish, and 8 for 8 since P-0082.

## 2. Luck test (1,000 shuffles on SPY; 500 per basket market)

| Rule | Makes money (avg trade) | p, SPY since 1993 | p, SPY since 2009 | Basket since 2009: markets p < 0.05 | Pooled basket avg trade |
|---|---|---|---|---|---|
| Williams %R(7) | yes, 0.82% | 0.001 | 0.086 | 0 of 9 | +0.34% (1,300 trades) |
| Stochastic | yes, 0.68% | 0.001 | 0.049 | 1 of 9 | +0.27% (2,148) |
| IBS < 0.2 | yes, 0.41% | 0.001 | 0.021 | **4 of 9** (SPY, QQQ, DIA, IWM) | +0.27% (4,431) |
| Down 5% in 5 days | yes, 1.15% | 0.118 | 0.52 | 0 of 9 | +0.89% (529) |
| Three lower closes | barely, 0.18% | 0.217 | 0.42 | 0 of 9 | +0.07% (2,108) |
| *RSI(5), for reference (P-0082, P-0083)* | *0.96%* | *0.001* | *0.037* | *4 of 9 on either fill* | *+0.64% (970)* |

With the 200-day filter: Williams %R 155 trades, profit factor 3.2, p 0.001 then 0.133. Stochastic
243, 2.86, p 0.001 then 0.059. IBS 631, 2.01, p 0.001 then 0.075. The filter improves trade quality
and halves the drawdown, but the post-2009 p-values get worse because trades fall away.

The two "famous rules", down 5% in 5 days and three lower closes, do not beat luck even on SPY's
full history.

## 3. Is it one edge? Mostly yes

Share of each rule's basket trades (2009 on) that overlap an RSI(5) trade in time:

| Rule | No filter | With the 200-day filter |
|---|---|---|
| Williams %R(7) | 46% | 80% |
| Stochastic | 48% | 75% |
| IBS | 23% | 33% |
| Down 5% in 5 days | 34% | 97% |
| Three lower closes | 37% | 53% |

Add RSI(5)'s trend filter and the family collapses into RSI(5): three quarters or more of the
trades are the same. Without the filter they are weaker per trade than RSI(5) on the basket, at
0.27% to 0.34% against 0.64%. So the systems book already holds this edge, and none of these
belongs beside it.

## 4. The exception: IBS

IBS overlaps least (23%). It passes the luck test in all four US markets, and its trades split
sharply by whether RSI(5) was already in:

| IBS trades, basket since 2009 | Trades | Average |
|---|---|---|
| While an RSI(5) trade is open | 1,036 | **-0.49%** |
| With no RSI(5) trade open | 3,395 | **+0.51%** |

Buying a weak close inside a sell-off that RSI(5) is already holding loses. Buying a weak close in
a calm market makes about half a percent. Caveat: "open" here uses RSI(5)'s position over the
whole IBS trade, which is hindsight. The rule a trader could follow is "IBS only when the RSI(5)
book is flat at the signal close". That needs its own luck test, queued as P-0091. If it passes,
it is the candidate for a second systems book, because it trades on different days from the first.

## Caveats

About 110 luck tests ran here, so a few p-values under 0.05 are expected by chance. The pattern
counts more than any one number: four of four US markets for IBS, none of nine for most of the
others. No costs: on SPY, at 0.03% a round trip, they matter little against a 0.3% to 0.8% trade.
On the smaller ETFs they would matter more.

## Reproduce

```
/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0085/p0085.py
```
About two minutes. Imports P-0082's engine and P-0083's RSI(5) reference. Results in `results.json`.
