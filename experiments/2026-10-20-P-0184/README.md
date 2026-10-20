# P-0184: is graphInsidersDetected 0 just a fresh-token marker?

Follow-up to P-0013, which found Grinder positions with 0 graph insiders at entry did far worse over
24h (-99.3% mean, n=10) than those with over 5 (-60.3%, n=9).

**Called shot.** works at 0.55: the 0-insider median age at entry under half the over-5 median.

**Method.** `age.py` repeats P-0013's join, takes `age_h` from the same scan row in `grinder/SNAPSHOTS.csv`,
adds R01 rows (no 24h score there, so their own entry-to-exit move is used, flagged and kept out of the
test), and runs a one-sided permutation test (20,000 shuffles, seed 20261020) on the G-book gap.

**Numbers.**

- Median age at entry: 0 insiders 5.4h (n=13), over 5 insiders 5.8h (n=16). Not half; the shot missed.
  Age does not explain the split. My P-0013 guess was wrong.
- G book gap (over 5 minus 0): +39.0 points, permutation p = 0.0002 one-sided.
- R01 rows (10 of 13 seen had an outcome): over 5 hit take-profit 3 of 7; 0 insiders hit it 0 of 3, and 2 of 3 rugged.
- Rugs across both books: 7 of 7 in the 0 bucket.
- The 1 to 5 bucket is empty in both books: RugCheck seems to report 0 or a network.

**Reading.** On 29 positions, every rug and every near-total loss in the 0 group came from tokens the
graph found no insider network on, and that is not because they were younger. A guess I have not tested: a
token with no transfer network at all may be one wallet cluster the graph cannot see, which is what a
drain looks like. The split was named in P-0013's title before any data was looked at, so the test
is not fully post hoc; but n is small, two books overlap tokens, and nothing is out of sample.

**What I did not do.** Change any rule. A filter only counts once it is run forward: queued as a
shadow filter with a due date.
