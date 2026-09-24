# The Pitch: forecast rules (v0, written before the first prediction)

Question under test: does a weekly-refit Dixon-Coles model beat the closing line on English
football, and if so, where.

## Data (keyless, proven 2026-09-22)

football-data.co.uk: results, expected goals, opening and closing odds for the Premier League (E0)
and Championship (E1), last three seasons, plus the fixtures file with current average odds. No API
key, no account. The Odds API key in 1Password stays in reserve for a live closing-line feed.

Fixture fallback (added 2026-09-24, before any prediction existed; plumbing, not a rule change):
football-data's fixtures file only carries the next round and refreshes late in the week, so the
desk had never committed a row. fixturedownload.com publishes the whole season, keyless, without
odds. A fallback fixture is used only when football-data still lacks the match 48 hours before
kickoff. Such a row gets probabilities and no market line, so no paper bet. It is still scored on
Brier against the closing odds once results land.

## Model, version 0

Dixon-Coles bivariate Poisson with the low-score correction and exponential time decay (xi 0.0065
per day), fitted jointly on both divisions so promoted and relegated sides keep their strength. Home
advantage is one shared parameter. Light L2 shrinkage on attack and defence. Refit before every
prediction run. Output per fixture: P(home), P(draw), P(away), P(over 2.5).

Version 1 (not claimed yet): Elo blend, expected-goals priors, per-division home advantage.

## Publication rule

A prediction is committed with a UTC timestamp. Any row committed at or after kickoff is marked
LATE by `score.py` and excluded from every average. The git history is the proof.

## Scoring

Brier score on 1X2 per prediction (0 is perfect; a uniform guess scores 0.667 on three outcomes) and
its mean, beside the market's Brier from the closing average odds with overround removed
proportionally. Closing-line value on backed sides: model probability minus closing implied
probability. Calibration in ten bins on the lab page once there are enough rows.

## Paper bankroll

£100, quarter Kelly, backing the 1X2 side where model minus market exceeds 3 points, capped at £10
a bet, at the fixture file's average odds at commit time. No bet when no side clears the edge.

## Honesty line

Most published models do not beat the closing line. The point of the desk is a clean public record
either way. If eight weeks show no edge, that is the finding, and it gets published.
