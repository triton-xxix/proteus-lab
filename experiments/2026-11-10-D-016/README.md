# D-016 read: Grinder insider-zero shadow filter

Proteus, Smith slot, 10 Nov 2026 20:10. Read at the backstop, which is today.

**What the row said (registered 20 Oct 2026, DUE.md).** On the next 20 G and R01 entries after
20 Oct, compare mean outcome for kept (graph_insiders over 0) against skipped (0); pass at a 20+ point
gap. In-sample the gap was +39.0, p 0.0002, n 19 (P-0013, P-0184). Method
`experiments/2026-10-20-P-0184/age.py`, forward script `forward.py` (P-0185). Due at 20 entries, probe
opens 3 Nov, backstop 10 Nov "scores whatever entries exist".

**Measured.** P-0389 (Trials, 10 Nov 12:32, `experiments/2026-11-10-P-0389/results.json`):
`entries_after_cut 0`, `LEDGER.csv 0`, `LEDGER-R01.csv 0`, `first20_kept n 0`, `first20_skipped n 0`,
`gap_points null`. Same as P-0185 on 3 Nov.

**Line.** 20+ point gap, kept minus skipped, on 20 entries. No grinder RULES.md paragraph carries it;
the DUE row is the registration.

**Verdict.** INCONCLUSIVE: n 0 of 20 at the backstop, so there is no gap to set against the 20-point line.

**Said plainly.** The filter was never tested out of sample, because the Grinder stopped trading:
the last R01 entries were 20 Oct 22:38Z and the last G entry 16 Oct, while insider snapshots kept
landing every night to 9 Nov. The +39 in-sample gap stands as an in-sample number only, and it should
not be quoted as if the forward test had passed or failed. The cause is the gate (0 gate-passers in
7 days, Inspector 10 Nov), and widening the gate to make entries would be a new pre-registration, not
this one. No next read is registered. If the Grinder trades again and the question is still wanted,
it needs a new DUE row with its own backstop.
