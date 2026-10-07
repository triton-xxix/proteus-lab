# B-kevin-davey digest (12 videos, 23 ideas)

**Verdict:** Thin on complete strategies. One idea has fully stated rules and a checkable claim. The rest are Kaufman fragments (efficiency ratio, adaptive average, filter) and Davey intraday futures systems with hidden rules. The process material is worth more than the strategies.

**Test first:**
1. B-01 Efficiency ratio ranking of our 28 ETFs: bonds should rank most trending, indices least. Free data, informs P-0084 and the RSI(5) index book.
2. B-02 Breakout vs moving average vs regression vs exponential average at 80 days: Kaufman says breakout wins, EMA worst. Cheap extra arms on P-0084, but we write the rules.
3. B-03 Sign of the 200-day change against the 200-day average as a SPY filter: fully specified, extends P-0082.
4. B-04 Kaufman adaptive average (60-day window, fast end 8) with an efficiency gate against a plain average: slow end and threshold missing.
5. B-05 Quit-rule menu (12 months unprofitable, 1.5 times max drawdown, 3 years live) replayed on our forward curves: ties to the kill check.

**Frameworks worth copying:**
- Davey's pipeline: walk-forward, a marked live phase from a fixed date, 50-trade minimum, and judging a filter by on-versus-off across 44 markets, not one chart.
- Live versus ideal reconciliation, a weekly correlation table, and constant one-unit sizing so growth is not flattered.
- Where AI belongs: ideas, code porting, data cleaning, monitoring, two-model audits; not sizing, optimising or validation. Do not test the same data twice.

**Not testable on free daily data:**
- B-21 ES VWAP/ATR system: needs intraday bars; core rules withheld.
- B-22 Session-open slippage delay: needs intraday or tick data.
- B-13 ER-driven entry timing: needs intraday bars.
- B-23 Twelve-strategy micro portfolio: rules unpublished.
- B-20 AI switching scheme: nothing disclosed.

**Salesmanship noticed:**
- Nearly every video funnels to a free-algo email list, the September masterclass (650 dollar early-bird deadline), his book, or the strategy factory workshop.
- Code and exits are withheld to sell the book; the masterclass teaser covers up the approach.
- Out-of-sample in titles means walk-forward on developed data.
- Live results cover seven to eight months and end on a good month. His narration says hypothetical and real gains match while the chart shows them apart.
- The crude oil system is labelled AI inspired but shows plain ADX and momentum rules.
