# P-0191: PACF of daily returns for the systems book's nine ETFs (Kaggle TS lesson 4)

Run 22 Oct 2026, 12:48, Trials slot. Called shot before running: works at 0.75, expecting lag 1
negative in 7 of 9 ETFs and about 1 lag per ETF outside the 95% band. Measured: **lag 1 negative
in 9 of 9, mean 1.0 lag per ETF outside the band**. Verdict hit; the lag-1 count was 9 not 7.

## Question

Kaggle's Time Series course, lesson 4, says the partial autocorrelation function picks which lags
are worth using as features. The systems book (RSI(5) simple and IBS below 0.2) bets on short-term
mean reversion in nine index ETFs, which needs the lag-1 partial autocorrelation of daily returns
to be negative. Is it, on the data the book actually trades on?

## Method

`pacf.py` imports `bars()` from `systems/systems.py`, so the data is exactly what the book sees:
Yahoo chart endpoint, 2y, daily, completed sessions only. Daily log returns, 500 per ETF (501
bars, 2024-10-23 to 2026-10-21). Autocorrelations to lag 10, PACF by Durbin-Levinson, band
+-1.96/sqrt(500) = 0.0877. Pure Python, no numpy or statsmodels.

## Numbers

| ETF | PACF lag 1 | lags outside 95% band |
|---|---|---|
| SPY | -0.095 | 1, 3, 4, 7 |
| QQQ | -0.072 | 4 |
| DIA | -0.036 | 3 |
| IWM | -0.074 | none |
| EFA | -0.062 | none |
| EEM | -0.074 | none |
| EWU | -0.052 | 3, 7 |
| EWJ | -0.060 | none |
| EWG | -0.039 | 3 |

- Lag 1 negative: 9 of 9, mean -0.063. Outside the band: 1 of 9 (SPY only).
- Lags outside the band: 9 across 9 ETFs, 1.0 per ETF, against a chance rate of 0.5 per ETF
  (10 lags at 5%). Pooled by lag: lag 3 in 4 ETFs, lag 4 in 2, lag 7 in 2, lag 1 in 1.

## Reading

- The direction the book bets on is there in every market, but it is small. A lag-1 partial
  autocorrelation of -0.06 explains 0.4% of next-day variance; the band test calls it noise in
  eight of nine. Nine negatives out of nine is not nine independent coins either: SPY, QQQ, DIA
  and IWM share most of their daily moves, and the four foreign ETFs trade in US hours against
  the same tape.
- Lesson 4's own tool, read straight, would pick lag 3 before lag 1 for this basket. Nothing in
  the book uses lag 3, and I have no story for it, so it is a candidate to re-test on an earlier
  window before it means anything.
- The RSI(5) and IBS rules do not act on lag 1 alone (five-day windows, intraday range), so this
  is a check of the premise, not a backtest of the rules; those have their own books.

## What I did not do

- No earlier window: 2y is what the book fetches. Whether lag 3 holds on 2022-24 is the deepen.
- No luck test beyond the 95% band and the chance rate; the nine series are not independent, so
  a pooled sign test would overstate it.

## Files

- `pacf.py` the script, re-runnable (fetches live, so the last bar moves).
- `results.json` every ETF's ACF lag 1, PACF lags 1-10 and the summary.
