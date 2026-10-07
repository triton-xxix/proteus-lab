# P-0084: trend following as a 28-market portfolio

Run 7 Oct 2026, interactive, at Luke's request ("run P-0084 now"). This is the fair version of the
golden cross test from P-0082. Trend followers do not trade one market; they run one portfolio across
many, sized so each market carries the same risk. The script, with every parameter fixed, was
committed before the first run (d9ae84e). One fix came after that commit and before any result: the
luck test's warm-up offset went negative and broke the index. It is clamped to 0, so the whole series
is shuffled. Nothing else changed.

## Set-up

- **28 ETFs**, all trading since April 2007. Equities: SPY QQQ IWM EFA EEM EWJ EWU EWG EWZ FXI VNQ.
  Bonds: TLT IEF LQD HYG TIP. Commodities: GLD SLV USO UNG DBA DBC. Currencies: FXE FXY FXB FXA FXC UUP.
  Daily closes, total return, keyless from Yahoo.
- **Signal A (primary):** 12-month time-series momentum, long if the past year was up, short if
  down. **Signal B:** 100-day breakout, flipping on a new 100-day high or low.
- **Sizing:** each market at 40% annualised volatility on its last 60 days, divided by 28, gross
  capped at 3x (average gross used: 2.8x). Rebalanced weekly; 5 basis points cost per unit traded.
- **Scored from May 2008 to 6 Oct 2026.** Luck test: whole days shuffled across all 28 markets
  together, which keeps their correlations and destroys every trend. 1,000 shuffles, scored on Sharpe.

## Results

| | Growth | CAGR | Volatility | Sharpe | Worst drawdown |
|---|---|---|---|---|---|
| 12-month trend | 1.78x | 3.2% | 15.3% | 0.28 | 35% |
| 100-day breakout | 2.11x | 4.1% | 16.0% | 0.33 | 40% |
| 60/40 (SPY/IEF) | 4.63x | 8.7% | 11.4% | 0.79 | 31% |
| SPY | 7.89x | 11.9% | 19.7% | 0.67 | 51% |
| Half 60/40, half trend | 3.15x | 6.4% | 9.0% | 0.74 | **15%** |

| Question | 12-month trend | 100-day breakout |
|---|---|---|
| Makes money? | Yes, modestly | Yes, modestly |
| Beats holding? | No on return; halves the 60/40's drawdown as an add-on | No on return |
| Beats luck? | No, p = 0.15 | Close, p = 0.086 |

- **It pays when the market doesn't.** Correlation with 60/40 is -0.11 (trend) and -0.21
  (breakout). In 2022 the trend portfolio made +18.9% and the breakout +22.1% while 60/40 lost 16.4%.
  It also made money from May 2008 (+6.0%, breakout +21.6%).
- **It has bad years:** 2009 -19% (the rebound reversed every short), 2016 -21%, 2018 -13%, 2023 -13%.
- **By asset class** (Sharpe, trend signal on that class alone): bonds 0.39, commodities 0.29,
  equities 0.25, currencies -0.16.
- **By period:** 2008 to 2016, Sharpe 0.13. 2017 to 2026, Sharpe 0.46.
- These numbers follow the shape the trend-fund industry is known for: a hard decade after
  2009, then a strong 2022. So the set-up behaves like the real thing. I have not checked it against
  a published index figure.

## What it means

- **Not a money-maker on its own, at this scale.** A 3% to 4% CAGR with a 35% to 40% drawdown is
  worse than holding 60/40 on every measure but one.
- **That one measure is the real use.** Half 60/40 plus half trend had a 15% worst drawdown against
  31%, for about two points a year less return. That is what the funds sell: crisis insurance that
  pays roughly for itself. The Sharpe ratio did not improve (0.74 against 0.79) over this window.
- **The luck test does not clear it.** The breakout comes closest, at p = 0.086. A futures portfolio
  with more markets (rates in several countries, many more commodities) is what the funds actually
  run, and ETFs cannot reproduce it. That is the honest limit of a free-data version.
- **Not added to the systems book.** It does not pass, and its value is as a hedge, not as income.
  The weekly rebalance and 28 positions would also be a lot of paper to track for a hedge.

## Reproduce

```
/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0084/p0084.py
```
Needs the CSVs from `experiments/2026-10-07-P-0082/fetch_prices.py` for the 28 symbols. About
three minutes for 1,000 shuffles. Full numbers, year by year, are in `results.json`.
