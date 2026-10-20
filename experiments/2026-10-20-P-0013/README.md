# P-0013: Grinder positions split by graphInsidersDetected

**Question.** Do Grinder positions whose token showed more RugCheck graph insiders at entry do worse over 24h?

**Called shot (before looking).** works at 0.60: the over-5 group's mean 24h outcome at least 10 points worse than the 0 group.

**Method.** `split.py` joins each position in `grinder/LEDGER.csv` and `LEDGER-R01.csv` to the latest
`grinder/insiders/*.jsonl` snapshot of its mint taken at or before entry (insider capture began 11 Oct,
P-0105). Outcome is `score_24h` from the ledger, or `path_move_pct` from `PATHS.csv` when that is blank
(2 of 19). One row per token. Buckets: 0, 1 to 5, over 5.

**Numbers (19 positions, G-0071 to G-0092, 11 to 16 Oct; all v0.2 book).**

| graph insiders | n | mean 24h | median | at or below -50% | rugged |
|---|---|---|---|---|---|
| 0 | 10 | -99.3% | -99.3% | 10 of 10 | 5 |
| 1 to 5 | 0 | | | | |
| over 5 | 9 | -60.3% | -74.8% | 6 of 9 | 0 |

The shot missed: the over-5 group did 39 points *better*, not 10 worse. Every rug in the sample has 0 insiders recorded.

**Reading.** Most likely `graphInsidersDetected: 0` is not "clean": on a fresh token RugCheck's graph
may simply not have run or found nothing yet, and fresh tokens are the ones that rug. Tokens with a
populated insider graph are older or busier. That is a guess, not measured; the next probe checks it
against token age at entry.

**What I did not do.** No R01 rows joined (none have an insider snapshot before entry with an outcome yet).
19 rows, not 20: that was all there was. No significance test; at n=19 with this split, a permutation
test is the next step, not a verdict. No change to any rule.
