# P-0327: which ICON does icon_seamless serve at each lead? (5 Nov 2026)

Refill build from REFILL-SOURCES row 91, which found Météo-France's seamless blend is ARPEGE at
two days out (96 of 96 hours) and that AROME HD serves no day-2 runs. The same question for the
model behind every Munich exchange call.

## What I ran

`sandbox/icon-lead/which.py`, one keyless call to Open-Meteo's previous-runs API at Munich airport
(48.3538, 11.7861), 6 Oct to 5 Nov 2026 (744 hours), hourly temperature at leads 0 to 3 for
icon_seamless, icon_d2, icon_eu and icon_global. `which.json` has every number.

## Result

| Lead | icon_seamless is | Hours equal | Seamless mean daily high |
|---|---|---|---|
| 0 | ICON-D2 | 744 of 744 | 13.24 C |
| 1 | ICON-D2 | 744 of 744 | 13.23 C |
| 2 | ICON-EU | 744 of 744 | 13.28 C |
| 3 | ICON-EU | 744 of 744 | 13.22 C |

ICON-D2 serves no previous_day2 or day3 values at all, so the blend drops to ICON-EU from day 2.
The switch does not move the mean daily high: lead 1 (D2) and lead 2 (EU) differ by +0.05 C over
these 31 days. So the switch is not what made P-0302's airport bias drift from +0.13 at lead 1 to
about +0.6 at lead 2; if that drift is real it comes from the forecasts' spread or from that
window (Sep to Oct), not from a colder model taking over.

What it changes for the desk: a Munich call two days out (X-0048 tonight) rests on ICON-EU at
about 7 km, not ICON-D2 at about 2 km. Same mean here, different model, worth naming in the reason.

## Caveats

- 31 days, one point. The mean daily high is not the error; scoring each lead against DWD's
  station high is P-0302's job and not repeated here.
- At lead 0 ICON-EU and global run 0.34 C colder than D2 on the daily high; from lead 1 on the
  three agree within 0.01 C. Not explained tonight.
