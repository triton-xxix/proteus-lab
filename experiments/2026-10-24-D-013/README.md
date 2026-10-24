# D-013: G2 window two, scored on candles with Jupiter beside

Smith, 24 Oct 2026. `window2.py` committed at 79aa98a (20:29) before any candle came back; the job
ran keyless against GeckoTerminal from 20:21 to 21:01 and wrote `RESULT.md` and `results.json`.
Candle cache `candles.jsonl` beside them. Rules in the script's docstring; method is P-0100's.

**Measured.** 259 counted G2 trades in the window (14 Oct 16:14:36Z to 21 Oct 16:14:41Z), 249
re-priced, 10 without candle data (3.9 percent, under the 10 percent line, so a verdict).

| read | n | expectancy per £100 | best 10 removed | at or below -50% | KEEP lines |
|---|---|---|---|---|---|
| candles, primary | 249 | -5.00 | -6.71 | 6.0% | fail |
| Jupiter quotes, same trades | 249 | +44.48 | -5.70 | 6.0% | fail |
| Jupiter quotes, all 259 | 259 | +42.77 | -5.47 | 5.8% | fail |

**The flag.** 6 of 249 entries had a Jupiter quote more than 2x off the pool's candle. Median
candle over quote 1.0058, so on almost every trade the quote was fine.

**The top-ten question, read blind.** Of the ten best trades on Jupiter, five are flagged. The top
five on quotes (+5,643, +3,771, +1,098, +938, +786 percent) read -2.0, +9.4, +10.7, +0.6 and +2.1
on candles. The other five (+24 to +57 on quotes) read +22 to +75 on candles: real, small. The
book's quoted edge is five quote errors in 259 trades.

**Against window one (P-0100, D-009).** Window one: -3.98 on candles against +45.75 on quotes.
Window two: -5.00 against +44.48. Same shape, independent week. This time even the quoted read
fails the best-ten line (-5.70), where window one passed it by 13 pence.

**So.** G2 stays KEEP withdrawn, nothing graduates (amendment 14 Oct, untouched). The second window
was the test of whether the first was a fluke of ten trades; it was not. Honest fills on the
graduation book lose about £5 per £100 at 20 minutes with a -50 percent stop, two windows running.
Nothing here changes a registered line.
