# P-0367: does the 2 km ICON-D2 ensemble sit warmer and catch Munich's highs?

**Question.** P-0232's ICON-EPS and P-0249's ECMWF bands had the high above the band on 4 of 8 or 9
scored days. Does ICON-D2 (the 2 km ensemble) sit warmer and catch those days?

**Called shot.** works at 0.60; D2 median about 0.5 C warmer than the global ensemble median, on only 3 or 4
past days the API still holds.

**Method.** `d2.py`: one Open-Meteo ensemble call per model (`icon_d2`, `icon_seamless`), same point as
P-0232 (48.137, 11.575), `past_days=7`, `forecast_days=3`, daily high. Observed high is DWD 03379 through
`munich_forecast_error.py`, as P-0232 scores.

**Numbers.** D2 had data on 5 of 10 days (5 to 9 Nov), 19 members, and stops two days ahead.

| Day | Obs (C) | D2 p50 | Global p50 | D2 minus global | D2 p90 | Global p90 |
|---|---|---|---|---|---|---|
| 5 Nov | 8.3 | 7.7 | 7.2 | +0.5 | 8.2 | 8.02 |
| 6 Nov | 4.5 | 3.8 | 3.4 | +0.4 | 4.12 | 3.66 |
| 7 Nov | 8.5 | 7.9 | 7.1 | +0.8 | 8.2 | 7.6 |
| 8 Nov | | 9.8 | 9.6 | +0.2 | 10.22 | 10.3 |
| 9 Nov | | 8.5 | 7.9 | +0.6 | 9.22 | 9.9 |

Mean D2 minus global p50: +0.50 C over 5 days. D2's median missed by 0.6, 0.7 and 0.6 C against the global's
1.1, 1.1 and 1.4 C on the three observed days. It does sit warmer, and it is closer.

It does not catch them. The high was above D2's p90 on 3 of 3 observed days (and above the global p90 on 3
of 3 too). D2's band is also narrower: 0.6 to 0.9 C wide on those days, against 1.2 to 1.7 for the global.

**What I did not do.** Three observed days is not a calibration. The past-days values are short-lead, not
the D-1 forecast the committed band is, so the +0.5 is not yet a D-1 number. On today's and tomorrow's rows
the lead is real, and the gap is +0.2 and +0.6. No forward row is committed yet.
