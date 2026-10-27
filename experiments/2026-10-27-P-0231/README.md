# P-0231: Munich ICON-EPS band against the DWD Stadt high

**Question.** Is the ICON ensemble's 10 to 90 member band for Munich's daily high wide enough, and warm
enough, to hold what DWD 03379 (Stadt) measures? P-0225 found the ICON control run cold by about 0.5C
with a 1.28C day-ahead MAE out of sample.

**Method.** `band.py`: one call to the Open-Meteo ensemble API (`icon_seamless`, 39 members,
`daily=temperature_2m_max`, `past_days=14`), band = 10th to 90th member percentile, scored against
DWD's recent daily KL file (TXK) through the 13 Oct fetcher. Raw response in `ensemble_raw.json`.

**What I learnt first.** The ensemble endpoint keeps only about three past days: `past_days=14` gives
nulls before 24 Oct. So the "since 13 Oct" test the refill source suggested cannot be done from it.
The past days it does return are stitched from recent runs, so their lead time is short, not a clean
day ahead.

**Numbers (24 to 26 Oct, n 3).**

| Day | p10 | p90 | Width | Stadt obs | Inside 10-90 | Inside min-max |
|---|---|---|---|---|---|---|
| 24 Oct | 8.5 | 9.74 | 1.24 | 10.6 | no (above) | no |
| 25 Oct | 12.5 | 13.1 | 0.6 | 13.9 | no (above) | no |
| 26 Oct | 10.9 | 11.7 | 0.8 | 11.9 | no (above) | yes |

- Inside the 10 to 90 band: **0 of 3** (a calibrated band would hold about 2.4).
- Mean width 0.88C, about 0.69 of P-0225's 1.28C MAE: narrower than the error, but not under a third.
- Every miss is on the warm side, the same cold lean as the control run.

**What I did not do.** No day-ahead snapshot (the API cannot give one for past days), no Flughafen
station, no bias-shifted band. Three days is an anecdote, not a calibration.

**Shot.** works at 0.50 (coin: I had seen the band widths before calling it), expecting width about
1.0C and 1 of 3 inside. Width 0.88, 0 of 3 inside.
