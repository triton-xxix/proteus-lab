# Forward paper week from the 11 Nov 2026 ladder

Written 11 Nov 2026 about 23:40 UK time by the nightly, before the first of these sessions opens on
12 Nov (14:30 UK). The commit timestamp is the proof.

Tonight's ladder (`LADDER.md` beside this file) had 4 of 61 rules climb all three rungs. Luck alone
gives about 7.6, so this is not a discovery: four climbers is fewer than noise would give, and the
forward week is the only test that counts. Three of the four are already on the register: E-013
(VWAP cross after 11:00) and E-014 (ORB 15m fade) are in their second forward week (D-025), and
Gap and go 2% is read beside E-017, whose family row carries it (D-026). One is new.

| id | rule | ladder W1, W2, W3 | forward week | pass line |
|---|---|---|---|---|
| E-019 | ORB 30m fade (failed break) (stocks, 12 names, 5m bars, flat at close) | +2.68%, +2.37%, +3.67%, 145 trades, pooled p 0.01, 3 of 11 blocks | 12, 13, 16, 17 and 18 Nov 2026 (5 sessions) | week total after 0.03% costs above zero AND above its random-entry control mean |

Ladder weeks: W1 sessions 3, 4, 6, 9 and 10 Nov (5 Nov dropped, as on earlier reads), W2 27 Oct to
2 Nov, W3 20 to 26 Oct. The 11 Nov session sits in neither the ladder nor the forward week.

Scoring: run `scan.py --tag 2026-11-18` after the 18 Nov close (the nightly does this anyway) and read
the rule's W1 row. No parameter changes before then.

**Check the sessions first**, as `edges/scan/2026-11-09/FORWARD.md` says: read W1 only if
`span.stock_w1_sessions` in that night's `results.json` is exactly 2026-11-12, 13, 16, 17 and 18. If it
is not, score the registered sessions that exist with the `rescore.py` method from
`experiments/2026-11-09-D-019-D-021/` and say so in the row. Fewer than four registered sessions kept:
INCONCLUSIVE, no re-run on a later week.

Things that weaken this before it starts, said now: this is the 30-minute sibling of E-014, which is
already in a second forward week, so the two will mostly win and lose on the same mornings and a pass
here is not independent evidence; its mean is 0.06% a trade, twice the cost and no more; it wins on
about one trade in five, so a week rests on a handful of trades; it is positive in only 3 of 11 earlier
blocks; and a pass earns a second forward week, never money. DUE D-027, backstop 2026-11-21.
