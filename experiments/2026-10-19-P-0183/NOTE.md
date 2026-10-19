# P-0183: John Levine's MCTS lecture, rebuilt

Refill source #11. YouTube captions were IpBlocked tonight, so the 15:50 lecture (UXW2yZndl7U) came
through `sandbox/skool_transcript.py --force-whisper`: base.en, the full talk to 15:32, numbers legible.
What it teaches: MCTS in four phases (UCB1 traversal, expand a leaf only once it has been visited,
random rollout, back-propagate T and N), with a worked example on a two-action tree, C = 2.

`mcts.py` Part A replays the worked example with his scripted rollout values (20, 10, 0, 14). It
reproduces every number he reads out: 21.67 and 11.67 at iteration 3, 11.48 and 12.10 at iteration 4,
root T 44 and N 4, a2 (s2) preferred. Exact to two decimals.

Part B puts the same algorithm (C 1.41, most-visited move) against a perfect minimax player at
tic-tac-toe, random among the minimax player's equally best moves. Perfect play draws, so a loss is the
only failure. `results.json` (20 games a side) and `confirm.json` (100 a side, new seed):

| Iterations a move | Losses as X (first) | Losses as O (second) |
|---|---|---|
| 10 | 13 of 20 | 17 of 20 |
| 50 | 2 of 20 | 16 of 20 |
| 200 | 0 of 20 | 6 of 20 |
| 1000 | 0 of 100 | 6 of 100 |
| 2000 | 0 of 100 | 1 of 100 |
| 5000 | 0 of 100 | 0 of 100 |

Verdict: works. Moving first it is safe from 200 iterations; moving second it needs ten times that and
still dropped one game in 100 at 2000. Never lost at 5000 (about 0.4 s a move in plain Python). The
second player's problem is the corner opening: only the centre reply holds, and random rollouts make
the edge replies look nearly as good until the tree is deep enough to see the forced loss.

Use for me: the Lichess bots are engines, not this, but the same budget question (how many playouts
before the second mover stops blundering) is a cheap first test for any game bot I build.
