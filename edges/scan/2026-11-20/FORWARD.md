# Forward paper week from the 20 Nov 2026 ladder

Written 20 Nov 2026 about 23:35 UK time by the nightly, before the first of these sessions opens on
23 Nov (14:30 UK). The commit timestamp is the proof.

Tonight's ladder (`LADDER.md` beside this file) had 3 of 61 rules climb all three rungs. Luck alone
gives about 7.6, so this is not a discovery: three climbers is fewer than noise would give, and the
forward week is the only test that counts. One of the three is already on the register: ORB 15m fade
(E-014) failed its second forward week on 17 Nov (D-025) and goes no further, so it is not re-entered.
Two are new and are one family, so they get one row.

| id | rule | ladder W1, W2, W3 | forward week | pass line |
|---|---|---|---|---|
| E-020 | Gap fade 0.5% (stocks, 12 names, 5m bars); the row carries Gap fade 2%, a subset of its trades, read beside it | 0.5%: +11.18%, +0.85%, +0.15%, 123 trades, pooled p 0.24, 7 of 11 blocks. 2%: +7.74%, +3.60%, +0.39%, 37 trades, pooled p 0.23, 8 of 11 blocks | 23, 24, 25, 27 and 30 Nov 2026 (5 sessions; 26 Nov is Thanksgiving, closed; 27 Nov closes early at 13:00 ET) | 0.5%: week total after 0.03% costs above zero AND above its random-entry control mean. 2% is reported, not passed or failed: it may have no trade in the week |

Ladder weeks as the scanner read them tonight: W1 13 to 19 Nov, W2 6 to 12 Nov, W3 29 Oct to 4 Nov.
The 20 Nov session sits in neither the ladder nor the forward week.

Scoring: run `scan.py --tag 2026-11-30` after the 30 Nov close (the nightly does this anyway) and read
the rule's W1 row. No parameter changes before then.

**Check the sessions first**, as `edges/scan/2026-11-09/FORWARD.md` says: read W1 only if
`span.stock_w1_sessions` in that night's `results.json` is exactly 2026-11-23, 24, 25, 27 and 30. If
it is not, score the registered sessions that exist with the `rescore.py` method from
`experiments/2026-11-09-D-019-D-021/` and say so in the row. Fewer than four registered sessions kept:
INCONCLUSIVE, no re-run on a later week.

Things that weaken this before it starts, said now: this is the mirror of E-017 (Gap and go, which
climbed on 10 Nov and is still owed its D-026 read), so the two rules cannot both be right on the same
gaps and the ladder is flipping between them; W2 and W3 are +0.85% and +0.15%, so the climb rests on one
good week; pooled p is 0.24; three climbers against a luck figure of 7.6; a half-day session sits in
the week; and a pass earns a second forward week, never money. DUE D-031, backstop 2026-12-03.
