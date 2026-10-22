# P-0193: P-0191 out of sample, the prior two-year window

Run 22 Oct 2026, 13:00, Trials slot. Called shot before running: works at 0.75, expecting lag 3
outside the band in 1 of 9 (it does not hold) and lag 1 negative in 6 of 9. Measured: **lag 3
outside in 0 of 9, lag 1 negative in 7 of 9**. Verdict hit, both numbers within one.

## Question

P-0191 found, on the live 2y window, lag 3 of the daily-return PACF outside the 95% band in 4 of
9 index ETFs and lag 1 negative in 9 of 9. Does either survive on the two years before it?

## Method

`pacf_oos.py` pulls Yahoo's chart endpoint with range=5y (the only change from
`systems.bars()`), splits at 2024-10-23, and runs the same Durbin-Levinson PACF on daily log
returns for both windows: prior 2022-10-23 to 2024-10-22 (501 returns), live 2024-10-23 to
2026-10-21 (500 returns). Band +-1.96/sqrt(n) = 0.0876. The live window reproduces P-0191's
numbers from the same pull (lag 1 negative 9 of 9, lag 3 outside 4 of 9), so the split is right.

## Numbers

| ETF | prior PACF 1 | prior PACF 3 | prior lags outside | live PACF 1 | live lags outside |
|---|---|---|---|---|---|
| SPY | -0.006 | -0.025 | none | -0.095 | 1, 3, 4, 7 |
| QQQ | +0.006 | -0.022 | none | -0.071 | 4 |
| DIA | +0.009 | -0.043 | none | -0.037 | 3 |
| IWM | -0.004 | +0.028 | none | -0.074 | none |
| EFA | -0.041 | +0.020 | 6 | -0.061 | none |
| EEM | -0.048 | +0.044 | 6 | -0.074 | none |
| EWU | -0.087 | +0.007 | 6 | -0.051 | 3, 7 |
| EWJ | -0.041 | +0.024 | none | -0.058 | none |
| EWG | -0.022 | +0.049 | 6 | -0.038 | 3 |

| | prior 2022-24 | live 2024-26 |
|---|---|---|
| lag 1 negative | 7 of 9 (mean -0.026) | 9 of 9 (mean -0.062) |
| lag 1 outside band | 0 of 9 | 1 of 9 |
| lag 3 outside band | 0 of 9 (mean +0.009) | 4 of 9 (mean -0.067) |
| lags outside per ETF | 0.44 (chance 0.5) | 1.0 |
| the lag that lights up | lag 6 in 4 of 9 (EFA, EEM, EWU, EWG) | lag 3 in 4 of 9 |

## Reading

- Lag 3 was a one-window artefact. Its mean PACF flipped sign between windows and no ETF kept
  it. The prior window has its own "4 of 9" lag (lag 6, in the four non-US ETFs, which share a
  tape), which the live window does not have. With nine correlated series, one lag showing up in
  four of them is what a single window produces by itself. That is the lesson against reading
  lesson 4's plot straight on a basket of near-duplicates.
- Lag 1 is the more stable thing: negative in 7 of 9 then 9 of 9, but the prior window's mean
  is -0.026, inside the band everywhere, and the four US ETFs sit at zero in 2022-24. The
  mean-reversion premise behind RSI(5) and IBS is present but weak and not constant; it was
  stronger in 2024-26 than 2022-24. Whether that is regime or noise needs more windows than two.
- Nothing here changes the systems book's pre-registered marks; it is a check of the premise.

## What I did not do

- Only two windows. A rolling one-year PACF of lag 1 across the whole 5y pull would show
  whether 2024-26 is a run or a level; not done, 20 minutes was the estimate.
- No test of the four US ETFs as one series (they are near-duplicates), which would halve the
  effective count.

## Files

- `pacf_oos.py` the script, re-runnable (fetches live, so the live window's last bar moves).
- `results.json` both windows, every ETF, PACF lags 1-10.
