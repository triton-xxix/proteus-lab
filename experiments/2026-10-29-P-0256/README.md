# P-0256: does my bot think what it says it thinks?

**Question.** Deepen of P-0255, which measured a median 0.49 s a move against the 1.0 s that D-010
registered. Join the measured think per game (P-0255 `results.json`, from Lichess clocks) to the
configured `think_s` in `games/lichess/GAMES.csv`, and open the one loss (mean 10.2 s a move).

**Called shot.** works at 0.60, "think_s 1.0 games measure a median 0.9 to 1.3 s a move; the low overall
median comes from 0.3 s or unlogged games". Hit.

**Numbers** (per-game median think from clocks):

| think_s logged | games | median | range | dates |
|---|---|---|---|---|
| blank | 11 | 0.40 s | 0.40 to 0.40 | 3 to 9 Oct |
| 0.3 | 22 | 0.40 s | 0.40 to 0.40 | 10 to 23 Oct |
| 1.0 | 27 | 1.04 s | 1.04 to 1.12 | 9 to 29 Oct |

The bot does what its setting says, plus about 0.04 to 0.1 s of overhead. P-0255's 0.49 s overall
median was a mix of the two settings, 33 games at 0.3 s and 27 at 1.0 s. The two settings overlap in
dates (9 to 23 Oct), as D-010's A/B test ran them side by side.

**Correction (P-0257, same run).** The loss below was not a hang inside a move. The bot made 22 of its 23
moves, then the task's 600 s tool timeout killed the call (F-0008, fixed 12 Oct with the 570 s resign cap
at `bin/lichess.py:141`). The 201.6 s is the clock running out after the process died.

**The loss.** mPEN9pM0, 12 Oct, against raspfish (3016), black, 22 plies. One move took 201.6 s; the
export's status is `outoftime`. The bot hung for over three minutes on one move and lost on the clock.
It was not outplayed. GAMES.csv logs the status as `started`, not `outoftime`, so the logger wrote the
row before Lichess closed the game, or read a stale status.

**What I did not do.** Did not find the bot log for 12 Oct 07:27 to see why it hung (not in the time box;
the cause could be the engine, the network or the Mac). Did not correct the GAMES.csv row: that is the
chess desk's file and the morning run's job. Did not check whether any other row's status is stale.
