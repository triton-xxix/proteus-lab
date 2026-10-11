# P-0120 (D-004): why P-0088's trend baseline had Sharpe 0.35 where P-0084 recorded 0.28

**Cause found, from the code.** `experiments/2026-10-07-P-0088/p0088.py`, `portfolio_n()`, works out
`cost = turnover * COST` on line 92, then returns `(held * rets).sum(axis=1)` on line 93 without
subtracting it. P-0084's own `portfolio()` returns `... - cost`. So every P-0088 portfolio is gross of
costs, and P-0084's 0.28 is the net figure.

**The numbers agree with that.** P-0088's all-28 line beats P-0084's by about one point in every
calendar year, 2008 to 2026 (2008 6.6 v 6.0, 2016 -19.8 v -21.0, 2025 15.0 v 13.7). CAGR is 4.23 against
3.19 and vol is the same (15.25 v 15.26). A steady drag of that size is what 0.0005 a unit costs at an
average gross of 2.83 with weekly rebalances. Different data would not look like that.

**What the old note got wrong.** P-0088 blamed a shuffle-offset edit to `p0084.py`. The only change
between P-0084's script commit (d9ae84e) and its results commit (72c25ae) clamps the permutation start
index. It touches the luck test, not the real Sharpe. The README's "the committed script, run again,
gives 0.35" really meant p0088's copy of the portfolio, not p0084.py.

**What stands.** P-0084's headline (TSMOM Sharpe 0.28, breakout 0.33, both under 60/40's 0.79) is
right as recorded. P-0088's comparison of top-14 against all-28 is gross on both sides, so its sign is
probably right. But the top-half rule trades more, so net of costs it would look worse, not better.
P-0088's verdict (not worth it) only gets stronger. P-0088's files are left as committed; this note is
the correction.
