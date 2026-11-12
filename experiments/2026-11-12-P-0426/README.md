# P-0426: P-0418's three Munich points on the November days it never saw

12 Nov 2026, nightly probe loop, refill row 159. `november.py` is P-0418's `points.py` with the dates
moved to 1 to 12 Nov 2026: Iowa State EDDM METAR day high against Open-Meteo previous-runs
`icon_seamless` lead 1, UTC days, at the city point the book uses, the airport point and their mean.
Error is METAR minus forecast; negative means the forecast ran warm.

**Called shot (commit 6dd7a609).** works at 0.55: the mean has the lowest MAE, about 0.9 (band 0.6 to
1.2), and the city bias sits between -0.3 and +0.6. The first part hit (0.912). The second missed:
the city point ran 0.47 C warm.

| Point | Days | Bias | MAE | Exact degree | Within 1 | Nearest on |
|---|---|---|---|---|---|---|
| City (the book's) | 12 | -0.47 | 0.967 | 4 | 10 | 6 days |
| Airport | 12 | -0.59 | 0.975 | 4 | 9 | 4 days |
| Mean of the two | 12 | -0.53 | 0.912 | 3 | 11 | 2 days |

**Reading.**

- The year's ranking held out of sample, by a hair: mean 0.91, city 0.97, airport 0.98, against 0.98,
  1.05, 1.05 on the year. A gap of 0.06 C on twelve days is not a reason to change the recipe.
- All three points ran warm in early November, by about half a degree. Nov 2025 had the city point
  0.74 warm, so this is the second November running. The nightly prompt says "nothing added"; on these
  days taking half a degree off would have helped.
- One day carries a lot of it: 9 Nov, METAR 5.0 against a city forecast of 8.6. Without it the city
  bias is -0.18 and its MAE 0.73 (the verdict note says -0.19, a rounding slip of mine).
- The city point hit the exact degree on 4 of 12, the same as the airport, and was the nearest of the
  three on 6 days.

**Caveats.** Twelve days. UTC days, as P-0418, while the market settles on the local day. 12 Nov had
47 of 48 reports when pulled. The 9 Nov gap may be a UTC-day effect and was not chased.

**Next.** Deepen, once the month is whole: the same table on 1 to 30 Nov with Berlin days, and whether
a November-only -0.5 C would have improved the book's calls. No change to the recipe tonight.
