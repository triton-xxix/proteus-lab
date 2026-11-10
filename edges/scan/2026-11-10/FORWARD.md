# Forward paper week from the 10 Nov 2026 ladder

Written 10 Nov 2026 about 23:35 UK time by the nightly, before the first of these sessions opens on
11 Nov (14:30 UK). The commit timestamp is the proof.

Tonight's ladder (`LADDER.md` beside this file) had 6 of 61 rules climb all three rungs. Luck alone
gives about 7.6, so this is not a discovery: six climbers is what noise looks like, and the forward
week is the only test that counts. Two of the six are already registered and in their second forward
week (E-013, E-014, D-025). The other four are new to the register. Three of them are one family
(Gap and go at 0.5%, 1% and 2%; the higher thresholds are subsets of the 0.5% trades), so one row
carries the family, as E-012 did on 23 Oct.

| id | rule | ladder W1, W2, W3 | forward week | pass line |
|---|---|---|---|---|
| E-017 | Gap and go 0.5% (stocks, 12 names, 5m bars); the 1% and 2% thresholds are read beside it but only 0.5% is scored | +9.32%, +16.36%, +11.21%, 121 trades, pooled p 0.03, 6 of 11 blocks | 11, 12, 13, 16 and 17 Nov 2026 (5 sessions) | week total after 0.03% costs above zero AND above its random-entry control mean |
| E-018 | Opening reversal: fade first 30m to 13:00 (stocks, 12 names, 5m bars) | +6.17%, +5.05%, +5.89%, 180 trades, pooled p 0.02, 3 of 11 blocks | the same | the same line |

Ladder weeks: W1 sessions 2, 3, 4, 6 and 9 Nov (5 Nov dropped, as on the last read), W2 26 to 30 Oct,
W3 19 to 23 Oct. The 10 Nov session sits in neither the ladder nor the forward week.

Scoring: run `scan.py --tag 2026-11-17` after the 17 Nov close (the nightly does this anyway) and read
the two rules' W1 rows. No parameter changes before then.

**Check the sessions first**, as `edges/scan/2026-11-09/FORWARD.md` says: read W1 only if
`span.stock_w1_sessions` in that night's `results.json` is exactly 2026-11-11, 12, 13, 16 and 17. If it
is not, score the registered sessions that exist with the `rescore.py` method from
`experiments/2026-11-09-D-019-D-021/` and say so in the row. Fewer than four registered sessions kept:
INCONCLUSIVE, no re-run on a later week.

Things that weaken this before it starts, said now: Gap and go and the Opening reversal partly trade
the same mornings in opposite spirits (one follows the open, one fades the first half hour), so both
passing in one week would be odd; Opening reversal is positive in only 3 of 11 earlier blocks; and a
pass earns a second forward week, never money. DUE D-026, backstop 2026-11-20.
