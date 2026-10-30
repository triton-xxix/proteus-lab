# P-0263: favourite-longshot recalibration on the exchange book

Date: 2026-10-30, Trials slot, refill source 48. The source's code (PolyWeatherData, arXiv 2610.13593)
is a 404 on GitHub (main, master and the API), so this takes the paper's idea only: a recalibration
curve fitted to settled calls, then applied to new ones. One parameter instead of their B-spline,
because 29 rows cannot carry more. Stdlib, keyless.

## Called shot

works at 0.65; a about 1.3, leave-one-out Brier moves under 0.01, bootstrap interval includes 1.

## Method

`recalibrate.py`: p' = sigmoid(a * logit(p)), a on a grid 0.1 to 4.0 by Brier. Leave-one-out for the
honest score (refit a on 28, score the 29th), 2,000-draw bootstrap for the interval on a, and a
three-bucket calibration table by my p.

## Numbers

| measure | value |
|---|---|
| settled rows | 29 |
| a, full fit | 1.4 (leave-one-out fits 1.3 to 1.6) |
| a, bootstrap 95% | 0.6 to 2.8; 80% of draws above 1 |
| Brier raw | 0.1662 |
| Brier in-sample after recalibration | 0.1623 |
| Brier leave-one-out after recalibration | 0.1721 (+0.0059 v raw) |

| my p | n | mean p | hit rate |
|---|---|---|---|
| under 0.35 | 18 | 0.245 | 0.167 |
| 0.35 to 0.65 | 8 | 0.486 | 0.375 |
| 0.65 and over | 3 | 0.793 | 1.000 |

Shot v measured: a 1.4 v 1.3 called, Brier move +0.006 v under 0.01 called, interval 0.6 to 2.8 includes
1. Hit on all three parts.

Reading: the point estimate says I am slightly underconfident (the lows come in lower than I say, the
highs higher), the same direction as the favourite-longshot bias the paper finds in Polymarket prices.
But the interval is wide, and the honest score gets worse, not better: fitting a on 28 rows and applying
it to the 29th costs 0.006 Brier. At 29 rows there is nothing to recalibrate yet. The 60-row floor the
exchange book already carries is the right time to look again.

## What I did not do

- No B-spline, no time-varying term (the paper's actual contribution). One parameter only.
- No fit against the market mid; this is my p against outcomes, not market price against outcomes.
- Did not separate market types (weather, elections, football); 29 rows do not split.
