# P-0237: win rate against entry price, football closing odds

The question came from harvest item H-0424: do heavy favourites win most often, yet return at or below zero at the closing odds?

The data is every result in `pitch/cache/`: football-data CSVs for nine leagues over five seasons. I took 13,419 matches with average closing odds, and 11,025 of them also have Pinnacle closing odds (the Pinnacle columns are missing on some rows). Each outcome (home, draw, away) is treated as a one-unit bet at its closing price and grouped by that price. Script: `p0237.py`. Numbers: `results.json`.

## Result

| Price | Pinnacle win | Pinnacle ROI | Average-close ROI |
|---|---|---|---|
| 1.0-1.3 | 0.842 | +0.9% (se 1.4) | +0.1% |
| 1.3-1.5 | 0.720 | +0.3% (se 1.9) | -2.4% |
| 1.5-1.8 | 0.595 | -1.9% | -3.8% |
| 1.8-2.2 | 0.500 | -0.6% | -3.1% |
| 2.2-3.0 | 0.384 | -2.1% | -4.9% |
| 3.0-5.0 | 0.263 | -4.1% | -5.8% |
| 5.0-10 | 0.138 | -13.6% (se 3.3) | -16.7% |
| 10+ | 0.054 | -28.6% (se 8.9) | -42.1% |

Backing the favourite in every match wins 54% of the time and returns -0.5% at Pinnacle and -2.2% at the average close.

## Reading

Yes on both counts, but the shape matters more than the yes. Heavy favourites win most often and return about zero: under 1.5 at Pinnacle the ROI is +0.3% to +0.9%, inside one standard error of nothing. The losses grow steadily as the price lengthens, down to -29% on 10+ shots. That is the favourite-longshot bias, and it shows clearly even at the sharpest closing line.

A high win rate is not an edge. Nothing in this table beats the closing line once the error is counted. The usable lesson for the Pitch is about where it backs: shadow bets on long prices carry about four times the bookmaker's margin of short ones.

This is in-sample, it ignores staking, and it uses closing prices that nobody can actually get at kickoff.
