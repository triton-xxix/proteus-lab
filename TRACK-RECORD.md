# Track record

Every number here is computed from the committed ledgers by `bin/score.py`, never typed by hand.
A losing record is published in exactly the same format as a winning one.
An independent script that shares no code with the scorer recomputes every line monthly and on
every rebuild; see `audit/README.md` to run it yourself.

Rebuilt 2026-10-18 17:04 UTC at commit fe4c3b3.

## The Grinder (meme-coin paper desk)

Current rules v0.2, £100.00 a position. Earlier rule versions are their own books, in the table below.

| Measure | Value |
|---|---|
| Paper bankroll | £11.33 (started £1000.00) |
| Positions opened | 83 |
| Positions closed | 83 |
| Positions scored at 24h | 81 |
| Hit rate | 0.313 |
| Expectancy per position | £-11.91 |
| Expectancy as a share of the stake | -11.9% |
| Positions that rugged | 7 |

| Rule version | Stake | Opened | Closed | Expectancy | Share of stake | Bankroll | Rugged |
|---|---|---|---|---|---|---|---|
| v0.1 | £5.00 | 6 | 6 | £-1.08 | -21.5% | £93.54 (from £100.00) | 1 |
| v0.2 | £100.00 | 83 | 83 | £-11.91 | -11.9% | £11.33 (from £1000.00) | 7 |

Every position is also rescored on its minute-candle price path in `grinder/PATHS.csv`, beside
what the ledger recorded, so a stop honoured late shows next to the stop the rule said.

## The Pitch (football forecast desk)

| Measure | Value |
|---|---|
| Predictions committed before kickoff | 174 |
| Predictions committed late (excluded) | 0 |
| Predictions scored | 34 |
| Predictions scored with a market line (the paired set) | 34 |
| Brier score, model (lower is better; 0.667 is a uniform guess on three outcomes) | 0.6028 |
| Brier score, market, same matches | 0.6099 |
| Paired Brier, model minus market (negative means the model is better) | -0.0071 |
| Closing-line value, mean | 0.0441 |
| Paper bankroll, quarter Kelly | £100.00 (started £100.00) |

## Field Notes

| Measure | Value |
|---|---|
| Things installed and run | 4 |
| Weekly notes shipped | 4 |
| Luke-gates opened | 0 (must stay 0; asserted, not computed) |

## Probes

One new thing a night taken to a verdict. Kills are published here in the same table as wins.

| Measure | Value |
|---|---|
| Probe verdicts | 165 |
| Works | 123 |
| Broken | 5 |
| Blocked | 25 |
| Not worth it | 12 |
| Killed | 4 (1 by the cull rule, 3 on Luke's word) |
| Still open | 7 |

## Spend

| Month | Spent | Cap |
|---|---|---|
| 2026-10 | £0.00 | £50.00 |

