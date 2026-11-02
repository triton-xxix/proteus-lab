# P-0292: P-0280 split by what the MPC did

**Question.** P-0280 found nothing in the pooled pre-meeting window (175 MPC decisions since 2009). Does it
hide something once meetings are split by what they did (hike, cut, hold) or by whether the vote was split?

**Method.** `mpc_bucket_split.py` reads the Bank Rate sheet of the Bank's `mpcvoting.xlsx`
(`sandbox/boe-mpcvoting.xlsx`, pulled keyless 1 Nov) with zipfile: column B the date, C the rate decided,
one column per member holding the rate they voted for or "Increase"/"Decrease". Decision kind against the
previous meeting's rate; split = any member cell differing from the decided rate. The systems book's RSI(5)
next-open trades whose signal day sits in the 5 trading days before a meeting carry that meeting's labels.
Per bucket: the random-entry control from P-0280 (1,000 draws) and a permutation test of the bucket against
trades outside every pre-window (5,000 shuffles). `meetings.json` holds the 175 labelled meetings.

**Numbers.** 175 meetings: 16 hikes, 12 cuts, 147 holds; 79 split votes (45%); 8 or 9 voters.

| | EWU trades | EWU mean | all nine trades | all nine mean | minus rest | perm p |
|---|---|---|---|---|---|---|
| hike | 1 | too few | 9 | +0.41% | -0.20 | 0.78 |
| cut | 0 | too few | 17 | +1.89% | +1.28 | **0.034** |
| hold | 20 | +0.61% | 204 | +0.73% | +0.12 | 0.54 |
| split | 7 | +0.21% | 92 | +0.92% | +0.32 | 0.23 |
| unanimous | 14 | +0.71% | 138 | +0.72% | +0.11 | 0.62 |
| rest (no window) | 75 | +0.54% | 736 | +0.61% | | |

Split minus unanimous: EWU -0.50 points (p 0.62), all nine +0.20 (p 0.55). The cut bucket also beats its
random-entry control (excess +1.97 points, p 0.001).

**Reading.** One bucket out of ten tests under 0.05 is about what chance hands out; the Bonferroni bar is
0.005 and the cut bucket misses it. Its 17 trades sit before 12 cuts across nine ETFs that move together
(2009, March 2020 and the 2024-25 easing), so the independent bets are fewer than 17. EWU itself, the UK
fund the idea is about, has no trade at all before a cut. Dissent changes nothing.

**Not done.** No count of distinct meetings behind the 17 cut trades, no leave-one-meeting-out, no
window other than 5 days, no SPY row (P-0280 had it).
