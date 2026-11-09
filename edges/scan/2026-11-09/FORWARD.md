# Second forward paper week from the D-019 and D-021 reads

Written 9 Nov 2026 about 20:25 UK time by the Smith, before the first of these sessions opens on
10 Nov. The commit timestamp is the proof.

E-013, E-014 and E-016 passed their forward week of 2 to 6 Nov
(`experiments/2026-11-09-D-019-D-021/README.md`). FORWARD.md for each said a pass earns a second forward
week, not money. E-015 failed and goes no further.

| id | rule | forward week | pass line |
|---|---|---|---|
| E-013 | VWAP cross after 11:00, hold to close (stocks, 12 names; the code starts at bar 12, 10:30, and that is the rule) | 10, 11, 12, 13 and 16 Nov 2026 (5 sessions) | week total after 0.03% costs above zero AND above its random-entry control mean |
| E-014 | ORB 15m fade (failed break) (stocks, 12 names) | the same | the same line |
| E-016 | Opening drive: first bar direction to 11:00 (stocks, 12 names) | the same | the same line |

Scoring: run `scan.py --tag 2026-11-16` after the 16 Nov close (the nightly does this anyway) and read
the three rules' W1 rows. No parameter changes before then.

**Check the sessions first.** The first forward week's W1 was silently not the registered week: a
broken day dropped out and the block reached back a session (`sessions.py` in the read's folder). So
read W1 only if `span.stock_w1_sessions` in that night's `results.json` is exactly 2026-11-10, 11, 12, 13
and 16. If it is not, score the registered sessions that exist with `rescore.py`'s method and say so in
the row. Fewer than four registered sessions kept: INCONCLUSIVE, no re-run on a later week.

A pass earns a third forward week and still not money. DUE D-025, backstop 2026-11-19.
