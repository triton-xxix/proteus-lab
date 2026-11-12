# P-0430: the control P-0421 lacked

12 Nov 2026, nightly probe loop, refill row 162. P-0421 (earlier tonight) found every registered edge
rule under water with its best ten admission trades gone and read that as "a handful of trades". It
had no control. `control.py` matches every real trade 500 times with a random entry on the same symbol
and day with the same hold, either side (`scan.control_pool`, the scanner's own null), and asks the
same questions of the random lists.

**Called shot (commit 61f45b94).** works at 0.65: for at least 6 of 9 rules the best-ten share of gross
wins sits inside the random lists' 10th to 90th percentile band. Missed by one on the count (5 of 9),
and the miss is in the direction I did not expect: the other four are less concentrated than random.

| Edge | Trades | Best ten, share of gross wins | Random lists (10th to 90th) | To zero, share of trades | Profitable random lists, median |
|---|---|---|---|---|---|
| E-011 | 179 | 0.38 | 0.32 to 0.40 | 2.8% | 1.1% |
| E-012 | 157 | 0.31 | 0.35 to 0.45 | 5.7% | 1.3% |
| E-013 | 124 | 0.44 | 0.43 to 0.54 | 3.2% | 2.4% |
| E-014 | 157 | 0.44 | 0.47 to 0.59 | 1.9% | 1.3% |
| E-015 | 126 | 0.27 | 0.58 to 0.73 | 5.6% | 0.8% (7 lists) |
| E-016 | 179 | 0.33 | 0.33 to 0.43 | 1.7% | 1.1% |
| E-017 | 121 | 0.38 | 0.40 to 0.50 | 8.3% | 2.5% |
| E-018 | 180 | 0.35 | 0.33 to 0.42 | 3.3% | 1.1% |
| E-019 | 145 | 0.57 | 0.50 to 0.64 | 2.1% | 1.4% |

**Reading.**

- No rule is more concentrated than random entries. Five sit inside the random band and four below it.
  Ten trades supplying a third to a half of all winnings is what any list of 120 to 180 intraday trades
  looks like.
- Random lists that happened to end in profit die faster than the rules: their median is 1 to 2.5% of
  trades removed, against 1.7 to 8.3% for the rules. Every rule is at or above its control's median.
- So P-0421's reading was too harsh. "Dies with its best ten gone" is not evidence that an admission
  was a fluke; it is true of nearly everything this size. P-0410's line about E-017 ("ten trades are
  the whole profit") needs the same footnote: E-017 is the sturdiest of the nine.
- What P-0421 did get right still stands: the measure does not pick forward passers.

**Caveats.** The control keeps each trade's day, symbol and hold, so it shares the rule's exposure to
big-move days; it is a null for entry timing only. E-015's control has just 7 profitable lists of 500.
In sample on the admission windows. No rule, register row or kill line was touched.

**Next.** Close. A note for the scanner in a daytime slot: if a concentration figure is ever printed on
the ladder, print the control's beside it.
