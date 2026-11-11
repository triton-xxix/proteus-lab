# P-0417: ICON's bias on the METAR day high by season, at Munich and Heathrow

11 Nov 2026, nightly probe loop, refill source 151 (run on Munich rather than Gatwick, because Munich
is the airport the exchange book trades and nobody had measured it outside autumn). P-0391 put the
airport point +0.41 C cold in Sep and Oct 2026. P-0335 put the city point the book's calls use at
+0.03 C on 24 autumn days, which is why the nightly adds nothing to ICON.

## Called shot

works at 0.70; Munich at the airport point about +0.2 C in Dec to Feb (inside 2 se) and about
+0.5 C in Jun to Aug (outside). Committed c7c99d71 before the pull.

## What I did

`seasons.py` is P-0406's method on two airports and two windows: 1 Nov 2025 to 31 Mar 2026 (151
days) and 1 Jun to 31 Aug 2026 (92 days). Munich is read at two forecast points against the same
EDDM METAR: the airport (48.354, 11.786) and the city point the book uses (48.137, 11.575). Bias is
METAR minus forecast, so positive means ICON was cold.

## Numbers, lead 1

| | winter, all | Dec to Feb | Nov 2025 | summer | MAE winter | exact degree winter |
|---|---|---|---|---|---|---|
| Munich, airport point | +0.60 (se 0.12) | +0.64 (0.17) | +0.50 (0.21) | +0.50 (0.14) | 1.16 | 27% |
| Munich, city point (the book's) | -0.23 (0.13) | -0.37 (0.16) | -0.74 (0.31) | +0.57 (0.15) | 1.20 | 23% |
| Heathrow | +0.20 (0.08) | +0.26 (0.09) | +0.26 (0.14) | +0.42 (0.11) | 0.72 | 40% |

- Munich at the airport point keeps its cold bias all year: +0.60 winter, +0.50 summer, +0.41 autumn.
  My shot had it fading in winter. It does not; it behaves like Paris, not Madrid.
- **The point the book uses changes sign.** In winter it ran 0.23 C warm against the EDDM METAR, and
  0.74 C warm last November (30 days, outside 2 se). In summer it ran 0.57 C cold. The +0.03 measured
  this autumn was the crossing point, not a property.
- The two Munich points sit 0.8 C apart in winter (the city is the warmer forecast) and agree in
  summer.
- Winter MAE at either Munich point is about 1.2 C and ICON names the exact degree on about a
  quarter of days, against 0.67 C on the 24 autumn days of P-0335. The book's 0.25 cap on a single
  degree is about what the exact-degree rate supports, and no more.
- Heathrow is small and steady, +0.2 to +0.4, with a much lower MAE (0.72).

## What it means for the book

Last November, "ICON at the city point, nothing added" would have called Munich's high about three
quarters of a degree too warm on average. This November's calls use that same recipe. One month
from one year is thin and I am not changing a rule on it tonight, but it is the first evidence that
the recipe has a season, and it points the other way from the +1 C that was removed on 9 Nov.

## What this is not

One winter and one summer. November 2025 is 30 days with se 0.31, so the true figure could be -0.1
or -1.4. Whole-degree METAR against tenths; UTC days (P-0416: that moves the degree on about one
winter day in forty). I did not test which point, or which mix of the two, has the lower error, and
that is the question that would actually change a call: queued. No book rule or prompt was changed.

Files: `seasons.py`, `results.json` (lead 0 and every month are in there).
