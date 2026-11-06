# P-0336: ICON-D2 v ICON-EU for a one-day Munich call (6 Nov 2026)

Refill row 99. P-0327 found the seamless blend serves D2 at leads 0 to 1 and EU from lead 2. Does the
choice of model matter for a one-day call?

Shot: D2 lead 1 MAE against DWD 03379 about 0.15 C below EU lead 1, on about 60 days. **Missed.** The
measured gap is 0.02 C, se 0.09, on 60 days.

## What I ran

One Open-Meteo previous-runs call at the city point, then `d2_v_eu.py` against DWD 03379 TXK (7 Sep to
5 Nov, 60 days) and P-0334's EDDM METAR high (13 Oct to 5 Nov, 24 days). `results.json` has the rest.

## What I found

| Forecast, city point | MAE v DWD 03379 | Exact, of 60 | MAE v METAR | Exact, of 24 |
|---|---|---|---|---|
| D2 lead 0 | 0.79 | 17 | 0.83 | 11 |
| D2 lead 1 | 1.16 | 15 | 0.67 | 9 |
| EU lead 0 | 1.03 | 11 | 0.94 | 7 |
| EU lead 1 | 1.18 | 11 | 0.83 | 11 |
| EU lead 2 | 1.21 | 12 | 1.06 | 6 |

1. **At lead 1 the two models are level.** EU minus D2 absolute error is +0.02 C (se 0.09) against DWD
   and +0.17 C (se 0.14) against METAR. Neither separates from zero. The exact-degree counts disagree on
   the winner too: 15 v 11 against DWD, 9 v 11 against METAR.
2. **D2's edge is at lead 0 only,** 0.79 v 1.03 against DWD.
3. **The seamless numbers check out.** D2 lead 1 here reproduces P-0335's "city grid +0" row to the
   hundredth (+0.03, 0.87, 0.67), which confirms P-0327 that the seamless blend serves D2 at lead 1.

The answer for the desk is that picking D2 or EU for a one-day call would not change anything measurable,
so the nightly's single `icon_seamless` call stays as it is.

## What I did not do

Change anything. The METAR column carries P-0334's unconfirmed rule and only 24 days.
