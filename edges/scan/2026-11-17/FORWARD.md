# Third forward paper week for E-016, from the D-025 read

Written 17 Nov 2026 about 23:59 UK time by the nightly, before the first of these sessions opens on
18 Nov (14:30 UK). The commit timestamp is the proof.

D-025 was read tonight (`experiments/2026-11-17-D-025/README.md`): E-013 and E-014 failed their second
forward week and go no further; E-016 passed its second (+14.84% on 60 trades, control mean -0.035%
a trade, sessions 10, 11, 12, 13 and 16 Nov as registered). The 9 Nov FORWARD.md said a pass earns a
third forward week and still not money. This is that week.

| id | rule | forward week | pass line |
|---|---|---|---|
| E-016 | Opening drive: first bar direction to 11:00 (stocks, 12 names, 5m bars) | 18, 19, 20, 23 and 24 Nov 2026 (5 sessions) | week total after 0.03% costs above zero AND above its random-entry control mean |

The 17 Nov session sits in neither the second week nor this one: it had closed before this was
written, though the scanner had not pulled it.

Scoring: run `scan.py --tag 2026-11-24` after the 24 Nov close (the nightly does this anyway) and
read the rule's W1 row. No parameter changes before then.

**Check the sessions first**, as before: read W1 only if `span.stock_w1_sessions` in that night's
`results.json` is exactly 2026-11-18, 19, 20, 23 and 24. If it is not, score the registered sessions
that exist with the `rescore.py` method from `experiments/2026-11-09-D-019-D-021/` and say so in the
row. Fewer than four registered sessions kept: INCONCLUSIVE, no re-run on a later week.

Things that weaken this before it starts, said now: tonight's ladder has the rule at two rungs of
three (its 26 to 30 Oct week lost 3.59%); two passes in a row happen by luck about one time in four
for a rule with no edge; and 12 names trading the same open are closer to one bet a day than twelve.
A third pass earns a write-up on what an executor would need, not an executor and not money.
DUE D-029, backstop 2026-11-27.
