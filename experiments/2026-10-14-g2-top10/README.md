# G2's top ten: where the edge sits, and whether it is real

Interactive, 14 Oct 2026, on Luke's question "how do we identify the top 10". Script `top10.py`,
output `result.json`. Read-only against the book.

**Measured.** 623 counted G2 trades, +£38.31 per £100. The ten best carry 86 percent of the P&L;
without them the book reads +£5.29. Nothing known at entry marks the ten out: median liquidity
$150k against $186k for the rest, latency 7.75 s against 7.8 s, spread across every weekday and
every liquidity bucket above $100k.

**What they are.** Seven of the ten sit in P-0100's 403 re-priced trades. On each, Jupiter's quoted
entry was 12 to 59 times below the pool's own 1-minute candle at that minute (entry_ratio 12.4 to
58.8 in `experiments/2026-10-10-P-0100/results.json`). Scored on candles the seven closed at the
time stop between -1.96 and +3.69 percent. The "+5,800 percent" trade is a quote that was wrong at
entry; the token did not rise. The other three (vMLycAbq, E7GozZ1X, 94F9U1K2) entered after P-0100's
cut-off and are not yet re-priced; P-0152 covers them with window two.

**So.** There is no top-ten pattern to find and no wallet to follow on these. The real finding is
the quote error itself: at migration, Jupiter's price can lag the pool by an order of magnitude.
Window two (watcher reloaded 14 Oct 16:34Z, DUE D-013) is scored on candles as primary, with every
entry flagged where the quote and the candle differ by more than 2x.
