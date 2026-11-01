# P-0291: ICON's Munich bias at the airport, at the lead the calls are made

1 Nov 2026, nightly probe loop, refill rows 64 and 67 merged. P-0281 measured the city station
(DWD 03379) only. Here: Open-Meteo previous-runs API at the airport grid point (asked 48.3538,
11.7861, served 48.3469, 11.7705), hourly latest, day-ahead and two-days ICON seamless runs, maxed
per Berlin day, against DWD 01262 Muenchen-Flughafen daily TXK, 1 Sep to 31 Oct 2026, 61 days.
`airport_lead_bias.py` reuses P-0281's table code so the two are like for like.

## Measured (`results.json`), observed minus ICON

| lead | airport bias, sd | city bias, sd (P-0281) |
|---|---|---|
| latest run | +0.13, 0.56 | +0.66, 0.68 |
| day ahead | +0.35, 1.47 | +0.83, 1.32 |
| two days | +0.54, 1.22 | +1.00, 1.35 |

Exact-degree hit at the day-ahead lead: airport +0.0 gives 47% (Sep) and 36% (Oct), +0.5 gives 33%
and 42%; the city with +1.0 gives 50% and 29%.

## So

The airport runs about half a degree warmer relative to ICON than the city, at every lead: the
task file's "+0.3C for the airport" is right for the day-ahead run (+0.35) and a touch low two days
out (+0.54). The noise is the same at both stations (sd about 1.2 to 1.5 a day or more out), so the
station choice moves the centre, not the confidence. The 0.25 single-degree cap still sits under
the measured day-ahead hit rate at either station.

## Verdict

works. Airport day-ahead bias +0.35 (sd 1.47) against the city's +0.83 (sd 1.32) over the same 61
days; the existing corrections hold.
