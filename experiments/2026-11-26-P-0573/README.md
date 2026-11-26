# P-0573, Yahoo 5-minute bar revisions, leg one

Pulled 26 Nov 2026 about 23:36 UTC (exact time in `leg1/summary.json`): v8 chart, range=60d, interval=5m, for the 12 stocks in `edges/scan/scan.py`. Raw JSON for each symbol is in `leg1/`, about 410 kB each.

## What came back

- 12 of 12 pulled, no errors. Each has 4,681 bars, 2 Sep 13:30Z to 25 Nov 21:00Z: 60 sessions of 78 bars plus a closing 21:00 stamp. 26 Nov is US Thanksgiving, so there is no session for that day.
- 19 null closes in every symbol. 16 of them share timestamps across all 12: one unbroken hole, 5 Nov 17:15 to 18:30Z (80 minutes, 16 bars). It looks like a hole in Yahoo's feed, not a halt in any one stock. The other 3 nulls per symbol differ by symbol.
- So the scanner's 5 Nov session is 16 bars short on every symbol. Rules that read the 17:15 to 18:30 window (VWAP after 11:00 ET, afternoon direction) saw a gap there in every ladder that used 5 Nov.

## Leg two (pre-registered here, before it can be known)

Run `pull.py` again into `leg2/` after 27 Nov 23:00Z, then diff each bar that sits in both pulls (OHLCV, by timestamp). Count the changed bars in two groups: the last five sessions before leg one, and bars older than a week. Question: do recent bars get revised more often than old ones, and does the 5 Nov hole get filled? Called shot: under 1% of bars change in either group, and the hole stays.

`nulls.py DIR` lists the null timestamps shared by every symbol.
