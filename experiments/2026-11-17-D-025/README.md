# D-025: the scanner's second forward week, E-013, E-014 and E-016

Registered 9 Nov 2026 in `edges/scan/2026-11-09/FORWARD.md`: sessions 10, 11, 12, 13 and 16 Nov, pass
line "week total after 0.03% costs above zero AND above its random-entry control mean". Due the
night of 16 Nov; nothing ran that night (F-0098), so it is read on 17 Nov, inside the 19 Nov backstop.

## Sessions checked first

`span.stock_w1_sessions` in `edges/scan/2026-11-17/results.json` is exactly 2026-11-10, 11, 12, 13 and
16. That is the registered week, so W1 is read as it stands and `rescore.py` is not needed. The
17 Nov session is not in the data the scanner pulled at 23:26 UK, which is why W1 ends on the 16th.

## The read (W1 rows of tonight's scan, no parameter changed)

| id | rule | trades | week total | mean a trade | control mean | p | verdict |
|---|---|---|---|---|---|---|---|
| E-013 | VWAP cross after 11:00, hold to close | 46 | -7.88% | -0.171% | -0.017% | 0.82 | **FAIL** (below zero, below control) |
| E-014 | ORB 15m fade (failed break) | 53 | -1.40% | -0.027% | -0.034% | 0.43 | **FAIL** (below zero; a hair above control, 25% winners) |
| E-016 | Opening drive: first bar direction to 11:00 | 60 | +14.84% | +0.247% | -0.035% | 0.007 | **PASS** |

E-013 and E-014 each passed one forward week (2 to 6 Nov: +19.88% and +7.50%) and failed the next.
They go no further. One good week then one bad week is what a rule with no edge looks like.

E-016 has now passed two forward weeks (+0.87% as read, +6.71% on the registered sessions, then
+14.84%). A pass earns a third forward week and still not money:
`edges/scan/2026-11-17/FORWARD.md`, DUE D-029.

Caveat: tonight's ladder has E-016 at two rungs of three, because its W3 (26 to 30 Oct) was -3.59%.
The forward weeks are the test that counts, and the ladder week it lost is not one of them, but it
is the same rule losing a week three weeks ago.
