# P-0063, Nightwatch slice: Open-Meteo cloud cover to tonight's longest clear dark run

Ran 5 Oct 2026, about 22:55 UTC. Keyless. `nightwatch.py`, raw rows in `result.json`.

- One Open-Meteo forecast call per site (hourly total, low, mid and high cloud, visibility). Darkness
  computed locally: sun below -18 degrees at the hour's midpoint (NOAA low-precision formula),
  because Open-Meteo gives only sunrise and sunset. Clear means total cloud at or below 20 percent.
- Kielder, Exmoor, Galloway: 6, 7 and 6 dark hours left tonight, every one at 99 to 100 percent
  cloud. Longest clear dark run: 0 hours at all three. The nearest clear hour anywhere was Galloway
  16:00 UTC tomorrow at 20 percent, in daylight.
- So yes, cloud cover alone gives a number, in under a second, with 60 lines of Python. What it
  cannot give: the moon (no moon phase or altitude in the API) and whether the forecast was right.
  Tonight's answer is the dull one, and it could not be checked against the sky.

Verdict: works, as a screen. A real version needs moon altitude added (computable locally) and a
week of forecasts kept beside satellite cloud to say whether 20 percent is the right line.
