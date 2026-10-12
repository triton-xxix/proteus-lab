# P-0121, attempt 1, 13 Oct 2026: R01 wiring, groundwork only

No verdict tonight. The wiring was not built, and I stopped the loop because tonight's snapshot data
is not there (below).

Measured with `replay.py`, read-only, R01's selection over the four snapshots since 2026-10-08T12:00Z:

- The Telegram look-up R01 needs is there for every gate-passer, not only the picks: 41 of 41 passers
  had a telegram row in `grinder/research/MENTIONS.csv` on their night.
- R01 and v0.2 share 2 of 4 picks on every one of the four nights. On 11 Oct R01 found only 3.
- One ordering problem for the wiring: the nightly runs `mentions.py` after `paper.py --apply-rules`,
  so R01's entries need their own step after mentions and before the commit (`paper.py --apply-r01`,
  or move mentions ahead of apply-rules).

Why the loop stopped: the 12 Oct scan was killed by a 10-minute tool timeout before it wrote
SNAPSHOTS.csv, so there is no 12 Oct snapshot, and paper.py opened G-0075 to G-0077 from the 11 Oct
snapshot. Fixed going forward in 9825d44 (scan writes row by row) and edcd270 (paper.py refuses a
snapshot more than 3 h old). The three rows are still in the ledger.
