# Forward paper week from the 23 Oct 2026 ladder

Written 23 Oct 2026 about 18:30 UTC, before the week of 26 to 30 Oct exists. The commit timestamp
is the proof.

The ladder (LADDER.md here) climbed one rule of 61 through all three weeks, against about 7.6 by
luck and 5 on the pure-noise benchmark. That is fewer than noise, which says the last three weeks
did not hand anything out. Two rules go forward anyway, on paper, because forward is the only test
that counts:

| id | rule | why | forward week | pass line |
|---|---|---|---|---|
| E-011 | Morning direction into the afternoon (stocks, 12 names): at the middle bar of the session, go the way the day has moved from the open, hold to the close | the only rule up three weeks running (+0.54%, +5.33%, +4.15%), pooled p 0.10 over 179 trades; but only 5 of 11 earlier blocks positive | 26 to 30 Oct 2026 (5 sessions) | week total after 0.03% costs above zero AND above its random-entry control mean |
| E-012 | ORB 30m, target 1R (stocks, 12 names): break of the first 30 minutes' range, stop at the other side, target one range width, flat at the close | up two weeks of three with the lowest pooled p of the family (0.03), +11.0% and +14.3% then -8.4% in W3; 5 of 11 blocks | 26 to 30 Oct 2026 | the same line |

Scoring: run `scan.py --tag 2026-10-31` on Saturday 31 Oct. Its W1 is exactly 26 to 30 Oct; read the
two rules' W1 rows. No parameter changes before then. A pass earns a second forward week, not money.
DUE D-017, backstop 2 Nov 2026.

Rules not carried forward: every other rule failed W1, W2 or W3. They stay in the scanner and get
a fresh ladder every night, as Luke asked; a rule that climbs on a later night gets its own forward
week registered the same way.
