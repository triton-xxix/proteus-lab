# The graduation book: paper rules

Written 30 Sep 2026, before the watcher has recorded a single trade. Luke asked for it the same day
("yes build the graduation watcher") after `experiments/2026-09-30-launch-flip/` found one lead in a
day of data: tokens bought within about a minute of graduating from pump.fun to PumpSwap and sold 20
to 30 minutes later made +£19 to +£27 a paper trade (150 pools, one day, in-sample), while every
launch-buying variant lost. This book tests that forward, with nothing tuned after this file.

Paper only. No wallet, no key, no order. Charter: a stake stays on the execution ladder, and this
book is the first rung.

## What counts as a graduation

A confirmed Solana transaction that mentions pump.fun's migration account
`39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg` and logs `Instruction: MigrateV2` (or `Migrate`),
received over the public RPC websocket (`logsSubscribe`, keyless). The token is the non-SOL mint
in the transaction's post token balances.

## Entry

At the first Jupiter price (`lite-api.jup.ag/price/v3`, keyless) the watcher can get for the mint
after it hears the migration. Entry price is that price; entry time is when it was fetched; latency
is entry time minus the transaction's block time, recorded on every trade. Every graduation heard is
entered; there is no selection. £100 paper stake each, no bankroll cap (the question is the average
trade, not sizing).

## Exits, four recorded, one primary

Prices are sampled every 15 seconds from Jupiter for every open position.

- **Primary (P): -50% stop, otherwise sell at 20 minutes.** The stop fills at the first sample at or
  below -50%, at that sample's price (not the level): a bot polling every 15 seconds gets no better.
- A: sell at 20 minutes. B: sell at 30 minutes. D: -50% stop, otherwise sell at 30 minutes.
- The time exit uses the first sample at or after the mark.
- A token with no price at the mark (Jupiter stops quoting) exits at its last sampled price and is
  flagged `stale`; if that last price is more than 5 minutes old it is scored as -100%.

## Costs

`grinder/paths.pnl_v02`, unchanged: 1% pool fee and $0.05 each side, constant-product price impact
from Jupiter's reported liquidity, 3% slippage on stops and 1% on time exits.

## Pass marks (also in PASS-MARKS.md)

Counted on primary-exit trades with latency at most 120 seconds, closed after this file's commit.

- **KEEP** at 400 such trades: expectancy at least +£10 per £100, still at or above zero with the
  best 10 trades removed, and at most 25% of trades at or below -50%.
- **KILL** at 400 if expectancy is at or below zero, or earlier at 200 if it is at or below -£10.
- Anything else at 400 is CHANGE: one written variant, a fresh 400.
- Trades with latency over 120 seconds are recorded and reported, never counted.

## Running

`watcher.py`, one long-running process under launchd (`com.proteus.graduates.plist`, loaded from
this folder, nothing written to `~/Library`). Stops itself 7 days after first start or on HALT.
Writes only under `grinder/graduates/`. Restarted by launchd only if it crashes.
