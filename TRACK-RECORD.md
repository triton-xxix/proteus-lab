# Track record

Every number here is computed from the committed ledgers by `bin/score.py`, never typed by hand.
A losing record is published in exactly the same format as a winning one.
An independent script that shares no code with the scorer recomputes every line monthly and on
every rebuild; see `audit/README.md` to run it yourself.

Rebuilt 2026-10-13 08:06 UTC at commit ec9bd32.

## The Grinder (meme-coin paper desk)

Current rules v0.2, £100.00 a position. Earlier rule versions are their own books, in the table below.

| Measure | Value |
|---|---|
| Paper bankroll | £822.22 (started £1000.00) |
| Positions opened | 68 |
| Positions closed | 68 |
| Positions scored at 24h | 68 |
| Hit rate | 0.353 |
| Expectancy per position | £-2.61 |
| Expectancy as a share of the stake | -2.6% |
| Positions that rugged | 2 |

| Rule version | Stake | Opened | Closed | Expectancy | Share of stake | Bankroll | Rugged |
|---|---|---|---|---|---|---|---|
| v0.1 | £5.00 | 6 | 6 | £-1.08 | -21.5% | £93.54 (from £100.00) | 1 |
| v0.2 | £100.00 | 68 | 68 | £-2.61 | -2.6% | £822.22 (from £1000.00) | 2 |

Every position is also rescored on its minute-candle price path in `grinder/PATHS.csv`, beside
what the ledger recorded, so a stop honoured late shows next to the stop the rule said.

## The Pitch (football forecast desk)

| Measure | Value |
|---|---|
| Predictions committed before kickoff | 97 |
| Predictions committed late (excluded) | 0 |
| Predictions scored | 22 |
| Predictions scored with a market line (the paired set) | 22 |
| Brier score, model (lower is better; 0.667 is a uniform guess on three outcomes) | 0.6028 |
| Brier score, market, same matches | 0.6131 |
| Paired Brier, model minus market (negative means the model is better) | -0.0102 |
| Closing-line value, mean | 0.0441 |
| Paper bankroll, quarter Kelly | £100.00 (started £100.00) |

## Field Notes

| Measure | Value |
|---|---|
| Things installed and run | 3 |
| Weekly notes shipped | 3 |
| Luke-gates opened | 0 (must stay 0; asserted, not computed) |

## Probes

One new thing a night taken to a verdict. Kills are published here in the same table as wins.

| Measure | Value |
|---|---|
| Probe verdicts | 116 |
| Works | 83 |
| Broken | 5 |
| Blocked | 19 |
| Not worth it | 9 |
| Killed | 4 (1 by the cull rule, 3 on Luke's word) |
| Still open | 18 |

## Spend

| Month | Spent | Cap |
|---|---|---|
| 2026-10 | £0.00 | £50.00 |

