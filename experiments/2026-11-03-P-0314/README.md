# P-0314 Fed cuts and the systems book's 200-day filter

P-0304 found Bank Rate cuts come in downtrends. Does the same hold for Fed cuts, so that the systems book's SMA200 filter keeps SPY
flat before most of them?

Data: FRED DFEDTARU (target upper bound, keyless CSV, from 16 Dec 2008), 11 cuts (2019 x3, 2020 x2, 2024 x3, 2025 x3; the 2008 cuts
predate the series). SPY daily adjusted closes from Yahoo's chart API. Decision day = last SPY session before FRED's effective date.
`check.py`, `results.json`.

| | count of 11 |
|---|---|
| SPY above SMA200 | 9 |
| 20-day return positive | 8 |
| both | 8 |
| RSI(5) below 30 (the book's buy) | 1 (18 Dec 2024, RSI 16.3) |

Mean SPY return over the 20 sessions after: +0.03%. The two below SMA200 are the March 2020 emergency cuts.

Verdict: works. The answer is the opposite of the MPC one: Fed cuts since 2019 mostly land in uptrends (8 of 11), so the 200-day filter
does not hide them; what keeps the RSI(5) book out is that SPY is rarely oversold on a cut day (1 of 11). Eleven events, so
this is a description of the record, not a tested edge.
