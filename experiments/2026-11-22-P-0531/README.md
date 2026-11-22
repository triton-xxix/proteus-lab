# P-0531: Lichess acceptance by hour and weekday

Question: is there an hour when the bot pool says yes more often than at the morning job's 08:00 UTC,
by 10 points or more on 50 or more asks? Refill row 220.

## Method

`hours.py`, on disk only: `games/lichess/CHALLENGES.csv`, 1,531 rows, 9 Oct to 22 Nov 2026. Accepted
means the verdict starts "accepted" (77 rows); declined 875, refused 419, no answer 160.

## Numbers

- By hour (asks, accept rate): 06h 252, 6.0%; 07h 681, 4.1%; 08h 426, 5.6%; 22h 139, 4.3%; 11h 25,
  12.0%; 23h 8, 12.5%. **No hour with 50+ asks sits 10 points above 08h.** The only higher rates are on
  25 and 8 asks.
- By weekday: Wednesday 8.6% (152 asks) is best, Sunday 3.4% (266) worst; the spread is 5 points on
  small counts.
- The clearest pattern is the date, not the hour: week 41 (the first, fresh pool) ran 13.6% to 18.8%
  at 06h to 07h; every later week sits 2% to 8.5%.

## What I did not do

No significance test (77 acceptances in all); no per-bot control (the same bots are asked across
hours). The hours on file are only those the jobs ran at, so this cannot say anything about 14h to 20h.
