# P-0171: what think time buys the Lichess bot on its own positions

**Question.** The Chess Programming Wiki's Time Management page (refill source, 17 Oct) gives the basic
scheme as base/20 + increment/2 per move, about 10 s on our 3+2 clock. The live think-time test
(EXPERIMENT.md section 1, D-010, scored 23 Oct) plays 0.3 s against 1.0 s. How much move quality do
those arms differ by, measured offline on positions from my own games?

**Method.** `thinktime.py` (run under `.venv`, which has python-chess) takes the position after ply 30
from each saved PGN, the first 24 games with enough moves. The bot's own Stockfish binary, on the same
default options as `bin/lichess.py` (1 thread, default hash cleared before each search), plays each
position at 0.3, 1.0 and 3.0 s. A depth-20 search then scores every candidate move with `root_moves`,
so all moves are judged by the same yardstick. Loss = best score minus the move's score, floored at 0.

**Numbers** (`results.json`, 24 positions)

| arm | mean cp loss | se | same move as reference | moves losing over 50 cp |
|---|---|---|---|---|
| 0.3 s | 2.96 | 1.65 | 18 of 24 | 0 |
| 1.0 s | 1.21 | 0.68 | 21 of 24 | 0 |
| 3.0 s | 0.46 | 0.35 | 24 of 24 | 0 |

Paired, 0.3 s minus 1.0 s: **+1.75 cp a move (se 1.64)**. The worst single pick at 0.3 s cost 36 cp.

**Called shot.** 3 to 10 cp more per move at 0.3 s. Measured 1.75, so a miss: Stockfish at 0.3 s is
already close to its 1.0 s move on these positions.

**Reading.** A gap of under 2 cp a move, with no move losing more than 50 cp, is far too small for an
80-game live test to separate. Its own registration says it would need a big effect, and this isn't one.
Expect D-010's think-time section to read "no clear difference". Its rule already switches to 1.0 s in
that case, and this agrees with that choice: 1.0 s is slightly better and costs nothing but wall-clock.

**What I did not do.** One position per game, all at ply 30, so no openings and no endgames. The
depth-20 yardstick agrees with the 3 s move every time, so it is about 3 s strength. Losses are measured
against that, not against a much deeper search. There is no game-level effect: centipawns are not points,
and against 2800 to 3000 bots a single 36 cp slip can still decide a game.
