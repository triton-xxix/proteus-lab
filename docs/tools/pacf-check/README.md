# pacf_check.py

Is that lag in your daily returns real, or one window's noise? One file, standard library only.

```
python3 pacf_check.py prices.csv --split 2024-10-23
python3 pacf_check.py --yahoo SPY QQQ EWU --start 2022-10-23 --split 2024-10-23
python3 pacf_check.py a.csv b.csv --split 2024-10-23 --lags 10 --json out.json
```

A CSV needs a date column and a close column; `adjclose` is used when present. `--yahoo` pulls five
years of daily bars from Yahoo's chart endpoint, no key. `--start` and `--end` trim the first and
second window; `--end` is the day after the last date kept.

## What it does

Daily log returns in each window, autocorrelation, then partial autocorrelation by Durbin-Levinson,
lags 1 to `--lags`. The band is the usual 95% one, ±1.96/√n. For each series it prints both windows
with a star on every lag outside the band, then the lags outside in both windows and the lags
outside in one only. With several series it prints a pooled count per lag.

A lag outside in one window only is the common case and is not evidence of anything: with ten lags
about one series in two shows one by chance. Correlated markets (SPY, DIA, QQQ) share their dips, so
"4 of 9" is closer to one coincidence than four.

## Checked against the probe

P-0193 (22 Oct 2026) ran the same arithmetic in `experiments/2026-10-22-P-0193/pacf_oos.py`. This
script, run the same afternoon on fresh Yahoo bars with `--start 2022-10-23 --split 2024-10-23
--end 2026-10-22`, gave all 180 PACF values (9 ETFs, 10 lags, 2 windows) and every band flag the
same. The run is kept in `check-2026-10-22.json` and `build.py` exits if the two disagree.

What it found: lag 3 outside the band in 4 of 9 ETFs in 2024-26 and 0 of 9 in 2022-24, lag 6 the
other way round, and no ETF with any lag outside in both windows. Lag 1 stayed negative (9 of 9,
then 7 of 9) but small.

Not advice.
