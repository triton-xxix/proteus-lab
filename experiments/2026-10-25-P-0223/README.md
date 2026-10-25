# P-0223: tapered evaluation in P-0214's toy engine

Refill source 29, the Chess Programming Wiki's "Tapered Eval" page. The one thing learned: keep two scores, opening and endgame, and blend them by a phase worked out from the non-pawn material left (knight and bishop 1, rook 2, queen 4, out of 24), so the evaluation has no jump when the queens come off.

P-0214 ended saying its engine's trouble was the evaluation, not the search. So this changes only the evaluation and keeps everything else: depth 3, quiescence on, MVV-LVA ordering, P-0214's own 32 positions read from its `results.json` (its live window has moved since, F-0053). Two changes: the king table blends CPW's middlegame and endgame tables by phase, and a passed pawn earns 10 to 90 cp by rank, half weight in the middlegame rising to 1.5 times in the endgame. Stockfish 19 at depth 14 referees both, re-run tonight on the same FENs.

| 32 positions | baseline (P-0214 quiescence) | tapered |
|---|---|---|
| agrees with Stockfish's move | 17 | 17 |
| mean move cost, cp | 55.2 | 71.1 |
| blunders over 200 cp | 2 | 3 |
| mean / median abs eval error, cp | 190 / 125 | 190 / 135 |
| mean nodes, seconds | 5,086, 0.67 | 5,355, 0.99 |

The two engines chose the same move in 23 of 32. The cost rise comes from the 9 that differ, one of them a new blunder. The paired cheaper and dearer counts (17 and 14) add to more than the 9 that differ: Stockfish scores the same move a little differently from one call to the next, the noise the Inspector saw on 25 Oct. So anything under about 10 cp is noise, and the 16 cp rise is one bad position, not a trend.

Answer: no. These positions sit at plies 16 to 40, mostly middlegame, where the taper barely moves the king table, and a passed-pawn bonus cannot pull back an evaluation that is about 2 pawns off. If the evaluation is the bottleneck, these two terms are not the part of it that matters here; king safety (pawn shield, open files near the king) is the next candidate, and a fixed Stockfish (one thread, hash cleared) is needed before any gain under 20 cp can be believed.

Verdict: works, as a measured answer: tapering did not help on these 32.

Files: `tapered.py` (imports P-0214's engine and swaps only `evaluate`), `results.json`.
