# P-0403: the Grinder's bankrolls, from the ledgers

Follow-up to P-0402, and a correction of it: P-0318 found the cause on 3 Nov. This probe recomputes
the numbers instead of quoting them, reads the R01 path, and fixes the line that kept hiding it.

`bankroll.py`, read-only, the desk's own RULES and gate (`results.json`):

| book | closed | realised | bankroll now | first below one £100 stake | last entry |
|---|---|---|---|---|---|
| v0.2 | 83 | -£988.67 | £11.33 | 17 Oct 00:18Z | 16 Oct 22:28Z |
| R01 shadow | 29 | -£1,093.83 | -£93.83 | 20 Oct 23:10Z | 20 Oct 22:38Z |

Neither book has entered since the exit that took it below a stake. R01 uses the same test
(`bankroll >= size_gbp` in `apply_r01`), so it stopped for the same reason four days later, and it is
below zero. Tonight 4 of 152 snapshot rows pass every gate and all 4 are mints never held, so held-mint
skipping is not the block.

What follows from that, and is not mine to settle in a scheduled run:

- D-016 was closed INCONCLUSIVE today at n 0 because "no G or R01 entry after 20 Oct". True, and the
  reason is that both books were bust, so no number of further nights would have produced one.
- The kill check reads R01 as RUNNING, 11 to the 40 mark. It cannot reach 40. v0.2's same-nights line
  is in the same position.
- Whether a bust paper book is closed, restaked or restarted is a rules decision.

Changed tonight, one commit: `grinder/paper.py` now prints "binding constraint: bankroll GBP 11.33 is
below the GBP 100 stake, so v0.2 cannot enter; 4 of 152 rows passed every gate" ahead of the gate
counts when money is what binds. A printed line only: no rule, ledger, stake or gate touched. Checked
by running `--apply-rules` again (0 exits, 0 entries, both lines printed). `--apply-r01` still prints
nothing about its bankroll; left for the Smith.
