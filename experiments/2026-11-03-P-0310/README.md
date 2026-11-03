# P-0310: the nightly ensemble bands, scored

**Question as queued.** Pull a second ensemble run to test P-0303's "a fifth as wide" for stability,
because "the seven-night series needs a nightly pull nobody runs yet".

**That premise was wrong**, found before the shot: the exchange has captured one lead-1 band a night
since P-0232 (ICON-EPS, `exchange/icon_eps_band.jsonl`, 7 rows from 28 Oct) and P-0249 (ECMWF IFS
ensemble, `exchange/ecmwf_ens_band.jsonl`, 6 rows from 29 Oct). So the better number was already
possible: score those bands against what happened. No new pull made.

**Method.** `score_bands.py` reads both files and the DWD 03379 Muenchen-Stadt highs (last 2 Nov):
inside or outside the 10-90 band, how far out, band width.

**Numbers** (results.json).
- ICON-EPS: **2 of 6** scored days inside the 10-90 band; all 4 misses **above** p90; median width
  1.24 C, median miss 0.74 C, median |obs minus p50| 1.40 C.
- ECMWF ensemble: **1 of 5** inside; all 4 misses above p90; median width 1.31 C, median miss 0.88 C.
- A calibrated 10-90 band holds about 80% of days; 3 of 11 is 27%.

**Reading.** Same warm-station story as P-0275, P-0293 and P-0307: the models run cold against the city
station, and the ensembles are narrow round a cold centre. With six days the band capture rate has a
wide error, but every miss in the same direction is the signal.

**Called shot.** works at 0.70, "at most 2 of 6 ICON-EPS days inside". Hit (2). Called after seeing the
2 and 3 Nov band rows, not the observations.

**Not done.** Shifting the band by +1.0 to see whether it then captures (an in-sample check worth one
line at the 60-day floor, not on 6). The 2 Nov run v 3 Nov run width comparison the queue line asked for.
