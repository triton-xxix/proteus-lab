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

## Note, 2026-09-24: the backtest verdict, written before the first live prediction

The international break (21 Sep to 6 Oct) left the desk with no fixtures, so the question was put to
the history instead. `pitch/backtest.py` refits every model each week on all matches before that
week and scores the week's matches against football-data's average pre-close and closing prices,
overround removed proportionally, on Brier, RPS and log loss, plus the log-opinion-pool weight the
model earns against the closing line and a replay of the paper rule above at pre-close odds with
closing-line value. History: nine leagues (E0, E1, SP1, D1, I1, F1, N1, P1, SC0), 2022-23 onward
for fitting, 2024-25 and 2025-26 in full plus 2026-27 to date as test seasons, 6,766 scored matches.

Three models, all in `pitch/models.py`: the v0 Dixon-Coles; a goal-difference Elo with an ordered
logit for 1X2; and a Poisson on a half-goals, half-shots-on-target target as the expected-goals
stand-in (football-data's xG columns only begin in 2026-27 and Understat is blocked from here).
A fourth line, the blend, pools all three with the pre-close price using weights fitted on the
other season.

Result. RPS over all 6,766 matches: closing 0.1964, pre-close 0.1972, shots-Poisson 0.2026, Elo
0.2047, Dixon-Coles 0.2061. Every model earns a pool weight of 0.00 against the closing price on
each full season and on all matches together, and the blend fitted on one season puts 0.00 on
every model when applied to the other. The paper rule loses for every model in every league on
both full seasons; the best full-season line is Dixon-Coles in Portugal 2025-26 at +0.4 percent
over 208 bets, and it is -3.3 percent over both seasons there. Closing-line value sits within a
point of zero everywhere. The per-league pool weights above zero in 2026-27 are on 34 to 93
matches and mean nothing yet. Full tables in `pitch/backtest/REPORT.md`.

What the leagues taught. No league is soft to these models; the gap to the market is smallest in
the Premier League, not in Portugal or Scotland. The market moves most between average and close
in Portugal, which is where closing-line value would live if a model could find it, and none did.
More leagues did not improve any model's ranking; what they did was triple the sample, make the
negative clean, and give the desk fixtures on every weekend of the season.

Decisions, all before any live row exists:
- The v0 paper bankroll does not bet. Rows still record the side the rule would have backed and
  its odds, so closing-line value is scored, but the stake is 0. It stays 0 until a model earns a
  pool weight above zero out of sample in this harness, in a dated note.
- The live desk widens to all nine leagues from 9 October, one Dixon-Coles fit per country, so the
  calibration record fills at about 90 matches a week instead of 22 and is never dark for a break.
- The live model stays the pre-registered v0 Dixon-Coles. It is the worst of the three here, and
  that is the point: the live record tests whether the harness's ranking holds on matches nobody
  had seen when the code was written. If it does, the harness is trusted for the next model.
- Version 1 candidates go through `backtest.py` first. Nothing is promoted on prose.

The honesty line above said most published models do not beat the closing line. These three do not
either. That is the finding.
