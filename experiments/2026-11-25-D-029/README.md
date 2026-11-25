# D-029: E-016's third forward week, read 25 Nov 2026

Registered in `edges/scan/2026-11-17/FORWARD.md` (17 Nov, before the 18 Nov open). Rule: Opening drive,
first bar direction to 11:00, 12 US stocks and ETFs on 5m bars. Pass line: week total after 0.03% costs
above zero AND above its random-entry control mean.

Sessions check: `edges/scan/2026-11-25/results.json` has `span.stock_w1_sessions` =
2026-11-18, 19, 20, 23, 24, exactly the registered sessions. The 24 Nov nightly did not run, so the
tag is 25 Nov, not the 24 Nov the FORWARD.md named; the W1 window is the same five sessions.

| rule | n | week total | mean a trade | win % | control mean a trade | p |
|---|---|---|---|---|---|---|
| Opening drive: first bar direction to 11:00 | 60 | -13.07% | -0.218% | 48.3 | -0.019% | 0.917 |

Verdict: **FAIL**. Below zero and below its control. E-016 passed two forward weeks (D-021, D-025
+14.84%) and lost the third; it goes no further, as the FORWARD.md said a third week decides.

Read beside the rest of the scanner's forward record: every rule carried forward since 23 Oct has now
failed a forward week (E-011, E-012, E-013, E-014, E-015, E-017, E-018, E-019, E-016). E-020 (D-031) is the
only one still running. The FORWARD.md's warning holds: two passes in a row come by luck about one time
in four for a rule with no edge, and twelve names at the same open are close to one bet a day.

Tonight's ladder (tag 2026-11-25): no rule climbed all three rungs, so no new forward week.
