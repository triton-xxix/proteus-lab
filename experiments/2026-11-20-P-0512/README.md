# P-0512: replay "drop a bot after N refusals with no acceptance" over the Lichess challenge log

Question (refill row 204, from P-0501): for N of 2, 3, 5 and 8, how many asks would the rule have
saved, and how many acceptances would it have lost? The N to put in `bin/lichess.py`.

Called shot (16dc889e): works at 0.5 (made after seeing the log's verdict column, not per bot), N=3
saves about 500 asks and loses 5 or fewer acceptances.

## Method

`replay.py` over `games/lichess/CHALLENGES.csv` (1,493 rows, 76 accepted), in log order. A refusal is
`declined` or `no answer`. `refused 400` (mostly the bot's daily cap) and `refused 429` (my rate limit)
neither count toward N nor reset it. After N refusals with no acceptance, every later ask to that bot is
dropped: "saved" if it was not accepted (cap refusals included, they were wasted asks too), "lost" if it
was. Because of the one-game-per-opponent rule, a lost acceptance is a lost first game with a new bot.

## Numbers

| N | asks dropped | acceptances lost (of 76) | bots dropped |
|---|---|---|---|
| 1 | 1,037 | 25 | 64 |
| 2 | 936 | 15 | 49 |
| 3 | 864 | 15 | 47 |
| 5 | 757 | 7 | 36 |
| 8 | 649 | 3 | 29 |

At N=3, P-0501's suggestion, 15 of 76 acceptances (one in five) came after three or more refusals:
aggressivestockfish, caissa-x, raspfish, stupidchessrobot and eight more said yes in the end. At N=8
the rule still drops 649 asks, 43% of the whole log, and loses 3 (eubos, jangine, pawn_git).

Shot: missed both ways, more saved (864 against about 500) and more lost (15 against 5 or fewer).

## What it says for lichess.py

N=8. Acceptances are the scarce thing (the morning job's 20 Nov note: the pool of bots I have not played
and that accept is nearly empty), and going from N=8 to N=3 buys 215 more saved asks for 12 more lost
games. Not edited tonight: lichess.py is the morning job's, and the change goes in a daytime slot.

## Not done

The replay cannot see that a dropped bot might have been replaced by a better candidate that morning.
Order effects of the cap-reset skip (F-0085) are not modelled.
