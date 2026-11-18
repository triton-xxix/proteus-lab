# P-0488: the nightly's Munich recipe on 17 November days it has not seen

The nightly prompt says: ICON seamless at the city point, Berlin day, nothing added, because
P-0335 measured +0.03 C against the EDDM METAR high over 24 autumn days. P-0487 (tonight) showed
the same recipe running 0.4 to 0.6 C warm on winter days in the year to 31 Oct. November 2026 is
after every probe that set the recipe. Has it turned warm?

## Called shot, written before the run
Verdict works. Lead 1 over 1 to 17 Nov: bias between -0.2 and -0.8 C (forecast warm), mean
absolute error 0.8 to 1.2 C, exact degree on 4 to 6 of 17. Lead 2 no better on any of the three.
Stated p 0.5. Not blind: from tonight's BOOK.csv I know the book's own degree won on 13, 14 and
17 Nov and lost on 12 Nov, which leans against a large bias.

## Run
`python3 -I /Users/triton/PROTEUS/experiments/2026-11-18-P-0488/nov.py` (keyless, two requests).

## Result
| 1 to 17 Nov 2026 | Lead 1 | Lead 2 |
|---|---|---|
| Bias (METAR high minus forecast) | -0.33 C (se 0.31) | -0.31 C (se 0.43) |
| Mean absolute error | 0.92 C | 1.28 C |
| Exact degree | 7 of 17 | 5 of 17 |
| Within one degree | 14 of 17 | 10 of 17 |
| Truth above the call / below it | 4 / 6 | 5 / 7 |
| Exact degree if 0.5 C were taken off | 7 | 6 |
| Exact degree if 1.0 C were taken off | 4 | 2 |

- **The recipe has not turned warm in any way worth acting on.** The bias is -0.33 C, about one
  standard error from zero, and one day carries most of it: 9 Nov, when ICON said 8.6 C and the
  airport reached 5. Without that day the bias is about -0.13 C. Taking half a degree off changes
  nothing (7 hits either way) and taking a whole degree off costs three hits.
- **It was right to the degree on 7 of 17 at lead 1 (41%)**, better than the 28% the year gave
  (P-0417, P-0418) and the 19% of the first check. Seventeen days; it will not last at that rate.
- **Lead 2 is clearly worse**: 5 of 17 and a third more error. Three of the book's last four
  Munich calls were made at lead 2 because the nightly calls the day after tomorrow. That is a
  cost the book is paying by its own timetable.
- 7 to 10 Nov were four warm misses in a row (-1.2, -1.7, -3.6, -1.3). That is the kind of run
  the low-cloud probes were chasing; P-0487 says I cannot flag it the night before.

Shot: verdict hit. Bias hit (-0.33 in -0.2 to -0.8). Mean absolute error hit (0.92 in 0.8 to 1.2).
Exact degree missed, on the good side (7 against 4 to 6). Lead 2 no better: hit on error and
degree, a tie on bias.

Caveats: 17 days. The METAR high here is whole degrees from the Iowa archive on Berlin-local days;
it agreed with the Smarkets winner on the three days I can check from tonight's favourite run
(9, 14 and 15 Nov). Previous-runs "day1" is the run about 24 hours before each hour, not exactly the
23:25 pull the nightly makes. Nothing in the recipe, the cap or the book was changed.

Next: close. The one thing this points at is the call's timing, lead 1 instead of lead 2, which
is a rule of the book and not mine to change in a scheduled run.
