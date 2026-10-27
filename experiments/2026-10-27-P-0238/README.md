# P-0238: does the closing price drift toward the Pitch model's side?

This came from refill source 36. football-data's notes say its pre-close odds are collected on Friday afternoon (Tuesday for midweek games), and the closing odds are the same columns with a C added.

## Method

I matched 257 committed Pitch predictions to played 2026-27 matches in `pitch/cache/`. Another 22 did not match on kickoff date and team names. Both the Avg (pre-close) and AvgC (closing) prices have the bookmaker margin removed.

For each match, the model's side is the outcome where its probability beats the pre-close market by the most. A hit means the closing probability of that side rose. The control repeats the count on a random side for each match, 10,000 times. Script: `p0238.py`. Rows: `results.json`.

## Result

- All 257 matches: 137 hits (53.3%). A random side averages 130.1 hits, so the gap gives p = 0.20. The mean move on the model's side is +0.06 points of probability.
- Edge of 5 points or more (157 matches): 93 hits (59%), with a mean move of +0.27 points.

## Reading

There is a faint lean in the right direction, and it is stronger where the model disagrees more. It is not distinguishable from chance, and the moves are tiny (a quarter of a point) next to the 5+ point gaps the model claims. The market does not come round to the model in any way that matters. That fits the judgement-book and shadow-bet results so far.

This uses one season, and predictions are committed at different times relative to Friday's collection. It is worth re-running at the week-8 review with about twice the rows, not before.
