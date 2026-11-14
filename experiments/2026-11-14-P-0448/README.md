# P-0448: RSI(5) hold length and a time stop, 2009 to 2026

**Question.** Refill 169 saw the systems book's three live trades held 4 sessions or fewer average +0.82%
gross and the five held 8 or more average -0.81%. In the backtest, what is the mean by hold length, and
would a 5-session time stop have helped?

**Rules (written before the run).** Book 1 as registered: close above SMA200 and Wilder RSI(5) under 30 ->
buy next open; RSI(5) over 50 at a close -> sell next open. Nine ETFs (SPY QQQ DIA IWM EFA EEM EWU EWJ
EWG), price-only Yahoo daily bars cached in `sandbox/p0082/data/` (to 6 Oct 2026), entries from 2 Jan 2009,
gross open to open, no costs. Time stop T: also sell at the next open after the T-th close in the trade.
Luck tests: a sign-flip permutation on the per-trade paired difference (stop minus base, same entries,
10,000), and a random-entry control for the stopped rule (same SMA200 filter, same exits, same trade count
per ETF, 500 draws). Script `timestop.py`.

**Called shot.** works at 0.8: the stop moves the mean by about -0.05 points (no help), win rate 75% to
about 70%.

## Numbers

Replication: 927 trades, mean +0.651%, win 74.9%, against the book's quoted +0.63% and 75%.

| hold (sessions) | trades | mean | win |
|---|---|---|---|
| 1 to 3 | 361 | +1.53% | 94% |
| 4 to 5 | 212 | +1.48% | 92% |
| 6 to 9 | 240 | +0.26% | 60% |
| 10+ | 114 | -2.83% | 13% |

| rule | trades | mean | win | sum of trade % |
|---|---|---|---|---|
| RSI exit only (book 1) | 927 | +0.651% | 74.9% | +603 |
| + 3-session stop | 1192 | +0.294% | 61.2% | +350 |
| + 5-session stop | 1038 | +0.452% | 67.9% | +469 |
| + 7-session stop | 974 | +0.480% | 71.6% | +468 |

- Paired, same 927 entries: the 5-session stop changes 353 trades, by -0.61 points each on average, -0.23
  per trade overall. Sign-flip p that the stop is better: 1.0.
- The stopped rule still beats random entries above SMA200 with the same exits (random mean +0.10%, p 0.002),
  so the signal survives, the stop just costs.

## What it means

The live pattern is the backtest's pattern: short holds win, long holds lose, by construction, because a
trade that bounces exits fast. Cutting the long holds early is worse, not better: a trade still open at
session 5 is down, and waiting for RSI over 50 recovers more of it than selling there. Every stop length I
tried lowered both the mean and the total. The live book's 3 of 8 winners is not a sign the exit is wrong.

## What I did not do

- No costs (they would hurt the stop rules more, since they trade more).
- No drawdown or time-in-market comparison; a stop frees capital sooner, which is not valued here.
- Price-only bars, no dividends, as the book itself trades.
