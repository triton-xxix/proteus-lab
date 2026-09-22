# The Pitch: forecast rules (v0, written before the first prediction)

Question under test: does a weekly-refit Dixon-Coles model blended with Elo beat the closing line
on English football, and if so, where.

## Data

- football-data.org free tier: fixtures, results, standings (Premier League, Championship).
- Understat: expected goals per match for the attack and defence strength priors.
- The Odds API free tier (500 requests a month): pre-match and closing 1X2 and totals odds.
  Key exists in 1Password; Luke tags it `proteus`.

## Model

Dixon-Coles bivariate Poisson with time decay (half-life 3 months), home advantage, and the
low-score correction, refit every Sunday on the last 2 seasons plus the current one. Blended 70/30
with an Elo rating updated per match. Output per fixture: P(home), P(draw), P(away), P(over 2.5).

## Publication rule

Predictions for the coming week are committed by 23:59 the day before the earliest kickoff. Any
prediction committed after its kickoff is excluded from scoring automatically (`score.py` compares
commit time to kickoff).

## Scoring

Brier score per prediction and mean, against the market's implied probabilities (overround
removed proportionally) on the same matches. Closing-line value: the model's probability minus the
closing implied probability on the side the paper bankroll backed. Calibration in ten bins.

## Paper bankroll

£100, fractional Kelly at one quarter, backing any side where model probability exceeds the
closing implied probability by more than 3 points. Flat £2 comparison line beside it. Bookmaker
odds at the time of commit, not the best available.

## Honesty line

Most published models do not beat the closing line. The point of the desk is a clean public record
either way. If eight weeks show no edge, that is the finding, and it gets published.
