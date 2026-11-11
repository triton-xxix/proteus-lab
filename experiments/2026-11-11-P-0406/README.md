# P-0406: ICON lead-1 bias on the METAR high, winter, Paris CDG and Madrid

Trials, 11 Nov 2026. Refill source 143.

**Question.** P-0391 put ICON +0.88 C (Paris CDG) and +1.00 C (Madrid) cold on the METAR day high at
lead 1 in Sep and Oct 2026. Does that hold from 1 Nov 2025 to 31 Mar 2026, or is it a warm-season thing?

**Shot.** works at 0.80: Dec to Feb lead-1 bias about +0.4 C at both airports, smaller than autumn but
still outside 2 se; 2 of 10 airport-months inside 2 se. Before the shot I had seen two days of the
archive's model values at Paris (to check it reached Nov 2025), no METAR.

**Method.** `winter.py`, which is P-0391's `four.py` with the dates changed and a monthly split: Iowa
State keyless METAR (routine and special, whole degrees, at least 12 reports a day, UTC days) against
Open-Meteo previous-runs `icon_seamless` at each airport's coordinates, hourly maxed per UTC day. Mean
METAR minus forecast. 4 calls, raw pulls saved. 151 days at each airport, none dropped.

**Numbers** (results.json), METAR minus ICON at lead 1, mean (se), n:

| | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Mar 26 | Dec to Feb | all 151 | autumn 26 (P-0391) |
|---|---|---|---|---|---|---|---|---|
| LFPG Paris CDG | +0.25 (0.20) | +0.63 (0.16) | +0.55 (0.17) | +0.57 (0.22) | +0.50 (0.14) | +0.58 (0.10) | +0.50 (0.08) | +0.88 (0.15) |
| LEMD Madrid | +0.02 (0.21) | -0.11 (0.19) | +0.11 (0.26) | +0.27 (0.20) | -0.10 (0.23) | +0.09 (0.13) | +0.04 (0.10) | +1.00 (0.16) |

Lead 0, all 151 days: Paris +0.35 (0.04), Madrid -0.16 (0.06).

**Reading.**

- Paris keeps the cold bias through winter, about two thirds of its autumn size: +0.58 in Dec to Feb,
  outside 2 se in four of five months (November is the one inside).
- Madrid's goes. +0.09 in Dec to Feb, inside 2 se in all five months, and at lead 0 ICON is slightly
  warm (-0.16). The autumn +1.00 is a warm-season number there.
- 6 of 10 airport-months inside 2 se, against my 2. I was right about Paris (+0.58 v my +0.4) and
  wrong to lump Madrid in with it.
- So one flat correction per airport is wrong for Madrid: adding +1.0 C to an ICON Madrid high in
  January would have cost about 0.9 C. A correction has to be per airport and per season.

**Caveats.** METAR whole degrees; UTC days (Madrid's local day is an hour off in winter); one model;
one winter; the winter is 2025-26 and the autumn is 2026, so season and year are tangled. The Madrid
grid point is 593 m against the airport's 610 m or so, the same point P-0391 used.

**Not done.** No change to any book's correction; that is a desk call. No summer months, which is
where the Madrid number would be tested properly (the archive may reach; not checked).
