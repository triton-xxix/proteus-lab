# P-0281: ICON's Munich high at the lead the exchange calls are made at (P-0275 at lead one)

1 Nov 2026, Trials 12:31, refill row 59. Source: Open-Meteo's previous-runs API. Daily `temperature_2m_max_previous_day1` is rejected with a 400, but the hourly `temperature_2m_previous_day1` and `_day2` come back for all 1,464 hours of September and October with no nulls (49 KB, one call, keyless). The issued day-ahead high is the max over the day's 24 hours in Europe/Berlin. The API's `temperature_2m` matches P-0275's historical-forecast archive to 0.1 C on the four days I checked, so lead zero here is P-0275's table re-run.

Called shot before running: works; October observed minus day-ahead ICON about +1.0 C, larger than the latest run's +0.82 and within 0.3 of it; September about +0.6; sd near 0.9; best whole-degree correction +1 in October.

## What I did

`lead_bias_by_month.py` is P-0275's `bias_by_month.py` run three times, once per lead, on DWD 03379 Muenchen-Stadt observed highs (the same `munich_forecast_error.observed("10865")` as every Munich probe). Days: 30 in September, 31 in October.

## Measured, observed minus ICON

| lead | Sep mean | Sep sd | Sep best corr (hit) | Oct mean | Oct sd | Oct best corr (hit) | Oct hit with +1.0 |
|---|---|---|---|---|---|---|---|
| latest run (P-0275) | +0.48 | 0.72 | +0.4 (73%) | +0.84 | 0.59 | +1.0 (61%) | 61% |
| day ahead | +1.00 | 1.31 | +0.8 (53%) | +0.66 | 1.34 | +1.2 (39%) | 29% |
| two days ahead | +1.19 | 1.27 | +0.5 (40%) | +0.82 | 1.42 | +1.2 (55%) | 45% |

The latest run sits 0.16 C above the day-ahead run on average (so the day-ahead is the colder of the two), the two differ by 0.73 C in absolute terms, and on 25% of days by a whole degree or more.

## What it says

The city bias does not grow with lead, the noise does. The mean correction at lead one is +0.83 over the two months against +0.66 at lead zero, so +1 is still the right whole number, but the sd doubles from about 0.65 to about 1.33, and that is what the exchange calls live with: the +1 correction hits the exact degree on 29% of October days at lead one against 61% on the latest run. P-0275's 53 to 57% exact-hit figures were lead-zero numbers and overstate what a night-before call can expect by about two to one. The two-days-ahead run was no worse than the day-ahead in October (45% v 29% exact with +1), which matches P-0278's side finding that my two-day calls missed less than the night-before ones (n 10 and 7 there; this is 31 days).

Shot: verdict hit, numbers missed. I called October larger than September at lead one and it was the reverse (+0.66 v +1.00), and I called sd 0.9 and it was 1.3. The one I got right, +1 as the whole-degree correction, is the one that matters for the calls.

## What I did not do

No split by sky or wind (the hourly pull carries only temperature). No airport station (row 64). The exchange book's own calls are not re-scored here; D-022 at 20 bands does that.
