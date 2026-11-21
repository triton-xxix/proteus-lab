# NOAA Kp three-day forecast, saved 20 Nov 2026 about 12:35Z, to be scored after 23 Nov

Refill row 201. The file is `forecast-2026-11-20T1243Z.json` (the 1243 in the name is my misread
of the clock; the fetch was about 12:35Z, between P-0504's 12:33Z run and P-0506's 12:38Z), straight from
`services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json`. It is committed now, before
the outcome, so the commit timestamp is the proof.

**What the forecast says.** 17 predicted three-hour slots, 21 Nov 00Z to 23 Nov 00Z, Kp 1.33 to 2.67,
mean 2.08. None at 5 or more (no G1 flagged). Four estimated slots for 20 Nov 12Z to 21Z read 1.67 to
3.00. Last observed slot: 20 Nov 09Z, Kp 0.67. The previous eight days held one G1 (19 Nov 00Z, Kp 5.00).

**Pre-registered score (queued as a probe, opens 23 Nov; DUE D-030).** On the 17 predicted slots,
against the observed rows in the same file read on or after 23 Nov 03Z:
- mean absolute error of NOAA's prediction;
- against two baselines: persistence (0.67 for every slot) and the mean of the 56 observed slots
  13 to 19 Nov in this snapshot;
- did any observed slot reach 5 or more, and was it flagged (it was not, so any 5 is a miss).
A pass line: NOAA beats both baselines on mean absolute error. No money, no rule changes; a forecast
book outside football and Munich if it is worth keeping.

## The 27-day outlook, saved 21 Nov 2026 about 00:05Z (refill row 207, DUE D-032)

`27-day-outlook-2026-11-21.txt`, from `services.swpc.noaa.gov/text/27-day-outlook.txt`. It was issued
16 Nov 02:33Z (the file is weekly), so its rows for 16 to 20 Nov were already partly knowable when I
saved it and do not count. **Scored rows: 21 Nov to 12 Dec, 22 days**, its "Largest Kp Index" column
(whole numbers; in the scored window it calls 5 on 27 Nov, 28 Nov and 4 Dec, and 2 to 4 on the rest).

Pre-registered score, on or after 13 Dec: observed daily largest Kp (max of the eight three-hour values,
rounded down to a whole number to match the table) for each scored day. Source: `text/daily-geomagnetic-indices.txt`,
which I believe keeps about 30 days (not checked tonight; if it keeps fewer, read it on 4 and 13 Dec).
- mean absolute error of the outlook against a flat climatology: the median of the observed daily
  largest Kp over the same 22 days (computed after, which flatters the baseline, said now);
- of its three days at 5, how many reached 5 or more; of the 19 others, how many did.
Pass: the outlook beats the flat line on mean absolute error. No rule change rests on it.
