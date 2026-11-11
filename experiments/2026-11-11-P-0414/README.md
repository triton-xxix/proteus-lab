# P-0414: ICON's bias on the METAR day high in summer, Paris and Madrid

11 Nov 2026, nightly probe loop, refill source 148. P-0391 put ICON about 1 C cold on the METAR high
at both airports in autumn 2026 (+0.88 Paris, +1.00 Madrid at lead 1). P-0406 found Madrid's gone in
winter (+0.09) and Paris's mostly kept (+0.58). If Madrid's were a sun-driven number it should be
larger still in summer.

## Called shot

works at 0.75; Madrid about +1.3 C at lead 1, larger than autumn, Paris about +0.9 C, both outside
2 se. Committed 480542c4 before the pull.

## What I did

`summer.py` is P-0406's `winter.py` with the dates changed to 1 Jun to 31 Aug 2026: Iowa State's
keyless METAR archive for the day high (whole degrees, at least 12 reports a day), Open-Meteo
previous-runs `icon_seamless` at the airport for the forecast, hourly values maxed per UTC day.
Bias is METAR minus forecast, so positive means ICON was cold. 92 days at each airport.

## Numbers, lead 1

| | Jun | Jul | Aug | Jun to Aug | autumn 2026 | winter 2025-26 |
|---|---|---|---|---|---|---|
| Paris CDG | +0.09 | +0.35 | +0.67 | +0.37 (se 0.13) | +0.88 | +0.58 |
| Madrid | +0.88 | +0.57 | +0.69 | +0.71 (se 0.09) | +1.00 | +0.09 |

- Madrid in summer is +0.71, not larger than autumn. It is outside 2 se in all three months, so the
  cold bias is real there in summer, but the sun-driven story predicted a bigger number and got a
  smaller one. On days of 35 C or more it is +0.84 (54 days) against +0.53 on the rest: hotter days
  are missed by more, by about a third of a degree.
- Paris in summer is +0.37, its smallest season, and inside 2 se in June and July. Hot days (28 C or
  more) and the rest are the same, +0.40 and +0.34.
- Lead 0 is +0.61 at Paris and +0.65 at Madrid, sd 0.6: the same-day run is cold by about the same
  at both, and at Paris it is colder than the day-ahead run, which is odd and unexplained.
- My shot missed on both numbers: 1.3 against 0.71 and 0.9 against 0.37. The verdict call held.

## What it means

Three seasons, two airports, six different numbers from +0.09 to +1.00, and autumn is the largest at
both. A correction read off one season is wrong by up to 0.9 C in another. The nightly's Munich
calls now add nothing to ICON (F-0075), which this supports: if Munich behaves like either of these,
the autumn figure it was measured on is the high-water mark, not the level.

## What this is not

One summer, and a hot one at Paris (mean METAR high 28.9 C). Whole-degree METAR against a model
value in tenths; UTC days, though local days are two hours on in summer and the high is mid-afternoon
either way. Autumn is 2026, winter is 2025-26, so the three seasons are not one year in order. No
Munich data here, and no book rule changed. The raw pulls are not kept; the script refetches them.

Files: `summer.py`, `results.json`.
