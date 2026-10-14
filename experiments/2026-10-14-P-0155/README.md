# P-0155: pull-at-5x against holding, on graduation watcher trades

Question (harvest H-0259): how often does a fresh pump.fun graduation reach 5x, and does selling at
5x beat holding?

Data: `grinder/graduates/closed.jsonl`, 14 Oct 23:4xZ. The watcher samples every 15 s for 30 minutes
only, so the 24 h hold in the question is not in the data; the hold here is exit B (sell at 30 min).
Raw moves before costs. Pull rule sells at exactly 5x when the sampled max reaches it, an upper bound.

| Set | n | reached 5x | reached 2x | hold B mean | pull mean | pull minus hold |
|---|---|---|---|---|---|---|
| counted (latency <= 120 s, liq >= $5k) | 10,811 | 494 (4.6%) | 3,122 | -26.5% | -30.5% | -4.0 pts |
| liq >= $50k (G2 line) | 867 | 25 (2.9%) | 33 | +30.7% | +6.3% | -24.4 pts |

Pulling at 5x loses to holding because the tokens that reach 5x mostly stay there: 23 of the 25 G2
hitters were still above +488% at the 30-minute mark (two went to -99%). A real pump does not hold
5x to 30 minutes that often. This matches the G2 top-ten finding of the same day
(`experiments/2026-10-14-g2-top10`): Jupiter's first quote is 12x to 59x below the candle on most of
the big winners, so "reached 5x" here is largely a bad entry price, not a move.

Shot said about 2% reach 5x: 4.6% on the counted set, 2.9% on G2. Missed on the counted set.

What this does not answer: the 24 h question, and the rule on real fills. Both need candle entry
prices, which D-013 (G2 window two, candles primary) and P-0152 will carry. Next: close.
