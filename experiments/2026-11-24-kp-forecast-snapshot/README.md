# NOAA Kp three-day forecast, saved 24 Nov 2026 about 12:40Z, to be scored after 27 Nov

Refill row 237, the second issue after P-0505 (20 Nov issue: NOAA MAE 1.02 against 0.67 persistence and
0.64 for the 13 to 19 Nov mean, running about one unit high in a quiet spell). One issue is one draw.
`forecast-2026-11-24.json` is straight from
`services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json`, committed before the outcome.

**What it says.** 17 predicted three-hour slots, 25 Nov 00Z to 27 Nov 00Z, Kp 0.67 to 4.33, mean 2.02.
None at 5 or more. Four estimated slots 24 Nov 12Z to 21Z: 2.00, 2.00, 2.67, 3.00. Last observed slot
24 Nov 09Z, Kp 1.00. Observed 17 to 23 Nov: 56 slots, mean 1.446, one at 5.00. 23 Nov observed mean 0.792.

**Pre-registered score (probe opens 27 Nov 03Z or later; DUE D-034).** On the 17 predicted slots,
against observed rows in the same file read on or after 27 Nov 03Z, with P-0505's `score.py` method:
- mean absolute error of NOAA's prediction, and its mean signed error (forecast minus observed);
- against three baselines: persistence (1.00, the last observed slot), the 17 to 23 Nov observed mean
  (1.446), and the last full observed day's mean (23 Nov, 0.792, the third baseline row 237 asked for);
- any observed slot at 5 or more is a miss (none predicted).
Pass: NOAA beats all three on MAE. **Second question: is the high bias the same?** Same bias if the
mean signed error is +0.5 or more again (20 Nov issue: forecast mean 2.08 against a much quieter
observed run). This issue is less flat (a 4.33 slot), so it is a fairer test of the forecaster.
