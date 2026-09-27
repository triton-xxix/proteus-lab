# Track record

Every number here is computed from the committed ledgers by `bin/score.py`, never typed by hand.
A losing record is published in exactly the same format as a winning one.
An independent script that shares no code with the scorer recomputes every line monthly and on
every rebuild; see `audit/README.md` to run it yourself.

Rebuilt 2026-09-27 17:02 UTC at commit c18a784.

## The Grinder (meme-coin paper desk)

Current rules v0.2, £100.00 a position. Earlier rule versions are their own books, in the table below.

| Measure | Value |
|---|---|
| Paper bankroll | £933.38 (started £1000.00) |
| Positions opened | 8 |
| Positions closed | 4 |
| Positions scored at 24h | 4 |
| Hit rate | 0.25 |
| Expectancy per position | £-16.66 |
| Expectancy as a share of the stake | -16.7% |
| Positions that rugged | 0 |

| Rule version | Stake | Opened | Closed | Expectancy | Share of stake | Bankroll | Rugged |
|---|---|---|---|---|---|---|---|
| v0.1 | £5.00 | 6 | 6 | £-1.08 | -21.5% | £93.54 (from £100.00) | 1 |
| v0.2 | £100.00 | 8 | 4 | £-16.66 | -16.7% | £933.38 (from £1000.00) | 0 |

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
| Things installed and run | 1 |
| Weekly notes shipped | 1 |
| Luke-gates opened | 0 (must stay 0; asserted, not computed) |

## Spend

| Month | Spent | Cap |
|---|---|---|
| 2026-09 | £0.00 | £50.00 |

