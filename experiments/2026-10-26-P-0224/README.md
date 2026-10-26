# P-0224: Lichess cloud eval as referee for P-0214

**Question.** How many of P-0214's 32 positions (plies 16, 24, 32, 40 from my last 8 Lichess games)
does `lichess.org/api/cloud-eval` cover, and on the covered ones does P-0214's ranking (quiescence
beats plain on move cost) hold with cloud evals in place of local Stockfish 19 depth 14?

**Called shot.** works at 0.60, "cloud covers about 10 of 32 positions, mostly the move-9 ones".
One move-9 position had been looked at before the shot (to check the endpoint answers at all).

**Method.** `cloud_referee.py`: one keyless GET per position, `multiPv=5`, 1.5 s apart, no 429s.
A move is costed against the cloud's best line only when it is among the cloud's five lines;
otherwise it is counted as "outside top 5", not guessed.

## Numbers

| | value |
|---|---|
| covered | **10 of 32** (ply 16: 6 of 8, ply 24: 2, ply 32: 2, ply 40: 0) |
| median cloud depth | 21 (range 18 to 25) |
| cloud best move = Stockfish d14 best move | 8 of 10 |

On the 10 covered positions:

| | plain | quiescence |
|---|---|---|
| agrees with cloud's move | 4 | 7 |
| move outside cloud's top 5 | 4 | 1 |
| mean cost v cloud (costed moves only) | 26.7 cp on 6 | 6.9 cp on 9 |
| mean cost v Stockfish d14, same moves | 47.0 cp | 10.1 cp |
| blunders over 200 cp v cloud | 0 | 0 |

## What it says

The ranking holds where the cloud can see: quiescence is the better engine on every column, and
plain's four moves outside the top five make the gap wider than the costed means show. The cloud and
local Stockfish agree on the best move in 8 of 10, so P-0214's referee was not the weak link.

But the cloud is no referee for my games. It covers the opening, thins out by move 13 and has none of
the eight move-21 positions, which is where P-0214's blunders were. Ten positions, mostly early, is
too few to rank engines on.

## Not done

- No fallback query on the position after each engine's move (would cost plain's four uncosted
  moves properly); python-chess was not needed for the main question and was left out.
- No significance test: n = 10, and this is not a trading or forecasting claim.
