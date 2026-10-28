# P-0244: skip the RSI(5) book's calm-market trades?

**Question.** P-0243 found the book's trades after a VIX close under 15.2 earn +0.17% and do not beat luck.
Does skipping them, with the cut set walk-forward and costs charged, improve the book?

**Rules, fixed before the run.** The book as in P-0243 (close above 200-day average, RSI(5) under 30, buy
next open, exit next open after RSI(5) above 50; nine ETFs; 2009 on). Skip when the signal-day VIX close is
under that year's cut: the lower tercile of every VIX close from 1990 to the end of the year before.
0.05% a side on every trade. Growth: nine equal sleeves, each compounding its own trades.

**Called shot.** not-worth-it at 0.6: drops about 20% of trades, lifts the net mean by about 0.1 points,
lowers total growth. Hit on all three.

**Numbers.**
- Walk-forward cuts stayed between 14.7 (2020) and 16.1 (2012-13).
- Book: 966 trades, net +0.554% a trade, sleeves average 1.80x.
- With the skip: 743 trades (23.1% dropped), net +0.649% a trade, sleeves average **1.70x**.
- Kept trades against filtered random entries in the same VIX regime, net of cost: +0.649% v +0.198%, p 0.000 (2000 draws).

**Reading.** The skipped trades are weak but still positive after costs (+0.17% gross, about +0.07% net), so
cutting them raises the average and lowers the money. The book is long-only and spends most of its time
flat, so idle capital is not a cost here. A skip would earn its place only if the freed capital went
somewhere better on those days, which is a different probe. The book stays as registered.

**What I did not do.** No equity-curve drawdown comparison; no 10,000-draw control; sleeves do not share
capital, which overstates growth for both versions equally.
