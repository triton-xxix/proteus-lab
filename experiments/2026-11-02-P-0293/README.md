# P-0293: Munich day-high error by lead, 0 to 6 days

**Question.** P-0281 measured the ICON Munich high against DWD 03379 at leads 0, 1 and 2. How does the
error grow out to a week, and how early can an exchange call be made before the exact-degree hit (after
the +1.0 correction the calls use) falls under 25%?

**Method.** One keyless call to the Open-Meteo previous-runs API (ICON seamless, 48.1374, 11.5755, hourly,
1 Sep to 31 Oct 2026, `temperature_2m` and `_previous_day1` to `_day7`), saved to
`sandbox/om-prevruns-munich-lead0-7.json`. Lead 7 came back all null; leads 0 to 6 had no nulls in 1,464
hours. `lead_curve.py` maxes each lead per Berlin day and compares with DWD Stadt observed highs (61 days).

**Numbers.**

| lead (days) | mean obs minus ICON | sd | MAE after +1 | within 1 deg after +1 | exact hit +0 | exact hit +1 |
|---|---|---|---|---|---|---|
| 0 | +0.66 | 0.68 | 0.55 | 87% | 30% | **59%** |
| 1 | +0.83 | 1.32 | 0.92 | 72% | 25% | 39% |
| 2 | +1.00 | 1.35 | 0.89 | 70% | 20% | 39% |
| 3 | +1.18 | 1.78 | 1.13 | 64% | 20% | 30% |
| 4 | +1.10 | 2.21 | 1.55 | 46% | 15% | 28% |
| 5 | +1.09 | 2.64 | 1.82 | 41% | 26% | 16% |
| 6 | +1.12 | 2.74 | 2.00 | 36% | 31% | 13% |

Leads 0 to 2 match P-0281's biases (+0.66, +0.83, +1.00). The warm bias stops growing after lead 3 (about
+1.1), while the sd keeps climbing, about +0.4 a day. The +1.0 hit stays at or above 25% out to lead 4.

**Reading.** Lead 0 is the latest run, issued on the day, nearly a nowcast; it is not a call anyone can
make the evening before. For a call made the day before, the hit is 39% and stays there at two days; it
drops to about 30% at three and four days and below the 25% line from five. The +0 hits at leads 5 and 6
(26%, 31%) beating +1 there is noise on 61 days (se about 6 points), not a sign the correction flips.

**Not done.** Two months only (Sep, Oct), one grid point (the city), no airport, no ensemble spread, the
best correction picked in sample.
