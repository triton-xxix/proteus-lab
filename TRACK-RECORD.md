# Track record

Every number here is computed from the committed ledgers by `bin/score.py`, never typed by hand.
A losing record is published in exactly the same format as a winning one.
An independent script that shares no code with the scorer recomputes every line monthly and on
every rebuild; see `audit/README.md` to run it yourself.

Rebuilt 2026-09-25 06:57 UTC at commit 259a9d6.

## The Grinder (meme-coin paper desk)

Current rules v0.2, £100.00 a position. Earlier rule versions are their own books, in the table below.

| Measure | Value |
|---|---|
| Paper bankroll | £1000.00 (started £1000.00) |
| Positions opened | 0 |
| Positions closed | 0 |
| Positions scored at 24h | 0 |
| Hit rate | n/a |
| Expectancy per position | n/a |
| Expectancy as a share of the stake | n/a |
| Positions that rugged | 0 |

| Rule version | Stake | Opened | Closed | Expectancy | Share of stake | Bankroll | Rugged |
|---|---|---|---|---|---|---|---|
| v0.1 | £5.00 | 6 | 2 | £-1.59 | -31.8% | £96.82 (from £100.00) | 0 |
| v0.2 | £100.00 | 0 | 0 | n/a | n/a | £1000.00 (from £1000.00) | 0 |

Every position is also rescored on its minute-candle price path in `grinder/PATHS.csv`, beside
what the ledger recorded, so a stop honoured late shows next to the stop the rule said.

## The Pitch (football forecast desk)

| Measure | Value |
|---|---|
| Predictions committed before kickoff | 0 |
| Predictions committed late (excluded) | 0 |
| Predictions scored | 0 |
| Predictions scored with a market line (the paired set) | 0 |
| Brier score, model (lower is better; 0.667 is a uniform guess on three outcomes) | n/a |
| Brier score, market, same matches | n/a |
| Paired Brier, model minus market (negative means the model is better) | n/a |
| Closing-line value, mean | n/a |
| Paper bankroll, quarter Kelly | £100.00 (started £100.00) |

## Field Notes

| Measure | Value |
|---|---|
| Things installed and run | 0 |
| Weekly notes shipped | 0 |
| Luke-gates opened | 0 (must stay 0; asserted, not computed) |

## Spend

| Month | Spent | Cap |
|---|---|---|
| 2026-09 | £0.00 | £50.00 |

