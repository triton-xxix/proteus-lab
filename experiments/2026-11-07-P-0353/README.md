# P-0353: how much of Heathrow's METAR-high gap is sampling alone? (7 Nov 2026)

Deepen of P-0352, which ruled out truncation. P-0346 found the whole-degree EGLL METAR high 0.93 C under
SYNOP TX (06 to 18 UTC). Question: if you only look at the air twice an hour, how far under the true max do you
land, using the station's own 10-minute tenths so the sensor is held fixed?

Shot: works at 0.65; half-hourly max 0.25 C under the full 10-minute max, that 0.3 C under TX.

## Method, and one change

`sampling.py`, October 2026, cached Ogimet 10-minute SYNOPs for 03772, 06:00 to 18:00 UTC. **The cache holds
no :50 reports at all** (minute counts in `results.json`), which is also why P-0352 matched only half its
METARs. So the half-hourly sample is :00 and :30, the same density as EGLL's :20 and :50 METARs but offset.
28 of 31 days had every slot (the skipped label in the output still says ":20 or :50"; it means the :00/:30
slots).

## Numbers (`results.json`)

| | shot | measured (28 days) |
|---|---|---|
| full 10-minute max minus half-hourly max | 0.25 | **0.16 C** (sd 0.23) |
| SYNOP TX minus full 10-minute max | 0.3 | **0.19 C** (sd 0.20) |
| half-hourly max, rounded, minus TX | | **-0.33 C** (sd 0.34) |

## What it says

Sampling twice an hour and rounding, on the station's own readings, puts the high about 0.33 C under TX.
P-0346's METAR gap was 0.93. So about a third is sampling and the TX being a peak inside the 10 minutes;
about 0.6 C is left, and it sits in the METAR's own reading. P-0352 found METAR unbiased against the tenths
over all hours (-0.02), so the remaining candidate is a METAR that runs cold at the warm part of the day,
which an hour-of-day split of P-0352's matched minutes would show.

## Not done

:00/:30 stands in for :20/:50. One month. P-0346's 0.93 was Sep to Oct, this is October only.
