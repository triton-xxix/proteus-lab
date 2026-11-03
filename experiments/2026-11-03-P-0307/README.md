# P-0307: is P-0293's lead curve a Munich thing? Berlin

**Question.** The exchange book's day-high calls add +1.0 to ICON and P-0293 measured how that holds by
lead at one grid point, Munich. Does a second city give the same curve, so the rule is not resting on one
station?

**Method.** One keyless call to the Open-Meteo previous-runs API (ICON seamless, Berlin-Tempelhof
52.4675, 13.4021, hourly, 1 Sep to 31 Oct 2026, timezone Europe/Berlin, `temperature_2m` and
`_previous_day1` to `_day6`), saved to `sandbox/om-prevruns-berlin-lead0-6.json`. `lead_curve.py` is
P-0293's script pointed at DWD 00433 Berlin-Tempelhof (TXK, recent daily file, keyless, 550 days, last
2 Nov). 61 days at every lead.

**Numbers.**

| lead | Berlin bias | sd | hit +1 | Munich bias | Munich hit +1 |
|---|---|---|---|---|---|
| 0 | +0.81 | 0.51 | 61% | +0.66 | 59% |
| 1 | +0.79 | 0.91 | **49%** | +0.83 | 39% |
| 2 | +0.89 | 1.43 | 41% | +1.00 | 39% |
| 3 | +0.75 | 1.62 | 39% | +1.18 | 30% |
| 4 | +0.72 | 1.88 | 16% | +1.10 | 28% |
| 5 | +0.63 | 2.23 | 25% | +1.09 | 16% |
| 6 | +0.45 | 2.44 | 23% | +1.12 | 13% |

**Reading.** The warm-ICON bias is there in Berlin too, about +0.8 at leads 0 to 3 (Munich +0.7 to +1.2),
so +1.0 is a fair round number for both. The day-before hit is 49% in Berlin against 39% in Munich: 10.2
points better, just outside "within 10", in the good direction. Both cities stay at or above 25% to
lead 3, then fall away. The sd grows about +0.3 a day in Berlin (Munich +0.4). With 61 days the se on a
hit rate is about 6 points, so the cities agree to within noise at leads 0 to 3.

**Called shot.** works at 0.75, "lead-1 hit about 30%, bias under +0.6". The verdict hit; both numbers
missed (49%, +0.79). I expected flat Berlin to have a smaller bias; it did not.

**Not done.** London (its only keyless observation so far is ERA5 reanalysis, not a station). Two months,
one autumn, the best correction in sample. Not checked which Berlin station a market would settle on.
