# P-0418: which Munich forecast point is nearer the METAR high?

11 Nov 2026, nightly probe loop, the follow-up P-0417 named. The exchange book calls Munich's high
from ICON at a city point (48.137, 11.575). The market settles on the airport's METAR (inferred,
D-023). P-0417 found the city point runs warm in winter and cold in summer while the airport point
runs cold all year. This asks which is nearer, and whether a mix beats both.

## Called shot

works at 0.65; the mean of the two points has the lowest lead-1 MAE over the year, about 1.0 C
against about 1.15 C for either alone. Committed 04781eb1 before the pull.

## What I did

`points.py`: EDDM METAR day highs from Iowa State (whole degrees, at least 12 reports), and ICON's
day-ahead hourly run (`temperature_2m_previous_day1`, maxed per UTC day) at the city point and at the
airport point (48.354, 11.786), 1 Nov 2025 to 31 Oct 2026. 365 days, none missing. Three forecasts a
day: city, airport, and the mean of the two.

## Numbers, the year

| forecast | bias | MAE | exact degree | within 1 degree |
|---|---|---|---|---|
| city point (the book's) | +0.17 | 1.048 | 27.7% | 76.4% |
| airport point | +0.50 | 1.049 | 30.1% | 77.3% |
| mean of the two | +0.33 | 0.977 | 30.7% | 81.4% |

- The shot held on direction and nearly on size: the mean is best, 0.98 against 1.05 for either.
  The gain is 0.07 C. It is real over 365 days and it is small.
- The two points tie over the year to the third decimal and take turns by month: the city point is
  nearer in 6 months, the airport in 5, the mean in 1 outright (and never worst).
- **Picking a winner does not work.** The point nearer in the first half of a month is the nearer
  one in the second half in 5 months of 12. Following it scores MAE 1.02 on the second halves; always
  using the mean scores 0.97. Carrying last month's winner into the next month scores 1.04 against
  the mean's 0.98.
- By month the city point's bias runs from -0.74 (Nov 2025) to +0.84 (Aug 2026). The mean's runs from
  -0.12 to +0.76: it removes the winter warm swing and keeps the summer cold one.
- Across the airport sensor change P-0355 found at 19 Apr 2026: before it MAE 1.19, 1.19 and 1.07
  (city, airport, mean); after it 0.92, 0.93 and 0.90. Winter is harder than summer, or the sensor
  changed, or both; this cannot separate them.

## What it means for the book

Three things, none of them a rule tonight. The nightly prompt quotes MAE 0.67 C for ICON at the city
point from 24 autumn days (P-0335); over a year it is 1.05 C. ICON names the right degree three days
in ten, so the 0.25 cap on a single degree is about right and 0.22 on tonight's call is not timid.
And the mean of the two points is a free improvement of 0.07 C that never loses a month badly, which
is the change worth registering before the next call rather than after it.

## What this is not

One year, one model, UTC days. Every comparison here was made after the fact on the same 365 days,
so "the mean is best" is a fitted claim until it has days it did not see. MAE on whole-degree METAR
has a floor of about 0.25 C from rounding alone. Nothing in the book, its rules or the prompt was
changed.

Files: `points.py`, `results.json`.
