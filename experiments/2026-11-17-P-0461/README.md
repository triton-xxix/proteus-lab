# P-0461: the low-cloud warm miss, model or weather?

**Question.** P-0446 and P-0447 found that a cloud base at or below 500 ft before 10Z marks a warm
icon_seamless lead-1 day-high miss at EDDM (-1.07 C). Is that ICON, or do other models miss the same
mornings?

**Method.** `models.py` reuses P-0447's `metar()` and `test()` (definitions only) and pulls lead-1 day
highs for icon_seamless, ecmwf_ifs025 and gfs_seamless at the same city point, in one Open-Meteo
previous-runs call per half-year. Scored on the 365 days all three have, 1 Nov 2025 to 31 Oct 2026.
Error = METAR day high minus forecast (negative = forecast warm). Permutation shuffles the flag within
calendar month, 10,000 times, one-sided.

**Numbers** (results.json; 67 flagged days of 365, 18%).

| model | mean error, all days | flagged | others | **gap** | perm p | 2.5 C+ warm misses caught |
|---|---|---|---|---|---|---|
| icon_seamless | +0.17 | -0.70 | +0.37 | **-1.06** | 0.001 | 9 of 17 |
| ecmwf_ifs025 | +1.04 | -0.29 | +1.34 | **-1.63** | 0.0001 | 9 of 17 |
| gfs_seamless | +0.52 | -1.90 | +1.06 | **-2.96** | 0.0001 | 28 of 35 |
| mean of three | | -0.96 | +0.92 | -1.88 | 0.0001 | 14 of 19 |

ICON's -1.06 matches P-0447's -1.07 on the same days, so the rerun is consistent.

**Reading.** It is the weather, or rather a thing all three models get wrong the same way: low stratus
that holds the day down is forecast to burn off. ICON handles it best. ECMWF runs about 1 C cold on an
ordinary day at this point, so on low-cloud days its cold lean and the warm miss nearly cancel (-0.29);
the gap is still -1.6. GFS is worst by far: -1.9 C on flagged days, and 28 of its 35 big warm misses
are low-cloud mornings. Averaging the models does not wash it out (-1.88).

Set beside P-0459: the Polymarket 09Z price's gap on the same flag was only -0.24 C over 16 days, so
whoever prices that market already leans away from the burn-off forecast.

**Called shot.** works at 0.65, "ECMWF about -0.7, GFS about -1.0, each p under 0.01". Direction and
p held; both sizes were badly under (measured -1.63 and -2.96).

**Not done.** One station (P-0447 did Heathrow and Paris for ICON only). City point, not the airport
point. No lead 2. No blend fitted.
