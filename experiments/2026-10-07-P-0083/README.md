# P-0083: paper-tracking the one strategy that survived P-0082

Run 7 Oct 2026, interactive, at Luke's request ("run P-0083 now"). The probe asked for a forward
paper-track of RSI(5) dip-buying on SPY. It became a standing book, `systems/`, because a forward
test is not something one night can finish.

## The problem with SPY alone

On SPY the rule trades about seven times a year (118 trades from 2009 to 2026). Twenty trades
would take three years and prove little. So before running anything I fixed a basket of nine broad
stock-index ETFs: SPY, QQQ, DIA, IWM, EFA, EEM, EWU, EWJ, EWG. All nine are tracked whatever their
backtest says. Choosing markets after seeing which ones worked would be the same data-mining
P-0082 was built to catch.

## Baseline: the basket, 2009 to 2026 (`basket_backtest.py`, `basket_backtest.json`)

Simple rule, per market, with neurotrader's permutation test (1,000 shuffles from 2009):

| Market | Trades | Avg trade, close fill | Avg trade, next-open fill | Win (next open) | p, close | p, next open |
|---|---|---|---|---|---|---|
| SPY | 118 | 0.80% | 0.78% | 78% | 0.029 | 0.041 |
| QQQ | 127 | 0.83% | 0.87% | 80% | 0.092 | 0.088 |
| DIA | 125 | 0.65% | 0.63% | 77% | 0.045 | 0.055 |
| IWM | 110 | 0.52% | 0.64% | 76% | 0.344 | 0.239 |
| EFA | 103 | 0.65% | 0.67% | 75% | 0.053 | 0.048 |
| EEM | 104 | 0.92% | 0.67% | 75% | 0.016 | 0.076 |
| EWU | 97 | 0.68% | 0.52% | 69% | 0.039 | 0.116 |
| EWJ | 88 | 0.34% | 0.14% | 70% | 0.376 | 0.569 |
| EWG | 98 | 0.65% | 0.73% | 71% | 0.104 | 0.068 |

Pooled: 970 trades, about 55 a year. Next-open fills: mean +0.64% a trade, 75% winners. Close
fills: +0.68%, 78%. The triple version: 465 trades, about 26 a year, mean +0.84% at the next open.
Every market made money on average. Japan is the weak one. Four of nine pass p < 0.05 on one fill
or the other, and most of the rest sit between 0.05 and 0.12. Each market alone is about 100
trades, which is thin for one market and the reason to pool.

## The book

- `systems/RULES.md`: rules, the two fills, and pass marks written before the first trade. KILL if
  the mean next-open trade is below zero once 30 have closed. KEEP at 60 if the mean is above zero
  and t is at least 1.65. Otherwise run to 100 and decide there.
- `systems/systems.py update`: nightly after the US close. Append-only `SIGNALS.csv` (one row per
  market per day) and `EVENTS.csv` (signals and fills). The nightly's pre-registration commit lands
  before the 14:30 UK open, so the next-open fills are decided before they happen.
- `systems.py score` and `bin/killcheck.py` say the word every night. `bin/preregister.py` now
  commits `systems/`. The nightly SKILL has the step, and the live scheduled task was reloaded to
  match the repo (diffed identical).

**First night:** the 6 Oct close. No market signalled. Most are well above their lows: RSI(5) runs
from 39 (EWU) to 85 (QQQ). Every book is flat. EWU and EWG closed under their 200-day average, so
they cannot signal until they recover.

## Checked before it went live

I replayed the tracker from November 2025 against the backtest on SPY, IWM, EWJ and EWG. SPY,
IWM and EWJ matched trade for trade on both fills. EWG differed only by a trade already open when
the replay began. The replay also exposed a bug in P-0082's trade counting: an unchanged close
split one trade into two. It is fixed, and corrected in that report. The p-values were untouched.

## What to expect, honestly

At the backtest's rate, 30 closed trades takes about six months and 60 about a year. The edge, if
it holds, is small: about +0.6% a trade. Money split nine ways across the markets, invested about an
eighth of the time, comes to low single digits a year. This book answers "is there a real edge we
can hold to", not "is this how we get to £146,500".
