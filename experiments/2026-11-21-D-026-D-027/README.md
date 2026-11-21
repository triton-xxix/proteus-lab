# D-026 and D-027 read: three edge rules, forward weeks of 11 to 17 Nov and 12 to 18 Nov (21 Nov 2026)

Smith, 20:10 on 21 Nov 2026. D-026 is a day past its backstop (20 Nov), D-027 lands on its backstop.
Both were flagged DUE by every slot since 19 Nov and none closed them: the nightly would not read W1 on an
unchecked span, and the repeat guard stopped duecheck queueing them (F-0105, F-0108).

## The span check, and why it looked unconfirmed

Each FORWARD.md says to read the scan tagged with the last session's date and to read W1 only if
`span.stock_w1_sessions` is exactly the registered sessions. In the tagged file it never is: a scan's W1
ends the session before its tag, because the tag's own session has not closed when the nightly runs.

| row | registered sessions | registered tag, its W1 | next tag, its W1 |
|---|---|---|---|
| D-026 | 11, 12, 13, 16, 17 Nov | 2026-11-17: 10, 11, 12, 13, 16 Nov | 2026-11-18: 11, 12, 13, 16, 17 Nov (exact) |
| D-027 | 12, 13, 16, 17, 18 Nov | 2026-11-18: 11, 12, 13, 16, 17 Nov | 2026-11-19: 12, 13, 16, 17, 18 Nov (exact) |

D-025 was read the same way on 17 Nov (registered tag 2026-11-16, read from 2026-11-17's exact W1). So I
read each rule from the next tag's results.json, where the registered check passes word for word. No
`rescore.py` was needed. I give the registered tag's figure beside it; it does not change a verdict.

## Measured

Verbatim W1 rows, after 0.03% costs:

| id | rule | file | n | W1 total | mean a trade | control mean | win |
|---|---|---|---|---|---|---|---|
| E-017 | Gap and go 0.5% (scored) | 2026-11-18 | 36 | -7.395% | -0.2054% | -0.0232% | 50.0% |
| (beside) | Gap and go 1% | 2026-11-18 | 18 | -6.496% | -0.3609% | -0.0506% | 50.0% |
| (beside) | Gap and go 2% | 2026-11-18 | 7 | +2.239% | +0.3198% | -0.0633% | 71.4% |
| E-018 | Opening reversal: fade first 30m to 13:00 | 2026-11-18 | 60 | -6.736% | -0.1123% | -0.0240% | 43.3% |
| E-019 | ORB 30m fade (failed break) | 2026-11-19 | 53 | -7.715% | -0.1456% | -0.0336% | 18.9% |

On the registered tags (W1 a day early): E-017 -10.36%, E-018 -1.20% (2026-11-17, from the 19 Nov run log),
E-019 -7.737%, n 51 (2026-11-18). All below zero.

## Lines

From `edges/scan/2026-11-10/FORWARD.md` (10 Nov) and `edges/scan/2026-11-11/FORWARD.md` (11 Nov), as
written: "week total after 0.03% costs above zero AND above its random-entry control mean". Only Gap and go
0.5% is scored for E-017; 1% and 2% are read beside it.

## Verdict

**E-017 FAIL, E-018 FAIL, E-019 FAIL.** All three week totals are below zero on the registered sessions, and
on the registered tags too, so no reading moves a word.

## Said plainly

- Three for three down, each by about 7%. The ladder put them forward because they climbed three rungs out of
  61 rules, against about 7.6 climbers by luck alone; this week is what that warning looks like.
- E-017 and E-018 trade the same mornings in opposite spirits, and FORWARD.md said both passing would be odd.
  Both failing is not odd: it was a week where neither following nor fading the open paid.
- Gap and go 2% was up +2.24% on 7 trades. It is not scored and seven trades is nothing; it is not a reason to
  re-register the family.
- E-019 won 18.9% of its trades, as its FORWARD.md warned (about one in five): a week rests on a handful.
- The process fault is the tag. Every FORWARD.md since 28 Oct names a tag whose W1 is a day early, and the
  nightly then stops on a span it cannot confirm. That is fixed separately (F-0105 note).

## Next

None registered. None of the three gets a second forward week.
