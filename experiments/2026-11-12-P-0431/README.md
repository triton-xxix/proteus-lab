# P-0431: the systems book's eight RSI(5) closes

12 Nov 2026, nightly probe loop, refill row 163. Tonight's two closes took the RSI(5) simple book from
+0.40% a trade (6 closed) to -0.20% (8 closed). `trades.py` pairs the opens and closes in
`systems/EVENTS.csv` (read only).

**Called shot (commit eee35226, after reading the desk's 38% line, scored as a coin).** Under a 5%
chance of 3 or fewer winners in 8 at a true 75% win rate. Hit: 2.7%.

| Market | In | Out | Open to open |
|---|---|---|---|
| SPY | 19 Oct | 22 Oct | -0.11% |
| QQQ | 15 Oct | 28 Oct | +0.78% |
| EWJ | 15 Oct | 28 Oct | 0.00% |
| EEM | 15 Oct | 29 Oct | -0.84% |
| SPY | 2 Nov | 5 Nov | +0.79% |
| SPY | 6 Nov | 10 Nov | +1.79% |
| QQQ | 2 Nov | 12 Nov | -2.17% |
| EWJ | 2 Nov | 12 Nov | -1.80% |

Eight trades, three winners, mean -0.195%, matching the desk's own -0.20% and 38%. Nothing open.

**Reading.**

- Tonight's two were the two longest holds in the book, bought 2 Nov and held eight sessions waiting for
  an RSI exit while the market fell. The rule has no stop and no time limit; these are what that costs.
- If the backtest's 75% win rate were true and trades were independent, 3 or fewer winners in 8 has a
  2.7% chance. At a true 65% it is 10.6%; at a coin flip, 36%.
- They are not independent. QQQ and EWJ went in and out on the same two days, twice. Counted as
  episodes there are about five, not eight, so 2.7% overstates the case against the rule.

**Caveats.** Eight trades against a 30-trade mark the rules fixed before the first one. This is a
reading of where the book stands, not a verdict: the kill check owns that and it says RUNNING.

**Next.** Close. Worth one line in the kill check's output some day: the count of distinct entry dates
beside the count of trades.
