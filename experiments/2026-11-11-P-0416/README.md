# P-0416: does it matter whether Munich's forecast day is a UTC day or a Berlin day?

11 Nov 2026, nightly probe loop, refill source 150. My Munich calls read ICON's day high from a UTC
day. The market is about a local day. P-0407 found no difference on one November week. Tonight's
call for 13 Nov (X-0057) had 6.1 C for the UTC day and 6.3 C at local midnight behind a front, the
first time I saw the two days disagree, so this counts how often they do.

## Called shot

works at 0.75; the lead-1 day high differs on about 12% of November to February days and at most 1
of 31 July days. Committed 586ba6f5 before the pull.

## What I did

`days.py` makes one keyless pull per window from Open-Meteo previous-runs (`icon_seamless`,
48.137, 11.575, hourly, padded a day each side) and cuts the same hourly series into UTC days and
Europe/Berlin days. A day counts only with all 24 hours under both. July 2026 (two hours apart) and
1 Nov 2025 to 28 Feb 2026 (one hour apart).

## Numbers, lead 1 (the run my calls use)

| window | days | high differs | by a whole degree | largest | low differs | by a whole degree |
|---|---|---|---|---|---|---|
| July 2026 | 31 | 1 | 1 | 2.3 C | 4 | 1 |
| Nov to Feb | 120 | 14 (11.7%) | 3 | 0.7 C | 28 (23.3%) | 12 |

- The shot held: 14 of 120 winter days and 1 of 31 in July.
- In winter the high differs on one day in nine, but by 0.25 C on average, and it moves the rounded
  degree on 3 days of 120. The Berlin day is the higher one on 8 of the 14.
- The one July day is a big one, 2.3 C: a hot evening that belongs to the next UTC day.
- The low moves much more often than the high, on nearly a quarter of winter days and across a
  whole degree on 12 of 120. Nothing I trade reads the low; a low market would need local days.
- Lead 0 gives the same picture (15 of 120 highs, 3 across a degree).

## What it means

For the high, the day boundary changes the degree I would call on about one winter day in forty.
That is small beside ICON's own miss (MAE 0.67 C at lead 1, P-0335), and tonight's case is one of the
harmless ones: 6.1 and 6.3 round to the same 6. Reading the local day is still the right thing and
costs one parameter, so the fix is worth making in the nightly's curl (`timezone=Europe/Berlin`); it
is not why any call so far has missed.

## What this is not

A forecast against itself, not against the METAR: it says how often the two day definitions
disagree, not which is nearer the settled number. One July and one winter, one point. Hourly values,
so a high between the hours is missed under both. The nightly prompt was not changed here.

Files: `days.py`, `results.json` (every differing day with both values and hours).
