# P-0226: Munich ICON bias, 30 days out of sample, split by sunshine

**Question.** P-0225 found the town cold bias had halved on 13 days (-0.48, se 0.47) and could not
tell -0.5 from -1.0. With 30 days observed (13 Oct to 11 Nov): which is it, does it depend on sunshine,
and should the exchange book's +1°C in town shrink?

**Called shot.** works at 0.80, "ICON Stadt bias about -0.4°C (inside -0.65 to -0.15), sunny days at
least 0.5°C colder-biased than dull days". Hit on both: -0.52, and a 2.16°C gap.

**Method.** `sun_split.py` imports the 13 Oct fetchers unchanged (Open-Meteo previous-runs, hourly
temperature issued one day before, daily max per Berlin day; DWD recent daily KL, TXK) and adds SDK
(sunshine hours) from the same DWD file for Muenchen-Stadt. Thresholds were written into the script
before it ran: sunny is SDK of 5 h or more, dull is 1 h or less. The airport file has no usable SDK, so
the airport rows borrow the town's sunshine. Results in `results.json`, every day under `out_days`.
The P-0225 folder was not touched.

## Numbers

ICON seamless, forecast minus observed, Muenchen-Stadt:

| Window | n | Bias °C (se) | MAE raw | +0.5 | +1.0 |
|---|---|---|---|---|---|
| 15 Aug to 12 Oct (in sample) | 59 | -0.95 (0.21) | 1.39 | 1.08 | 0.98 |
| 13 to 25 Oct (P-0225) | 13 | -0.48 (0.47) | 1.42 | 1.29 | 1.29 |
| 26 Oct to 11 Nov (new) | 17 | -0.55 (0.29) | 0.97 | 0.93 | 1.10 |
| **13 Oct to 11 Nov (all out of sample)** | 30 | **-0.52 (0.26)** | 1.17 | **1.09** | 1.18 |

The in-sample row and the P-0225 row reproduce to the hundredth, so the data did not move.

Out of sample, by the day's sunshine (town):

| Days | n | Bias °C (se) | MAE raw | MAE +1.0 |
|---|---|---|---|---|
| Sunny (5 h or more) | 7 | -1.87 (0.40) | 1.87 | 1.13 |
| Middle | 9 | -0.72 (0.28) | 0.83 | 0.72 |
| Dull (1 h or less) | 14 | +0.29 (0.35) | 1.03 | 1.50 |

Error on sunshine hours, out of sample: -0.28°C per hour (se 0.064, r -0.64, intercept +0.25). In
sample the slope was -0.076 (se 0.051): the days were nearly all sunny then (43 of 59), so there was
little to split.

Airport, out of sample: bias +0.09 (se 0.21), raw MAE 0.91, every correction makes it worse. Dull days
at the airport run +0.73 warm.

## What it says

- The town bias is -0.5, not -1.0. Two separate windows agree (-0.48 and -0.55), and -0.95 is 1.7
  standard errors away from the 30-day figure.
- A flat +1°C no longer earns anything out of sample: MAE 1.18 against 1.17 raw. A flat +0.5 is the
  best flat number (1.09), a gain of 0.08°C.
- The bias is a sunshine effect. On sunny days ICON is 1.9°C cold in town and +1 is still too little;
  on dull days it is 0.3 warm and +1 costs half a degree of error. 14 of the last 30 days were dull
  against 7 of 59 in the summer window, which is why the average halved.
- So for the exchange book: shrink the flat town correction to +0.5 now, and the better rule is by the
  sky, about +1.5 to +2 on a forecast-clear day and nothing on a forecast-overcast one.

## Not done

- The split uses observed sunshine, which is not known when the forecast is read. Applying the
  in-sample sunshine fit out of sample gives MAE 0.98, an upper bound on what a sun-aware rule could do.
  Whether forecast cloud or sunshine (which is known the day before) gets most of that is the deepen.
- 7 sunny days is thin; the -1.87 has a standard error of 0.40.
- No change made to the exchange book's correction from here; that is the desk's call.
- ECMWF and GFS not split.
