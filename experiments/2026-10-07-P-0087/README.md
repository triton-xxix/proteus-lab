# P-0087: calendar events on daily SPY against random days of the same kind

Run 8 Oct 2026 00:08 BST, `p0087.py`, SPY daily as traded 1993-01-29 to 2026-10-07. Definitions
fixed in the script's docstring before the run; results in `results.json`. Controls are every
other day of the same weekday class, and a 5000-draw bootstrap of the same count from them.

| event | n | mean | winners | control mean | bootstrap p (mean at or above) |
|---|---|---|---|---|---|
| Fed statement day, close to close (2016-26, 85 scheduled meetings) | 85 | +0.03% | 46% | +0.06% | 0.58 |
| session before the statement (pre-Fed drift, daily) | 85 | +0.09% | 51% | +0.06% | 0.42 |
| three sessions into the statement | 85 | +0.16% | 51% | +0.16% | 0.51 |
| jobs-report Friday (first Friday of the month, 1993-26) | 405 | +0.15% | 59% | -0.05% (other Fridays) | 0.000 |
| weak Monday (Monday close below Friday's low), Monday close to Friday close | 355 | +0.71% | 66% | +0.15% (all Mondays) | 0.000 |
| weak Monday since 2009 | 184 | +0.69% | 63% | +0.15% | 0.000 |

## What it says

- **Fed days carry nothing on daily bars.** The decision day, the day before it and the three-day
  run-in all sit on top of ordinary days. The pre-FOMC drift in the literature is an intraday
  effect (the 24 hours before the statement); a daily close-to-close window cannot see it, and
  this run says so rather than finding a spurious one. Dates are the Fed's own, 2016 to September
  2026, scheduled meetings only; earlier years would need 23 more calendar pages.
- **Jobs Fridays are a real up-day.** First Fridays average +0.15% against -0.05% for the other
  Fridays, 59% up against 50%, and no bootstrap draw of 405 other Fridays matched the mean. The
  first-Friday rule is an approximation of the BLS schedule, so some of the 405 are not release
  days; that would dilute, not create, the effect.
- **The weak-Monday reversal reconciles with the claim.** +0.71% a trade from the Monday close to
  the Friday close (claimed about +0.6%), 66% winners, against +0.15% for an average Monday-to-
  Friday hold; since 2009 +0.69%. What this run does not separate: how much is "buy after any
  down day" (a generic dip effect the RSI(5) book already holds) and how much is the Friday-low
  condition. That is the next check, queued, along with the nine-ETF basket and the overlap with
  the systems book.

## Verdict

**works**: two of three calendar claims survive their controls on free daily data and the third
is honestly invisible at this resolution. Nothing goes into a book from this run.
