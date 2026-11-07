# P-0355: a station change at Munich airport on 19 Apr 2026? (7 Nov 2026)

From refill row 112 (`experiments/2026-11-07-refill112/meta.py`): the historical KL zip for 01262, generated
17 Jun 2026, ends its 2011 PT 100 sensor row on 19 Apr 2026. P-0347 saw the EDDM METAR high minus TXK move
from -0.22 (2023) to +0.04 (2026). Question: is that a station change on 19 Apr?

Shot: works at 0.55; a shift of about +0.25 C at 20 Apr 2026 against under 0.1 C for the same split in 2025.

## Answer: no, and the date was a misreading

The recent zip's metadata, generated 6 Nov 2026, carries the same row (PT 100, 2 m, from 21 Sep 2011) to
**5 Nov 2026**. The end date is the file's last data day, not a change. The site table has no change since
2011 either.

## Numbers (`results.json`, cache only, P-0347's files)

Gap = METAR whole-degree high minus TXK. Split each year at 20 Apr (before 1 Jan to 19 Apr, after to 31 Oct).

| year | before | after | shift |
|---|---|---|---|
| 2021 | -0.25 | -0.11 | +0.14 |
| 2022 | -0.18 | 0.00 | +0.19 |
| 2023 | -0.19 | -0.23 | -0.04 |
| 2024 | -0.14 | -0.02 | +0.12 |
| 2025 | -0.11 | +0.09 | +0.20 |
| 2026 | +0.03 | +0.06 | **+0.03** |

Shift 2021 to 2025: mean +0.12 (range -0.04 to +0.20), the ordinary seasonal swing. 2026's shift is +0.03,
smaller than usual, the opposite of a break. My shot of +0.25 missed.

## What it says

The drift is gradual, already in the winter halves: -0.25, -0.18, -0.19, -0.14, -0.11, +0.03 from 2021 to
2026, about +0.05 a year with a jump into 2026. No station change behind it on DWD's side by its own metadata;
whether the METAR side (sensor, reporting software) changed is not in any file here.

## Not done

No METAR-side metadata. se about 0.035 a half-year, so the year-to-year steps are close to noise; the trend
across six years is not.
