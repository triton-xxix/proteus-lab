# P-0255: do my bot's draws come from moving too fast?

**Question.** Across every rated game of tritonxxix on Lichess, measure the real seconds my bot spent per
move from the game clocks, and test whether draws come with faster moves than wins.

**Pull.** The per-user export (`api/games/user/tritonxxix`) answered `{"error":"Not found"}` keyless, though
`api/user/tritonxxix` is public (61 games, 60 rated; 44W 16D 1L over all 61, so 43 rated wins plus
one unrated). Routed around: `fetch.py` posts the 60 ids in
`games/lichess/GAMES.csv` to the keyless by-ids export. 60 sent, 60 back, all 3+2.

**Method.** `think_time.py`: think on an own move = previous own clock + 2 s increment - own clock after.
First own move skipped. Per game the mean of those; then draws v wins, Mann-Whitney two-sided.

**Called shot.** works at 0.75, "median think in draws within 0.3 s of wins, Mann-Whitney p above 0.2".
Medians hit (0.47 v 0.49 s). p missed narrowly (0.189).

**Numbers.**

| result | games | median of per-game mean think | mean |
|---|---|---|---|
| win | 43 | 0.49 s | 0.72 s |
| draw | 16 | 0.47 s | 0.73 s |
| loss | 1 | 10.18 s | 10.18 s |

Mann-Whitney draw v win: U 421.5, p 0.19. Median opponent rating: draws 3003, wins 1906. Correlation of
per-game think with opponent rating: +0.16.

**Reading.** Draws do not come from moving faster; they come from opponents rated about 1100 points
higher. The bot moves in about half a second, well under the 1.0 s a move that D-010 registered, which
is worth a look. The one loss averaged 10 s a move, twenty times the usual: that game looks like a lag or
hang, not a chess loss.

**What I did not do.** Did not check the per-game think against GAMES.csv's `think_s` column or the date
D-010 took effect (queued as P-0256). Did not open the loss game's moves. Increment arithmetic assumes
no lag compensation.
