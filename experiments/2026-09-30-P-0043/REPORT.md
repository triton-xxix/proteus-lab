# P-0043: log-pool weight on the Pitch backtest (arXiv 2608.11505 method)

## Verdict (30 Sep 2026, scheduled nightly)

Works, and the answer is the paper's. The live book has no scored rows yet (`pitch/PREDICTIONS.csv`
is a header only), so this runs on the walk-forward backtest committed 24 Sep: 6,265 fit matches
over 2024-25 and 2025-26, 501 test matches from 2026-27 so far, five league groups.

- Fitted pool weight on the model is 0.00 for all three models (Dixon-Coles, Elo, shots on target),
  against the Shin de-vigged closing average and against the opening average alike. On the fit
  seasons the log-loss profile rises monotonically from 0 to 1 in all six cases, so it is a
  boundary solution, not an optimiser stopping at a bound.
- Unconstrained, the minimum sits below zero: DC -0.175 (the paper found -0.225 on Serie A), Elo
  -0.150, SoT -0.275. Given the price, the models lean slightly the wrong way. I did not test
  whether the negative tilt carries to the test season; the paper found it did not.
- Test-season RPS, market 0.1997 v DC 0.2109, Elo 0.2073, SoT 0.2055. The market wins overall.
- Three per-league cells show a model beating the market on test RPS (Italy DC and SoT, Netherlands
  SoT). Each is about a hundred early-season matches, and the fitted weight for those leagues is
  still 0.00, so I read them as noise, not edge.
- Caveat: average closing odds across books, not Pinnacle's close as in the paper. A sharper
  benchmark would only widen the gap.

What it changes: the Pitch's headline should be this weight, computed on the live book once it has
scored rows, not "Brier minus market". `pool_weight.py` reruns unchanged on any file with the same
columns.

Input `pitch/backtest/predictions.csv` (walk-forward, committed 24 Sep). Seasons [np.int64(2425), np.int64(2526), np.int64(2627)]; weight fitted on [np.int64(2425), np.int64(2526)], tested on 2627. Market is Shin de-vigged average closing odds unless stated.

| market | model | n fit | n test | w fitted [0,1] | w unconstrained | monotone fit | monotone test | RPS mkt test | RPS model test | test log-loss gain at w |
|---|---|---|---|---|---|---|---|---|---|---|
| close | dc | 6265 | 501 | 0.00 | -0.175 | True | True | 0.1997 | 0.2109 | +0.00000 |
| close | elo | 6265 | 501 | 0.00 | -0.150 | True | False | 0.1997 | 0.2073 | +0.00000 |
| close | sot | 6265 | 501 | 0.00 | -0.275 | True | False | 0.1997 | 0.2055 | +0.00000 |
| open | dc | 6265 | 501 | 0.00 | -0.200 | True | True | 0.2003 | 0.2109 | +0.00000 |
| open | elo | 6265 | 501 | 0.00 | -0.175 | True | False | 0.2003 | 0.2073 | +0.00000 |
| open | sot | 6265 | 501 | 0.00 | -0.300 | True | False | 0.2003 | 0.2055 | +0.00000 |

Per league group, closing market, weight fitted on the fit seasons:

| group | model | n fit | w fitted | RPS mkt test | RPS model test |
|---|---|---|---|---|---|
| ENG | dc | 1859 | 0.00 | 0.2109 | 0.2221 |
| ENG | elo | 1859 | 0.00 | 0.2109 | 0.2169 |
| ENG | sot | 1859 | 0.00 | 0.2109 | 0.2172 |
| ESP | dc | 757 | 0.00 | 0.1914 | 0.2092 |
| ESP | elo | 757 | 0.00 | 0.1914 | 0.2067 |
| ESP | sot | 757 | 0.00 | 0.1914 | 0.2033 |
| ITA | dc | 756 | 0.00 | 0.1948 | 0.1859 |
| ITA | elo | 756 | 0.00 | 0.1948 | 0.1909 |
| ITA | sot | 756 | 0.00 | 0.1948 | 0.1865 |
| NED | dc | 609 | 0.00 | 0.1887 | 0.1937 |
| NED | elo | 609 | 0.00 | 0.1887 | 0.1937 |
| NED | sot | 609 | 0.00 | 0.1887 | 0.1848 |
| POR | dc | 609 | 0.00 | 0.1790 | 0.1829 |
| POR | elo | 609 | 0.00 | 0.1790 | 0.1826 |
| POR | sot | 609 | 0.00 | 0.1790 | 0.1857 |
