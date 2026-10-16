# P-0168, which ten-match KPI predicts the next ten? (16 Oct 2026)

Refill from Soccermatics (David Sumpter), lesson 5, Team KPIs: track a team on a shot-quality trend
rather than its points, because points carry more luck. I have no xG, but football-data.co.uk has shots
on target for every match in the Pitch's nine leagues, so I tested the cheap version.

`kpi.py`: four complete seasons (2022/23 to 2025/26), nine leagues, every team cut into non-overlapping
pairs of ten-match blocks. Predictors from the first block, per game: shots-on-target difference, goal
difference, points. Target: points per game in the next ten. 1,444 block pairs. Output `result.json`.

| predictor (10 matches) | r with next 10 matches' points |
|---|---|
| shots-on-target difference | **0.594** |
| goal difference | 0.563 |
| points per game | 0.543 |

- Shots on target beat goal difference in 8 of 9 leagues and points in 8 of 9. The exception is Serie A,
  where goal difference (0.655) and points (0.651) both edge shots on target (0.626).
- Bootstrap over blocks, 1,000 resamples: shots on target minus goal difference in r is +0.008 to +0.054
  (95%), so the edge is small but not noise.
- Points per game, the number tables and pundits use, is the worst of the three everywhere but Italy.

Verdict: works. The lesson's claim holds on free data with the crudest shot measure there is.

Correction, same night: I wrote here that a shots term was the next test for the Pitch and queued it
(P-0169). It already exists: `pitch/backtest.py` runs a `sot` model, which beats goals-only Dixon-Coles
every season and never the market. This probe agrees with that backtest; it adds nothing the desk lacks.
