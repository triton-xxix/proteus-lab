# P-0153: long-only laggard of a matched crypto pair

Question (from harvest H-0254, a vault pairs-trading reel): on public hourly candles, does buying the
laggard of a correlated pair when the spread passes 2 sigma beat random holds of the same coin after
0.2% round-trip fees?

Rules were written into `pairs_laggard.py`'s docstring before the first run: 12 coins, 90 days of
hourly Binance closes (keyless data-api.binance.vision), 30-day formation (correlation >= 0.70 picks
11 pairs), 60-day trading window, z on a 168 h rolling spread, enter at |z| >= 2, exit at z back
through 0 or 48 h, 0.1% a side. Benchmark: 500 books of random entries on the same coin with the same
hold lengths.

Result (`results.json`), window 17 Jul to 14 Oct 2026, trading 16 Aug to 14 Oct:
- 144 trades, mean +1.49% each, median +0.18%, win rate 53%, mean hold 39 h, 89 of 144 hit the 48 h stop.
- Random entries, same coins and holds: mean +0.68%. 27 of 500 shuffled books beat the real mean, p 0.054.
- Every one of 11 pairs positive on the mean; ETH-XRP the weakest (+0.08%), XRP-DOGE the best (+3.67%).
- BTC-ETH: 11 trades, +12.8% summed. My shot said about -5% against a hold; missed, and that was a
  different comparison than the one I ran.

Caveats, in order of weight: the 11 pairs share coins and their trades overlap in time, so the 144 are
far from independent and p 0.054 is too kind; it is one 60-day window in a rising market (random holds
earn +0.68% on their own); the median trade is +0.18%, so a handful of big reversions carry the mean;
fills are at the hourly close with no slippage. Not run: cointegration tests, short legs, a second window.

Next: deepen. Same frozen rules on the previous, non-overlapping 90 days (out of sample), and a
block shuffle by day so overlapping trades cannot inflate the p-value.
