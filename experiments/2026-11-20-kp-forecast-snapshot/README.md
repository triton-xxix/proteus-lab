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
