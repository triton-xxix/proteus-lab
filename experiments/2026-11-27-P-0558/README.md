# P-0558: score the 24 Nov NOAA Kp three-day forecast (D-034)

**Question.** Does NOAA SWPC's 24 Nov Kp forecast beat three dumb baselines on its 17 predicted slots
(25 Nov 00Z to 27 Nov 00Z), and is the +1 high bias seen in the 20 Nov issue (P-0505) repeated?

**Method.** Pre-registered in `experiments/2026-11-24-kp-forecast-snapshot/README.md`, committed before the
outcome. Fetched the same SWPC file on 27 Nov about 12:35Z (`kp-2026-11-27.json`, two failed curl tries
first: a timeout and a DNS failure, the third worked). `score.py` is P-0505's method with the three
baselines from the pre-registration.

**Numbers (17 of 17 slots scored).**

| | MAE |
|---|---|
| NOAA forecast | 1.058 |
| Persistence 1.00 | 0.665 |
| 23 Nov mean 0.792 | 0.726 |
| 17 to 23 Nov mean 1.446 | 0.744 |

Forecast mean 2.02, observed mean 1.39, max observed 3.00 (NOAA had a 4.33 slot). Mean signed error +0.63.
No slot at 5 or more.

**Verdict.** NOAA loses to all three baselines. Pass: no. Same high bias: yes (+0.63 against the +0.5
line). Two issues out of two (20 Nov and 24 Nov) now run high in quiet weather and lose to persistence.

**Called shot.** works at 0.80, NOAA MAE about 1.0 losing to the 0.792 baseline. Measured 1.058, lost to
all three.

**Not done.** Two issues is two draws, both in quiet spells; nothing here says how NOAA does in a storm,
which is what the forecast is for. No per-day split (day 1 v day 3).
