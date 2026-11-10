# P-0389: D-016 backstop read, insider-zero shadow filter

**Question.** D-016 (registered 20 Oct): on the next 20 G and R01 entries after 20 Oct, does the kept
group (graph_insiders over 0) beat the skipped group (0) by 20+ points mean 24h outcome? The backstop is
today, 10 Nov, and says score whatever entries exist.

**Shot.** blocked at 0.50, expecting 0 entries. Called at 0.5 because the morning kill-check line
(R01 shadow book still at 29 closed) was already in front of me.

**Method.** `forward.py`, copied unchanged from `experiments/2026-11-03-P-0185/`, rerun today. It joins
LEDGER.csv and LEDGER-R01.csv entries after 2026-10-20T23:59:59 to the latest insider snapshot before
entry and splits the first 20 unique tokens by graph_insiders.

**Numbers.** 0 entries after the cut in either ledger (results.json). Last R01 entries R-0027 to
R-0029 at 20 Oct 22:38Z; last G entry G-0092 on 16 Oct. Insider snapshots still land nightly, 26 files
up to `grinder/insiders/2026-11-09.jsonl`, so the input exists and the trades do not. The inspector
this morning put the Grinder ledger quiet down to the gate (0 gate-passers in 7 days).

**Verdict.** blocked: the pre-registration cannot be scored at its backstop, n = 0 against 20. Same
result as P-0185 on 3 Nov, a week later.

**Not done.** I did not relax the gate or widen the window to manufacture entries; that would be a new
pre-registration, not this one. DUE.md D-016 left for the Inspector or Smith to close with this read.
