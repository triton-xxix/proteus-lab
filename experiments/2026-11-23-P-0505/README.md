# P-0505: did NOAA's 20 Nov Kp three-day forecast beat dumb baselines?

**Question.** The forecast saved 20 Nov about 12:35Z (`experiments/2026-11-20-kp-forecast-snapshot/`,
committed before the outcome) gave 17 predicted three-hour slots, 21 Nov 00Z to 23 Nov 00Z. Pre-registered
pass: NOAA's mean absolute error beats persistence (0.67 every slot) and the 13 to 19 Nov observed mean.

**Method.** Fetched the same SWPC product on 23 Nov about 12:35Z (`kp-2026-11-23.json`), took its
"observed" rows for the 17 slots, ran `score.py`. All 17 slots had observed values.

**Numbers** (`results.json`):

| | MAE |
|---|---|
| NOAA forecast (mean 2.08) | 1.02 |
| Persistence 0.67 | 0.67 |
| 13 to 19 Nov mean, 1.35 (56 slots) | 0.64 |

Observed mean 1.14, max 2.67, no slot at 5 or more (so no missed storm). NOAA ran about one Kp unit high
across a quiet weekend and lost to both baselines. **Fail.**

Called shot: broken at 0.55, NOAA about 0.8 against baseline about 0.6. Direction right, NOAA worse than I
guessed.

**What I did not do.** One forecast issue is one draw: 17 slots, strongly autocorrelated, so this is a
single quiet-spell data point, not a skill score. SWPC's "observed" rows are preliminary and can be revised.
No probabilistic or storm-day scoring; the 27-day outlook (D-032) is scored separately after 13 Dec.
