# Due: pre-registered tests that still owe a result

Written 8 Oct 2026 after Luke asked why the round-2 Grinder replay, pre-registered on 30 Sep,
had never been run. A pre-registration without a scoring date is a wish. Every row here is a
test that was written down before its data existed; `bin/duecheck.py` reads this file every
night in step 7, says which rows are due, and queues each overdue one as a desk probe at the
front of the loop. A row closes when the `scored` column carries the date and the artefact.

Rules: one row per pre-registration, added the night it is written. `due` is a date (the night
it should run) or a data condition in plain words plus a backstop date. `scored` is blank until
the run exists. Nothing here is a result; results live where the row points.

| id | registered | what | where the rule is | due | scored | probe |
|---|---|---|---|---|---|---|
| D-001 | 2026-09-30 | Grinder round 2: entry-rule variants E01-E06 and M01-M09 at exits V01 and V17, mentions joined | grinder/harness/VARIANTS-2.md | 40 post-30-Sep passers, backstop 2026-10-07 | 2026-10-08, grinder/harness/REPLAY-2.md and REPLAY-2-NOTES.md, P-0096 | P-0096 |
| D-002 | 2026-10-06 | Grinder fill check re-run (touch, close, late, depth fills on every closed v0.2 position) | experiments/2026-10-06-grinder-fill-check/REPORT.md | every Sunday, next 2026-10-11 | | |
| D-003 | 2026-10-06 | Grinder harness: an entry-delay variant (buy one minute after the snapshot) | experiments/2026-10-06-grinder-fill-check/REPORT.md "Next" | 2026-10-09 | | |
| D-004 | 2026-10-07 | P-0084 trend portfolio: its recorded Sharpe 0.28 against 0.35 on a re-run of the same script and data; re-read before it is quoted again | experiments/2026-10-07-P-0088/README.md | 2026-10-09 | | |
| D-005 | 2026-10-07 | Systems book 1: first KILL or KEEP reading at 30 closed trades | systems/RULES.md | 30 closed trades, backstop 2027-01-31 | | |
| D-006 | 2026-10-07 | Systems book 2 (IBS): KILL at 200 if negative after costs, verdict at 500 | systems/RULES.md | 200 closed trades, backstop 2027-12-31 | | |
| D-007 | 2026-10-08 | Grinder R01 shadow book wired into paper.py (BOOKS.json "second", LEDGER-R01.csv, Telegram look-up), forward from the 8 Oct 12:00Z snapshot | grinder/harness/VARIANTS-3.md | 2026-10-09 | | |
| D-008 | 2026-10-08 | Grinder R01 verdict at 40 closed against v0.2 on the same nights (KEEP, KILL lines in the file; KILL check at 20) | grinder/harness/VARIANTS-3.md | 40 closed R01 positions, backstop 2026-11-30 | | |
