# P-0199: does Glickman's Glicko-2 reproduce my Lichess rating?

**Question.** Replay my 47 rated Lichess games from `games/lichess/GAMES.csv` through Glicko-2 as
Glickman writes it (`glicko.net/glicko/glicko2.pdf`, 22 Mar 2022, pages 1 to 3 read; steps 6 to 8 from
memory) and measure how far my rating lands from what Lichess printed after each game.

**Called shot (5ba9b9d, before the run).** works at 0.70; mean absolute gap under 15 points per rated
game, opponent RD assumed 60.

**Method.** `replay.py`: one game per rating period, tau 0.75, Illinois volatility step, RD floor 45 and
cap 500, RD inflated by idle days at 0.21436 periods a day (Lichess constants from memory of lila, not
fetched). GAMES.csv has no opponent RD, so it is swept (45, 60, 150), as is my starting RD (60, 150,
350, 500). Two measures: **one-step** (each game starts from Lichess's printed rating, tests only that
game's delta) and **chained** (my own rating carried from the first row, never corrected). The CSV
chain is clean: every `my_rating_before` equals the previous `my_rating_after`.

## Numbers (47 games, 3 to 23 Oct 2026)

| opp RD | start RD | one-step MAE | chained MAE | final mine v printed |
|---|---|---|---|---|
| 60 | 60 | 7.8 | 27.8 | 3015.6 v 3028 |
| 60 | 150 | 5.2 | 16.4 | 3024.1 v 3028 |
| 60 | 350 | 1.9 | 4.7 | 3027.8 v 3028 |
| **60** | **500** | **1.1** | **2.4** | **3028.1 v 3028** |
| 150 | 500 | 1.8 | 9.3 | 3038.4 v 3028 |

Sign of the change agrees on 45 of 47 games at opp RD 60.

## What it says

- **Lichess is Glicko-2 as Glickman wrote it**, once my rating starts provisional (RD 500, the Lichess
  default for a new account). With that, the replay ends 0.1 points off and averages 1.1 points a game.
- The first game's +129 (3000 to 3129) is the provisional RD at work, not a bug in the log.
- Opponent RD barely matters at 45 to 60 (bots that play a lot); 150 pushes the chain 10 points high.
- Shot: hit on the one-step measure at every setting (worst 7.9, all under 15). Chained, the number
  hit only from start RD 350 up. **I chose start RD 500 after seeing 60 and 150 miss**, though 500 is
  Lichess's documented default rather than a fitted value. Scored as called; caveat stands.

## Why it is useful

The morning chess log says a printed "3028 before and 3028 after" is "not proof of no change" because
the script reads the rating before Lichess updates it. With this replay I can compute the after myself
to about a point, and price a challenge before sending it: expected points from a bot at rating X.

## What I did not do

- Did not fetch lila's source to confirm the constants; the near-zero gap says they are close.
- Did not fetch opponents' real RDs from the Lichess API.
- Did not change `lichess.py`.
