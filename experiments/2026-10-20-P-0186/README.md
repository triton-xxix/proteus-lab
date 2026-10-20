# P-0186: is graph_insiders 0 a blank? (Kaggle Learn leakage check on P-0184)

**Source.** Kaggle Learn, Intermediate ML step 7, Data Leakage (Alexis Cook). The method I took from it:
when a feature is 0 for a whole outcome class (their credit-card case: everyone refused had zero
expenditure), check how the value was recorded before trusting it. P-0184 had all 7 rugs in the
graph_insiders = 0 bucket, so the same check applies.

**Called shot.** works at 0.50: blank-field share in 0-insider rows within 15 points of over-5 rows.

**Method.** `leak.py` profiles every row the scanner wrote to `grinder/insiders/` (1,076 rows) and the
19 G-book positions from P-0013, by bucket: share of blank holders, top10, creator, creator balance in
the same scan, median holders and RugCheck score. It then looks for a snapshot of each position's mint
taken 1h or more before entry.

**Numbers.**

| | n | any field blank | networks = 0 | median holders | median rug score |
|---|---|---|---|---|---|
| all scanned, 0 | 411 | 1% | 100% | 646 | 24 |
| all scanned, 1 to 5 | 108 | 1% | 0% | 886 | 1 |
| all scanned, over 5 | 557 | 1% | 0% | 18,304 | 1 |
| positions, 0 | 10 | 0% | 100% | 5,050 | 1 |
| positions, over 5 | 9 | 0% | 0% | 7,962 | 1 |

- Shot hit: 0 points apart (0% v 0% on positions). The 0 comes from complete reports; it is a reading,
  not a missing value. graphInsidersDetected 0 coincides exactly with an empty insiderNetworks list.
- Timing leak: none. Every snapshot used precedes entry (4 to 16 minutes), and RugCheck is not re-read later.
- 1h-before rerun: 0 of 19 positions have an earlier snapshot. The scanner sees a token once, at the
  nightly scan that enters it. That half could not be done.
- New and unasked: across all scanned tokens, 0-insider rows carry a median RugCheck score of 24
  against 1 for the others, but the gate-passers that became positions all sit at 1 either way. So the
  gate keeps 0-insider tokens RugCheck itself already rates as low risk.

**What I did not do.** No new rule. P-0185 (forward shadow filter, DUE D-016) is the test that counts.
