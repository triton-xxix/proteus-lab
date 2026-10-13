# P-0121: R01 shadow book wired into paper.py

## Attempt 2, 13 Oct 2026 (Trials 12:31): wired

Question: can R01 (`grinder/harness/VARIANTS-3.md`) run as a forward shadow book beside v0.2, picking
what the read-only replay said it would pick?

Called shot: works at 0.55, "wired select_r01 reproduces replay.py picks on 4 of 4 nights".
Measured: 4 of 4 (`check.py`, `check.json`), same tokens in the same order every night.

What was built, in `grinder/paper.py`:
- `select_r01()`: v0.2's gate-passers by 1h volume, skipping held mints and any row with a rug marker
  (rugcheck risk, 1h change above 0, zero Telegram mentions that night). A token with no Telegram row
  is not skipped.
- `apply_r01()` behind `--apply-r01`: exits by `exit_v02` (rule_version "R01" has no paths levels
  entry, so v0.2's levels apply), entries at v0.2's stake, slots and bankroll check, ids `R-0001` up so
  candle caches never collide with G- rows, own ledger `grinder/LEDGER-R01.csv`. Refuses a snapshot
  older than 3 h and any snapshot before 2026-10-08T12:00Z.
- `tasks/nightly.md` step 2 runs it after `mentions.py`, which is what R01's third marker needs.

One live run at 12:3x: "no entries, latest snapshot 2026-10-11T22:23:37Z is more than 3 h old";
LEDGER-R01.csv written with its header only. First real entries: tonight's nightly.

Departures from the spec, said plainly:
- Not BOOKS.json "second": that book shares LEDGER.csv and its slot logic, and the spec also names
  its own ledger. A separate file keeps the v0.2 bankroll untouched.
- One small difference from replay.py: an empty Telegram `count` is read as unmeasured here, as 0
  (silent) there. It changed no pick on the four nights.
- PATHS.csv is not written for R- rows.

Not done: the four nights 8 to 11 Oct are not in the ledger. VARIANTS-3 says they can be scored after
the fact from candles; queued as a deepen.

## Attempt 1, 13 Oct 2026 (nightly): groundwork only

`replay.py` read R01's selection over the four snapshots since 2026-10-08T12:00Z: 41 of 41 passers had
a Telegram row, R01 and v0.2 share 2 of 4 picks each night, and on 11 Oct R01 found only 3. The nightly
ran mentions after apply-rules, hence the separate `--apply-r01` step. The loop stopped because the 12
Oct scan was killed before it wrote SNAPSHOTS.csv.
