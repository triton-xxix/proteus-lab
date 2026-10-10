# P-0109: what a Binance delisting notice does to the price

Date: 2026-10-10 (run just after midnight), nightly probe loop. Script `notices.py`, rules in its docstring;
every row in `results.json`. Keyless: Binance's public announcement list and spot 5-minute klines.

## Result (notices from about Nov 2025 to Oct 2026; 55 tickers, all priced)
| | Tickers | First 5 min | 24 h | 7 days | Fell by 24 h | Share of the 24 h fall avoided by selling at +5 min |
|---|---|---|---|---|---|---|
| Delisting notice | 51 | -13.2% | -19.7% | **-36.4%** | 45 | 0.48 (median, 45 that fell) |
| Monitoring tag | 4 | -7.9% | -11.4% | -19.4% | 4 | 0.43 |

All medians. Delisted pairs' history is still served before the removal date, so nothing was missing.

## What it means
A delisting notice is not a one-candle event: the median coin keeps falling for a week, -36% by day
seven, and roughly half of the first day's fall happens inside the first five minutes. A holder who
sells five minutes after the notice saves about half of the 24-hour damage and most of the week's. A
handful jump instead (VIC +76% in 24 h, VOXEL +21%), so "sell on notice" is a rule of thumb, not a law.

## Limits
- "+5 min" is the close of the 5-minute candle containing the release, so between 0 and 5 minutes after.
- Upbit's warning designations were not pulled tonight: out of time, not blocked.
- The Grinder does not hold listed coins, so this is a fact for the record and for a holder, not a book.

## Verdict
Works, measured.
