# C-testers digest (Algovibes, 5 videos)

Verdict: Thin for our data. All five videos test intraday Nasdaq futures. 15 ideas listed, four testable on free daily bars (C-05 to C-08), none with a complete trade rule. The value is in the methods.

Test first:
1. C-05 Fed decision day return and pre-Fed drift (priority 1). He reports +0.36% on 52 events, a one-in-eight luck match. Daily SPY/QQQ gives decades of events. Fix the definition first.
2. C-08 Quarterly exam gate (2). Cash for three months unless the past year passed. Pass mark unstated, so pre-register one. Try it on the RSI(5) book.
3. C-01 Opening range breakout, 30 minute box, NQ (2). Only survivor of a thousand settings, held out of sample and under four times slippage. Needs intraday bars.
4. C-04 Jobs-report fade held to 9:30 (2). +22,795 over 75 events, two of 10,000 random baskets matched. Needs 1-minute bars.
5. C-06 Jobs-day Friday weakness (3). -0.25% against +0.06%. He says it is not an edge; 25 years of daily data should settle it.

Frameworks worth copying:
- Same-trade random control: rerun the identical trade on random days, entries or directions 10,000 times, report where the real result sits.
- Freeze then judge once: rank by the weaker of two periods, never retune on the judge data.
- Break-even win rate plus pessimistic same-bar fill: ambiguous bars count as losses. Daily bars have the same trap.

Not testable on free daily data:
- C-01, C-02, C-03 (ORB, long-only skip-Monday version, news-day switch-off): 1 to 5 minute NQ bars, 2020 to 2026.
- C-04, C-12 (jobs fade, Fed press-conference reversal): minute bars around 8:30 and 2:00 to 3:30 pm.
- C-09 machine-learning timing filter: minute bars for ten markets plus VIX, about 75 dollars of paid data per the video.
- C-10, C-11, C-13, C-14, C-15: intraday, all lost after costs; skip.

Salesmanship noticed:
- Every video ends on a research lab link (lab.wisequant.app, price unstated) selling engine and code, plus a prompt to submit the next strategy.
- Results are one-contract dollars over a bull-market decade; the Monday rule was found by looking.
- The AI committee ends at +170 on 264 trades, tuned on seen history: a lead, not a result.
