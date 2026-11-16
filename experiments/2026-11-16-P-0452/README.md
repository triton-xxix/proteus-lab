# P-0452: insider purchase clusters (3+ insiders), 21 trading days after filing, against SPY

Called shot: median excess between -2% and +2%, mean pulled up by a few small caps. Missed.

## What ran

- SEC's quarterly Form 345 data set returned 403 to a User-Agent without a contact address. I
  will not put Luke's address in a request, so EDGAR direct is blocked keyless.
- OpenInsider's screener with a 1 Jul to 30 Sep 2026 range returned 500 blank rows
  (`sandbox/p0452-oi.html`), so the date-range route is broken from here.
- OpenInsider's latest-cluster-buys page worked: 100 clusters filed 16 Sep to 16 Nov 2026. Kept the
  ones with at least 3 insiders, open-market purchases, filed by 14 Oct so 21 trading days of
  prices exist: **10**.
- Yahoo daily adjusted closes (a full browser User-Agent drew 429s; the plain one the desks use
  worked). Entry the first close after the filing date, exit 21 trading days later, SPY on the
  same two days. `clusters.py`, `results.json`.

## Result

| | value |
|---|---|
| clusters scored | 10 of 10 |
| median 21-day return minus SPY | **-14.6%** |
| mean | -11.5% |
| beat SPY | 3 of 10 |

Worst: ACCV -27.1, BBD -24.9 (22 insiders), HELP -22.5, RWT -21.3. Best: PRHI +6.9, DKS +6.8.
GME, the largest cluster by value ($99m, 5 insiders), -4.0.

## Verdict

Works as a measurement, on ten clusters from one month, which is far too few to call a signal in
either direction. Clusters filed in late September and early October 2026 lagged SPY badly. The
real test needs a quarter of Form 4s, which needs either SEC access with a contact header or the
screener's date range working.
