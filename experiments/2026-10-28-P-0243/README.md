# P-0243: does the RSI(5) book only pay when VIX is high?

**Question.** Split the systems book's RSI(5) simple rule by the VIX close on the signal day and test each
tercile against a random-entry control from the same tercile.

**Rules, fixed before the run** (the book's own, from `experiments/2026-10-07-P-0083/basket_backtest.py`):
close above its 200-day average and RSI(5) Wilder under 30 at the close; buy the next open; exit at the
next open after RSI(5) closes above 50. Nine ETFs (SPY QQQ DIA IWM EFA EEM EWU EWJ EWG), 2009 on,
total-return scaled Yahoo OHLC from `sandbox/p0082/data`, no costs. VIX: FRED VIXCLS (keyless), terciles
15.2 and 20.7 taken from the whole 1990-2026 history (named in the probe title before the run).

**Called shot.** works at 0.85: high tercile at least 2x the low, and only the high tercile beats its
control at p under 0.05. First half hit (5.3x). Second half missed: the mid tercile beats its control
hardest.

**Control.** Random signal days from the same symbols, same tercile, same 200-day filter; next-open entry;
hold length drawn from that tercile's real trades; exit at an open. 2000 draws of the tercile's trade count.

**Numbers** (trades, mean per trade, win rate, control mean, excess, p):

| VIX on signal day | trades | mean | win | control | excess | p |
|---|---|---|---|---|---|---|
| under 15.2 | 201 | +0.17% | 69% | +0.05% | +0.12% | 0.187 |
| 15.2 to 20.7 | 453 | +0.68% | 75% | +0.17% | +0.52% | 0.000 |
| 20.7 and over | 312 | +0.92% | 80% | +0.59% | +0.33% | 0.024 |

Pooled 966 trades at +0.65%, against the book's +0.63% backtest: replicates. A first run without the
200-day filter on the control gave the same picture (p 0.151, 0.000, 0.043).

**Reading.** Raw return rises with VIX, but so does the return of a random long on a filtered day: after a
high-VIX close, almost anything bought earns +0.59% over five days. The signal's own edge is largest in the
middle tercile. In calm markets (VIX under 15) the rule earns little and does not beat luck. So: not
"only when VIX is high", but "not when VIX is low".

**What I did not do.** No neurotrader bar-shuffle permutation per tercile (the book's whole-sample test
already passed it, P-0089). 2000 draws, not the retired skill's 10,000. No walk-forward of the terciles
(they use full-history VIX, a mild look-ahead on the cut points). No holding comparison per tercile beyond
the control. No costs: at the low tercile's +0.17% a round trip of 0.05 to 0.1% eats half of it.
