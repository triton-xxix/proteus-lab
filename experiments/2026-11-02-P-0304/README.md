# P-0304, P-0292's MPC cut bucket out of sample (2 Nov 2026, nightly refill from source 73)

P-0292 (Trials, today) found RSI(5) next-open trades in the 5 trading days before a Bank Rate cut beat the
rest by about +1.9 points on all nine ETFs, 2009 onwards (17 trades, perm p 0.034), and said it was too
few meetings to trade. The Bank's mpcvoting.xlsx already holds every meeting from 1997, so this reruns
P-0292's own script on the meetings it filtered out: 1997 to 2008. `oos.py` reads that script, swaps the
date window (asserted swaps, nothing else changed) and writes `results.json` and `meetings.json`.

Meetings 1997 to 2008: 139, of which 23 cuts, 18 hikes, 98 holds; 91 split votes.

| bucket | all nine trades | mean | minus rest | perm p | EWU trades |
|---|---|---|---|---|---|
| cut | **1** | (too few) | | | 0 |
| hike | 23 | +1.40% | +0.45 | 0.39 | 3 |
| hold | 54 | +0.24% | -0.71 | 0.04 | 6 |
| split | 40 | +0.76% | -0.20 | 0.64 | 4 |
| unanimous | 38 | +0.38% | -0.57 | 0.15 | 5 |
| rest (no meeting near) | 357 | +0.95% | | | 44 |

The answer: the cut bucket cannot be tested out of sample. 23 cuts gave 1 trade, because the cuts of
1998, 2001 to 2003 and 2008 came in falling markets, where the systems book's 200-day filter keeps it
flat. So the rule never sees most cuts. That is a finding about the +1.9 too: it rests on the 2009 to
2026 cuts (2009, 2016, 2020, 2024 to 2026), several of them in uptrends, and there is no earlier record
of the same thing to check it against.

Nothing else holds up either: hike +0.45 (p 0.39), and the hold bucket is worse than the rest (-0.71,
p 0.04, one test of five, not adjusted). Split v unanimous +0.38, p 0.47.

Verdict: works, and P-0292's "close" stands: no MPC bucket to trade on, and the cut effect has no
out-of-sample test available in UK data.
