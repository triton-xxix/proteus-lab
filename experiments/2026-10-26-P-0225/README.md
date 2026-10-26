# P-0225: Munich ICON cold bias, out of sample

**Question.** The 13 Oct report measured ICON's day-ahead Munich high as 0.95°C cold at DWD
Muenchen-Stadt over 15 Aug to 12 Oct, and the exchange book has added about +1°C in town since. Does
the bias hold on the 13 days after it was measured?

**Called shot.** works at 0.65, "ICON Stadt bias about -0.8°C over 13 to 25 Oct (inside -1.5 to -0.5)".

**Method.** `out_of_sample.py` imports the 13 Oct script's fetchers unchanged (Open-Meteo previous-runs
API, hourly temperature issued one day before, daily max per Berlin day; DWD recent daily KL, TXK) and
splits the days into the original window and the new one. Results in `results.json`, every new day
listed under `out_days`.

## Numbers

ICON seamless, forecast minus observed:

| Station | Window | n | Bias °C (se) | MAE raw | MAE after +1°C | Exact degree |
|---|---|---|---|---|---|---|
| Stadt | 15 Aug to 12 Oct | 59 | -0.95 (0.21) | 1.38 | 0.98 | 19% |
| Stadt | 13 to 25 Oct | 13 | **-0.48 (0.47)** | 1.42 | 1.28 | 31% |
| Flughafen | 15 Aug to 12 Oct | 59 | -0.27 (0.23) | 1.16 | 1.32 | 34% |
| Flughafen | 13 to 25 Oct | 13 | +0.04 (0.30) | 0.82 | 1.18 | 31% |

The in-sample window reproduces the 13 Oct table to the hundredth (-0.95, 1.38, 19%), so the method
and data did not move. ECMWF and GFS stay cold in town (-1.28, -0.41) but less so too.

## What it says

The cold bias in town is still there but half the size: -0.48 against -0.95, and with 13 days the
standard error (0.47) cannot tell -0.5 from -1.0. The +1°C correction still helps on these 13 days
(MAE 1.28 v 1.42 raw) but by 0.14°C, not the 0.40 it gained in sample. The four warm, sunny days of
14 to 16 Oct (ICON 1.5 to 3°C cold) carry most of the bias; the cooler days after 17 Oct are near zero.
At the airport ICON has no bias left at all, and the correction makes it worse.

Shot missed on the number: -0.48 is 0.02 outside the band I called.

## Not done

- No test of a seasonal or sunshine dependence (the warm-days pattern above is a reading of 13 rows,
  not a measurement).
- No change to the exchange book's correction from here; that is the desk's call with more days.
