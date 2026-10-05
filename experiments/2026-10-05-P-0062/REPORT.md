# P-0062, Lichess: any acceptance above 2000, or is every rated game worth +0?

Measured from tonight's standing job (5 Oct, `bin/lichess.py play --games 3 --minutes 12`) and
`games/lichess/GAMES.csv`. No extra challenges sent for the probe.

## Acceptance above 2000

25 bots rated 2000 or more were challenged tonight (3+2, rated):

| Answer | Count |
|---|---|
| accepted | 1 (arasanx, 2990) |
| declined | 9 |
| no answer in 30 s | 1 |
| refused with HTTP 400 before reaching the bot | 14 |

So 1 in 25, 4 percent. The 400 body was not logged, so why 14 refused outright is unknown (likely
bots that accept no rated or no bot challenges).

## Is every rated game +0?

No. The draw against arasanx (2990) moved me 3129 to 3057, -72. The +0 rows are the 4 Oct wins
against 1093 to 1251 bots: a 1,900-point gap makes a win worth nothing, not the provisional rating
itself. Rated play against strong bots does move the number, in both directions.

## A defect found on the way

After the two sub-2000 declines, the next 57 challenges all came back HTTP 429: I had rate-limited
myself and the script kept firing. Fixed tonight in `bin/lichess.py`: it now prints the error body
and stops the night on the first 429.
