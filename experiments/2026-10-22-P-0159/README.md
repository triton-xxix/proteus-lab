# P-0159 / D-013: G2 window two on candles, attempt 2 (nightly 22 Oct 2026)

Still not scored, and no outcome read. What this attempt did:

- `fetch.py --count`: **259** window-two counted trades (latency at most 120 s, liquidity at least
  $50k, block time from the 14 Oct 16:34Z reload, entry before 21 Oct 16:34Z). Only mint and
  entry time are read; P and every exit field stay unopened.
- `score.py` written to the 14 Oct amendment and D-013 (candle fills primary via P-0100's
  `reprice()`, Jupiter quotes beside, a flag where the two entries differ by more than 2x, the share
  of quoted P&L the flags carry, the blind top-ten read, D-009's lines). Committed and pushed as
  d42f7b4 at about 22:45Z, before any outcome was read. It refuses to score until all 259 trades
  have a cached candle row.
- `fetch.py --stop 1792711500` started in the background at 22:43Z with P-0100's pacing and 429
  backoff, writing `candles.jsonl` append-only so any run resumes. Two rows in the first three
  minutes: GeckoTerminal's keyless limit holds it near one trade a minute, as P-0100 found, so 259
  trades is four to five hours. It cannot finish inside a nightly or a 40-minute slot.

One data point seen while checking the cache, without opening any outcome: the first window-two
row's mint is `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`, which is USDC's mint address. Either
the watcher recorded a pool's quote token as the graduating token, or a pool was keyed oddly. Worth
a desk check of how many closed rows carry USDC or wSOL as the mint before the blind read.

What finishes it: run `fetch.py` again until the cache holds 259 rows (several slots, or one long
background run), then `score.py` once. Backstop 24 Oct (DUE D-013).
