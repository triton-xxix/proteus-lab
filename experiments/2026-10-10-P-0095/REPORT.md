# P-0095: weak-Monday reversal, the harder test

Date: 2026-10-10, nightly probe loop. Follows P-0087 (SPY since 1993: +0.71% a trade, not separated from a
generic dip). Script `p0095.py`, numbers `results.json`. Rules fixed in the script's docstring before it ran.

## Called shot
On the nine-ETF basket the edge stays positive against random entries, but sits within 0.2 points of a
generic "close below yesterday's low, any weekday, hold four sessions" dip, and more than half of weak
Mondays in an uptrend are also book-1 RSI(5) entries, so it adds little.

## Result (2009 to 2026, nine ETFs pooled, gross of costs, not dividend-adjusted)
| Set | Trades | Mean a trade | Winners |
|---|---|---|---|
| Weak Monday (close below Friday's low, hold to Friday) | 1,947 | **+0.448%** | 56.0% |
| Down Monday, not below the low (control 1) | 1,490 | +0.134% | 54.7% |
| Any weekday below yesterday's low, 4 sessions (control 2) | 10,713 | +0.229% | 56.0% |
| Random weekday entries, 4 sessions, same counts per market (5,000 draws) | | +0.153% | |
| Weak Mondays that are also book-1 entries | 265 (13.6%) | +0.236% | 57.0% |
| Weak Mondays that are not | 1,682 | +0.481% | 55.8% |

Luck test: no random draw reached the weak-Monday mean (p below 0.0002). Every market is positive; SPY
+0.69 and QQQ +0.79 lead, EWG +0.11 trails.

## Where the called shot went wrong
- The gap to a generic dip is 0.22 points, just over the 0.2 I set: the Monday matters a little, and the
  "below the low" matters more than "down" (control 1 is barely above random).
- The overlap with book 1 is 13.6 percent, not over half, and the trades book 1 would not take are the
  better ones. I expected redundancy and found something nearly separate.

## Caveats
The nine ETFs move together, so many of the 1,947 trades are the same week counted several times; the
bootstrap treats them as independent and overstates the certainty. No costs: at a few basis points a
round trip, +0.45 survives; at 0.2 percent it halves. Gross paper numbers on history, not a book.

## Verdict
Works, as a measured effect: it survives the harder controls on paper and is mostly separate from book 1.
Whether it earns a paper book is a pre-registration question with its own kill line, not something to
decide inside a probe. Written up for that, not registered.
