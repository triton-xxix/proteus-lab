# P-0234: late move reductions in P-0214's toy engine

**Question.** The Chess Programming Wiki says LMR "can often reduce the effective branching factor to
less than 2". What does the textbook version do to P-0214's engine at depth 4?

**Method.** `lmr.py` imports P-0214's `quiescence.py` unchanged and subclasses its engine: first two
moves at full depth, then quiet moves (no capture, promotion or check, not in check) at remaining depth
3 or more searched one ply shallower on a null window, re-searched at full depth if they beat alpha.
P-0214's 32 frozen positions, depth 3 and 4 for both engines, Stockfish 19 depth 14 as referee on the
depth-4 move. Branching factor = nodes at depth 4 / nodes at depth 3, quiescence nodes included.

**Numbers (32 positions, depth 4).**

| | Base (quiescence) | With LMR |
|---|---|---|
| Mean nodes | 38,362 | 29,749 (**22.5% fewer**) |
| Mean seconds | 4.86 | 3.91 |
| Branching factor, pooled | 7.54 | 5.85 |
| Branching factor, median | 6.73 | 5.08 |
| Agrees with Stockfish | 15 | 16 |
| Mean move cost | 61.7 cp | 56.5 cp |
| Blunders over 200 cp | 3 | 3 |

Same move in 30 of 32. 3,138 reductions, 291 re-searches (9%). Most of the 5.2 cp cost drop is one
position (L5vicmQL ply 40: 165 cp to 35 cp); Stockfish re-scoring noise is about 10 cp (P-0223), so the
cost change is noise.

**Why nowhere near "under 2".** At depth 4 the rule only fires where 3 plies remain, i.e. one level of
the tree, and quiescence nodes (captures, never reduced) are most of the count. The wiki's figure is for
deep searches with good ordering (history, killers), which this engine has none of.

**What I did not do.** No depth 5 or 6, no log-based reduction formula, no killer or history ordering,
no PVS. Depth 4 base was already 5 s a position in pure Python.

**Shot.** works at 0.65: about 40% fewer nodes, branching factor above 2, cost within 10 cp. Nodes
22.5% (missed by half), branching factor 5.85 (hit), cost within 5.2 cp (hit).
