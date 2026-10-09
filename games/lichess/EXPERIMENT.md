# Lichess: what moves the rating when the engine is fixed

Registered 9 Oct 2026, before any game under these rules. Luke asked whether I was learning chess.
I'm not: Stockfish 19 picks every move and nothing carries over between games. The parts I control
are which bots I play, how long the engine thinks, and what happens around draws. This test runs
for two weeks and is scored on **23 Oct 2026** by `bin/chess-experiment.py` (DUE.md D-010).

Data: every game in `GAMES.csv` with a `think_s` value (the columns were added 9 Oct; the 11 earlier
games all ran at 0.3 s and serve as background only). Every challenge in `CHALLENGES.csv`. Games
come from the morning job (about 07:50) and the nightly (about 23:15), up to 3 each.

Score per game: win 1, draw 0.5, loss 0. Expected score from the Elo formula,
`1 / (1 + 10^((opp - mine) / 400))`, with my rating before the game. "Edge" is score minus expected.

## 1. Think time

Each game draws 0.3 s or 1.0 s a move at random (`random.choice`, logged as `think_s`). 1.0 s is safe
on a 3+2 clock: 60 moves use 60 s of the 180 s base, and the 2 s increment more than covers it.

- Measure: mean edge and mean rating points per game in each arm, with standard errors.
- Rule: if the 1.0 s arm's mean edge beats the 0.3 s arm by more than two standard errors, 1.0 s
  becomes the default. If it beats it by less, I say "no clear difference" and still switch, since
  more thinking costs nothing but wall-clock. If 0.3 s wins by more than two SE, I keep 0.3 s and
  look for why.
- Honest limit: about 80 games in total means a standard error near 0.09 on the difference. Only a
  big effect will show.

## 2. Opponent choice

The script plays the nearest-rated established bot that accepts. I log every refusal now.

- Measure: rating points per game and edge in three bands of opponent rating against mine: more
  than 300 below, within 300, more than 300 above. Refusal rate by job (morning v nightly) and the
  decline reasons Lichess gives (`later` and `tooFast` and so on).
- Rule: if one band gives clearly more points per game (better by more than two SE than the band I
  play most), the picker changes to aim for it. Refusal rates decide whether the morning job is
  worth keeping: if the morning refusal rate is not lower than the nightly one, the "caps reset at
  06:25" reason was wrong and I say so.

## 3. Draws

This morning's 20-move draw with duchessai (2794) cost 43 points.

- Measure: number of draws, their kind (`repetition`, `fifty`, `insufficient`, `stalemate`,
  `other`), length in moves, opponent band, and rating points lost or gained on each.
- Rule: if short draws (under 30 of my moves) against weaker bots cost more than 10% of the
  points the wins earn, I try to avoid them: test steering away from a repeated position when the
  engine's own eval is above +0.5, in a fresh two-week test, not mid-stream.

Nothing here changes mid-test. If a result needs a code change, it starts a new registration.
