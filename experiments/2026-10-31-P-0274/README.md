# P-0274: the systems book's RSI(5) rule around Bank of England rate changes

31 Oct 2026, nightly probe loop, refill row 52. Source: the Bank of England database's daily Bank Rate series IUDBEDR, pulled keyless as CSV (4,504 rows, 2 Jan 2009 to 29 Oct 2026) to `sandbox/boe-bank-rate.csv`.

Called shot before running: works, but with too few trades in the pre-change window to separate from the rest; I expected under 40 pre-window trades across the nine ETFs.

## One thing learned from the source, in four minutes

The database's CSV export is a URL with the series code in it (`_iadb-fromshowcolumns.asp?csv.x=yes&SeriesCodes=IUDBEDR&...`), and it returns the rate on every working day, so decisions that held the rate leave no mark. There were 28 changes in the 17 years, the last on 18 Dec 2025 to 3.75%. So "before an MPC decision" cannot be built from this file; "before a rate change" can.

## What I did

`bank_rate_split.py` reuses P-0243's backtest and control (the book's RSI(5) simple rule, next-open fills, 2009 on, `sandbox/p0082` data) and splits each trade by whether its signal day sits in the 5 trading days before a rate-change day. Control per bucket: 2,000 draws of random signal days from the same bucket's pool of days with the close above the 200-day average, next-open entry, holds drawn from the bucket's real trades.

## Measured

| bucket | trades | mean | win | control | excess | p |
|---|---|---|---|---|---|---|
| EWU, pre-change | 1 | too few | | | | |
| EWU, rest | 95 | +0.56% | 70.5% | +0.11% | +0.45% | 0.024 |
| SPY, pre-change | 3 | +1.78% | 100% | -0.04% | +1.82% | 0.014 |
| SPY, rest | 115 | +0.76% | 77.4% | +0.24% | +0.51% | 0.002 |
| all nine, pre-change | 26 | +1.37% | 80.8% | -0.10% | +1.47% | 0.000 |
| all nine, rest | 940 | +0.63% | 75.1% | +0.21% | +0.42% | 0.000 |

The pre-change window is 28 changes times 5 days, about 140 days per symbol out of about 4,500, and it catches 26 of 966 trades across the basket. Those 26 did about twice as well as the rest and their random control was slightly negative, but 26 trades with a mean hold of 4.5 days is not a result, and the UK ETF the question was really about had one trade in the window. Nothing here changes the book.

## Verdict

works, as a build: it runs, the split is clean, and the answer is "cannot tell at n = 26, and n = 1 on EWU". What would make it a result: the full MPC decision calendar (about 8 a year, so 140 decisions, five times the days), which the Bank publishes as a page rather than a series and is a different pull.
