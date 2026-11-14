# P-0446: the Munich fog flag out of sample, and a low-cloud flag

**Question.** P-0445 found fog-morning days (FG or FZFG in an EDDM METAR before 10Z) ran 0.79 C warmer on
the ICON lead-1 city day high over Nov 2025 to Oct 2026. Does that hold on 1 to 13 Nov 2026, and does a
low-cloud flag (BKN, OVC or VV at or below 500 ft before 10Z) catch more of the big warm misses?

**Method.** `oos.py`, same sources and rules as P-0445. Both flags scored out of sample (13 days) and on the
in-sample year, so they are compared on the same days.

**Called shot.** works at 0.5 (coin): shot after looking at the 8 to 10 Nov hourly METARs in refill 168, so
9 Nov was already known. Number called: gap -1.0 C, about 3 fog days.

## Numbers

| flag | sample | flagged days | flagged mean err | other mean err | gap | 2.5 C+ warm misses caught |
|---|---|---|---|---|---|---|
| fog | 1 to 13 Nov 2026 | 3 | -0.93 | -0.23 | **-0.70** | 1 of 1 |
| low cloud <=500 ft | 1 to 13 Nov 2026 | 5 | -1.18 | +0.10 | **-1.28** | 1 of 1 |
| either | 1 to 13 Nov 2026 | 6 | -0.98 | +0.11 | -1.10 | 1 of 1 |
| fog | year | 58 | -0.49 | +0.30 | -0.79 | 7 of 17 |
| low cloud <=500 ft | year | 67 | -0.70 | +0.37 | **-1.07** | 9 of 17 |
| either | year | 89 | -0.57 | +0.41 | -0.98 | 11 of 17 |

## What it means

The fog gap held its sign and size out of sample (-0.70 against -0.79), but on three days, and 9 Nov alone
(-3.6) carries it; that day is the one that started the question, so the out-of-sample leg is weak. The
low-cloud flag is the better flag on both samples: a wider gap (-1.07 on the year, -1.28 in November) and
more of the big misses caught (9 of 17 against 7). Fog plus low cloud catches 11 of 17 at the cost of
flagging a quarter of the year.

## What I did not do

- No permutation test for the low-cloud flag on the year (P-0445's within-month test was for fog only).
- One station. Whether a 500 ft cloud base before 10Z marks a warm forecast at Heathrow or Paris is open.
- No prices: no check that a 1 C cold shift moves a bucket market.
