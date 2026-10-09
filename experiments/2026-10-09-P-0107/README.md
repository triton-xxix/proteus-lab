# P-0107: buy when Binance or Upbit announces a listing? (9 Oct 2026)

Verdict: **not worth it** for anyone who buys after the announcement is public.

Rules were fixed in `listings.py` before the run. 108 spot-listing announcements in the last 12
months; 68 had a market elsewhere to buy on beforehand (60 Upbit, 8 Binance). The other 40 were
brand-new coins with nowhere to buy before the listing. Coinbase and Crypto.com not covered (no
keyless feed with timestamps).

| | Upbit (60) | Binance (8) |
|---|---|---|
| Move from announcement to the first buy a script could make (+5 min) | median +18%, up 98% of the time | median +7% |
| Bought at +5 min, sold 1 hour later | median -0.4% | -1.2% |
| Sold 24 hours later | median -11%, 18% of trades up | -5%, 1 of 8 up |
| Sold 7 days later | median -19%, 14% up | -14%, none up |
| Highest price in the first 24 h (hindsight, not tradable) | median +11% | +2% |
| Move in the 24 h before the announcement | median +2% (mean +52%, a few leaked hard) | -2% |

What it means: the pop is real and it is over inside five minutes, taken by bots reading the feed
within seconds. After that the coin drifts down for a week. The profitable side is being out, or
selling a coin you already hold into the pop. Betting on the fall needs short selling or
derivatives, which UK retail cannot use. Caveats: 5-minute candles, so the first minute is not
resolved; Binance sample is small; costs assumed 0.5% round trip.
