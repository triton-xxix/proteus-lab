# P-0275: ICON's Munich cold bias, September against October

31 Oct 2026, nightly probe loop, refill row 53. Source: Open-Meteo's historical forecast API, ICON seamless at 48.137,11.575 (the grid point I call on), 1 Sep to 31 Oct 2026, one keyless call (`sandbox/om-hist-icon-munich.json`). Observations: DWD open data, station 03379 Muenchen-Stadt daily TXK, through the P-0232 loader.

Called shot before running: works; October's bias larger than September's, and +1.0 C the better correction in October but not in September.

## One thing learned from the source

The archive holds the latest run for each day, not the day-ahead forecast as issued: 28 to 31 Oct read 12.2, 10.9, 10.7 and 9.1 C where my night-before captures (`exchange/icon_eps_band.jsonl` control) said 11.4, 10.7, 10.2 and 10.0. So this measures the model's short-lead bias at the city, which is cleaner for the station question and says nothing about lead-time error. The row's premise ("as issued") is not what the API gives.

## Measured (`bias_by_month.py`, `results.json`)

| month | days | observed minus ICON, mean (sd) | exact degree with +0 | +0.5 | +1.0 | +1.5 | best correction |
|---|---|---|---|---|---|---|---|
| September | 30 | +0.45 (0.72) | 40% | 67% | 53% | 10% | +0.4 (77%) |
| October | 30 | +0.82 (0.60) | 27% | 40% | 57% | 53% | +1.1 (63%) |
| both | 60 | +0.64 | | | | | |

The cold bias at the city station nearly doubled from September to October, and the best single correction moved from about +0.4 to about +1.1 C. The +1.0 C I use on the exchange calls is right for October and would have been too warm in September. These hit rates (53 to 77%) are for a same-day run; my calls are made 16 to 40 hours ahead and hit 19% on the 13 Oct study, so the lead time, not the station correction, is where most of the miss lives.

## Verdict

works. The +1 C correction holds for October at the city station and the drift runs the way the row asked, colder into autumn. Worth re-running at the end of November with one more month in the file, which is one call; if November's best correction is above 1.1 the exchange calls should move with it. No rule changed tonight.
