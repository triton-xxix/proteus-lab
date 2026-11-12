# P-0420: Munich ICON town bias by the forecast sky

**Question.** P-0226 (this morning) found the town cold bias is a sunshine effect: -1.87°C on sunny
days, +0.29 on dull ones, by observed sunshine. Observed sunshine is not known the day before. Does
ICON's own day-ahead cloud cover or sunshine forecast carry enough of it to beat a flat +0.5°C?

**Called shot.** works at 0.80, "a forecast-cloud correction fitted in sample scores MAE about 1.04 out
of sample (inside 0.98 to 1.08), a little better than flat +0.5 at 1.09". The probe ran and measured,
but the number missed: 1.16, worse than flat +0.5.

**Method.** `forecast_sky.py`: ICON seamless from the Open-Meteo previous-runs API, issued one day
before, for temperature (daily max), cloud cover (mean of 08:00 to 17:00 Berlin time) and sunshine
duration (daily sum). Town station DWD 03379, TXK. Linear correction and a two-bin rule fitted on
15 Aug to 12 Oct (59 days) only, scored on 13 Oct to 11 Nov (30 days). Both variables were served.

## Numbers

Out-of-sample MAE, town, 30 days:

| Correction | MAE °C |
|---|---|
| None | 1.167 |
| Flat +0.5 | **1.087** |
| Flat +1.0 | 1.180 |
| Forecast cloud, linear, fitted in sample | 1.162 |
| Forecast cloud, two bins, fitted in sample | 1.148 |
| Forecast sunshine, linear, fitted in sample | 1.164 |
| Forecast sunshine, two bins, fitted in sample | 1.158 |
| Forecast cloud, refitted on the test days (cheating) | 1.036 |
| Forecast sunshine, refitted on the test days (cheating) | 1.021 |
| Observed sunshine, in-sample fit (P-0226 bound) | 0.984 |

Why the fitted rules fail: in the summer window the error has no relation to the forecast sky at all
(cloud r +0.01, sunshine r 0.00), so the fit comes out as a flat +0.95 and inherits the wrong level.
Out of sample the relation is there but weak: r +0.36 for cloud, -0.31 for sunshine, against -0.64 for
observed sunshine in P-0226. Mean forecast cloud went from 62% to 82%, forecast sunshine from 8.6 h to
4.1 h between the windows.

## What it says

- No forecast-sky rule fitted on summer beats flat +0.5 in autumn. The summer window cannot teach the
  rule because almost every day in it was sunny.
- Even with the answer in hand, the forecast sky only gets to 1.02 to 1.04, a gain of 0.05 to 0.07°C on
  flat +0.5. Half the observed-sunshine effect is lost because ICON's cloud forecast is not the sky
  that arrives.
- So the usable advice from today's two probes is the plain one: shrink the town correction from +1
  to +0.5. A sky rule is not ready, and may be worth 0.05°C when it is.

## Not done

- No refit on autumn days with a later test window; there are no later days yet. That is the honest
  version of the cheating rows, and it needs December.
- Only ICON, only the town station, only linear and two-bin rules.
- Cloud layers (low v high) not split; low cloud alone may track sunshine better.
