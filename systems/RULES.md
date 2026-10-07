# The systems book

Started 7 Oct 2026 (P-0083), after Luke asked why we had not found one strategy that holds. The
single survivor of P-0082 goes here and is paper-traded forward, where it cannot be fitted after the
fact. Paper only: no account, no stake (charter, execution ladder).

## Book 1: RSI(5) dip-buying inside an uptrend

**Markets, fixed before any of them was backtested for this book:** SPY, QQQ, DIA, IWM (US),
EFA (developed ex-US), EEM (emerging), EWU (UK), EWJ (Japan), EWG (Germany). All nine trade in New
York, so one close serves them all. None is dropped for doing badly; that is the point.

**Rules, per market**, on daily bars as traded (Yahoo chart endpoint, not dividend-adjusted):
- **Simple.** At the close: if flat, the close is above its 200-day average and RSI(5) (Wilder) is
  below 30, buy. If long and RSI(5) is above 50, sell.
- **Triple.** As simple, plus RSI(5) has fallen three sessions running and was below 60 three
  sessions ago. Larry Connors's version.

**Two fills per signal:**
- `close`: filled at the signal's own close, as the rule was tested. Idealised: a real order would
  have to go in a minute before the close on a price estimate.
- `next_open`: filled at the next session's open, which any order placed after the close gets.
  **This is the scored fill.**

**The record.** `systems.py update` runs in the nightly after the US close. It appends tonight's
indicator row per market to `SIGNALS.csv` and every signal and fill to `EVENTS.csv`. Nothing already
written is changed. The pre-registration commit lands before the next open (14:30 UK), so the
`next_open` fills are provably decided before they happen. The first close the book acts on is
6 Oct 2026, and it starts flat: positions the rules would have held before that do not count.

## What the backtest says to expect (2009 to 2026, `experiments/2026-10-07-P-0083/`)

Pooled across the nine markets, simple, next-open fills: about 56 trades a year, mean trade about
+0.6%, about three trades in four winners. Triple: about 27 a year, mean about +0.8%. Japan is the
weak market. The figures are total return; the live book ignores dividends, which costs a little.

## Pass marks, pre-registered 7 Oct 2026 before the first trade

Judged on **simple, next-open fills, all nine markets pooled**, closed trades only:

- **KILL** as soon as 30 or more trades have closed and the mean trade is below zero.
- **KEEP** at 60 closed trades if the mean is above zero and t (mean over its standard error) is at
  least 1.65.
- Between 60 and 100 with neither: keep running. **At 100**, KEEP if t is at least 1.65, otherwise
  KILL.
- Triple and the close fills are reported beside it and not judged.

Honest limits. Nine stock markets fall together, so trades cluster in the same weeks and the t
figure overstates certainty. If KEEP is reached I will also report the mean by calendar week. At the
backtest's mean and spread, 60 trades gives roughly an even chance of reaching t 1.65 even if the
edge is real. 100 trades gives about three in four. Expect about a year to 100.

`bin/killcheck.py` reads this book through `systems.verdict()` and says the word every night.

## Book 2: IBS while book 1 is flat (from P-0085 and P-0091)

Added 7 Oct 2026, before its first close (the 7 Oct session). Same nine markets, same data, same
append-only files. Its daily rows go to `SIGNALS_IBS.csv`, its events to `EVENTS.csv` under the
strategy name `ibs_gated`.

**Rule, per market.** At the close: IBS, meaning (close - low) / (high - low), is below 0.2, and
book 1's simple RSI(5) book is flat after that close's decisions (no position, nothing pending). If
both hold, buy the next open. If long and the close is above yesterday's high, sell the next open.
Once in, the trade runs to its own exit even if book 1 buys meanwhile. Next-open fills only.

**Backtest, 2009 to 2026** (`experiments/2026-10-07-P-0091/`): 3,943 trades, about 220 a year,
mean +0.27% before costs, 65% winners. Luck test pooled across the nine with one shared shuffle:
p = 0.044. The US markets carry it: SPY, DIA and IWM pass on their own, the overseas five do not.
The gate does not improve on plain IBS (p 0.026). It is kept because it is what passed the
pre-registered test, and it keeps the two books on different days.

**Pass marks, pre-registered 7 Oct 2026 before the first trade.** Judged on next-open fills, all
nine pooled, closed trades, **each trade less a 0.05% round-trip cost**. The per-trade edge is
small, so costs count here in a way they barely do for book 1.

- **KILL** as soon as 200 or more trades have closed and the mean after costs is below zero.
- **At 500 closed trades:** KEEP if the mean after costs is above zero and t is at least 1.65,
  otherwise KILL.

At the backtest's rate, 200 trades take about eleven months and 500 about two and a third years.
Why so many: at the backtest's mean after costs (+0.22%) and spread (about 2.4% a trade), 100
trades would give t of about 0.9 even if the edge is real, and 500 about 2.0, roughly a two-in-three
chance of KEEP. Fewer trades would be a coin toss dressed as a verdict. `systems.verdict2()` gives
the word every night through `bin/killcheck.py`.

## What this is not

It is not a route to the McLaren. At the backtest's numbers, money split evenly across the nine
markets earns low single digits a year, invested about an eighth of the time. If it is KEEP, the
question becomes what can be built on it (more markets, more strategies, the idle cash), not how
big to bet.
