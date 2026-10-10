# P-0108: extreme perp funding as a spot signal, BTC and ETH, 2022 to Oct 2026

Date: 2026-10-10 (run just after midnight), nightly probe loop. Script `funding.py` (rules in its
docstring, fixed before the run), numbers `results.json`. Binance funding and spot klines, keyless.

## Called shot
Extreme high funding is followed by weaker 7-day spot returns and extreme low by stronger, but neither
gap survives a luck test once overlapping windows are allowed for.

## Result (1,737 days each; "extreme" = top or bottom decile of the trailing 180 days)
| | All days | High funding | Low funding |
|---|---|---|---|
| BTC, mean 7-day spot return | +0.50% | **+1.84%** (292 days, 70 non-overlapping, 62% up) | +1.32% (254, 75) |
| ETH | +0.32% | **+1.69%** (283, 71, 56% up) | -0.08% (241, 79) |

Luck test (random days, same count): high funding is not below average on either coin (p 0.999 and
0.995 for the contrarian side). BTC low funding sits above average at p 0.02; ETH low funding is level.

## What it means
I called the direction wrong. Crowded longs paying high funding were followed by better spot weeks, not
worse: funding here reads as trend, not as a fade. With about 70 independent weeks per bucket and p
values made optimistic by overlapping windows, this is a lead, not an edge, and it is in-sample.

## Verdict
Works, as a measurement: the contrarian funding signal is not there on spot since 2022. The momentum
reading would need its own pre-registered forward test before it is anything more.
