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

## Amendment, 30 Sep 2026 16:05 BST, before any trade had closed

Seen in the first 12 entries: some Jupiter prices at entry had almost no liquidity behind them ($9
to $11, prices about 400 times below the pool's) and one token was entered twice when two migration
messages for it raced. Neither can be traded. So, before any outcome existed:

- **Counted** trades now also need Jupiter liquidity of at least **$5,000 at entry**. Entries below it
  are still recorded and reported, never counted. This is a tightening.
- A token is entered at most once; the watcher now claims the mint before it prices it.

## Verdict on the book above, 3 Oct 2026: KILL

At 2,252 counted trades the primary expectancy was -£14.2 per £100; the KILL line (at or below -£10
at 200) was crossed days earlier and the nightly reported the number without comparing it. Recorded
3 Oct. The book is closed; its trades stay published.

## G2: the same trade, only into pools with at least $50,000 of liquidity

Registered 3 Oct 2026 about 11:35 UTC, before any trade it will count exists. Unlike the first book
this one is chosen after looking: on 3 Oct I searched 48 filter and exit combinations (liquidity
band, latency, hour of day, the four exits) on the first half of the counted trades by time, took
the best, and scored it on the second half it had not seen (`experiments/2026-10-03-graduation-filters/`).
No combination was positive on the first half. The best, entry liquidity at or above $50,000 with
the primary exit, was -£3.05 on 116 trades in the first half and +£7.65 on 125 in the second, with
62 to 66 percent winners and about one in ten at or below -50 percent (the whole book: 26 percent
and two in three). With its best ten trades removed the second half was -£9.75, so the positive
number leans on a few winners. That is a lead, not a result, and only fresh trades can test it.

- **Same watcher, same entry, same exits, same costs** as above. Nothing in `watcher.py` changes.
- **Counted:** primary-exit trades with latency at most 120 seconds, Jupiter liquidity at entry at
  least **$50,000**, and a migration block time at or after **2026-10-03T12:00:00Z**. Nothing before
  that time counts, including the 241 trades the filter was found on.
- **Pass marks:** the first book's lines unchanged. KEEP at 400 counted: expectancy at least +£10,
  at or above zero with the best 10 removed, at most 25 percent at or below -50 percent. KILL at 400
  if expectancy is at or below zero, or at 200 if at or below -£10. Anything else at 400 is KILL
  too: there is no third variant from this data.
- **Running:** the watcher stops on its own at 2026-10-07T15:08Z, likely short of 400 at about 80
  counted trades a day. If it is, I reload it once from this folder for a fresh 7-day window and
  say so in the run log; counting carries on across the gap.
- `bin/killcheck.py` reports this book every night against these lines.

## Verdict on G2, 8 Oct 2026: KEEP

At 403 counted trades (killcheck, 8 Oct about 22:45Z) the primary expectancy was +£45.03 per £100,
+£0.13 with the best ten removed, and 14 percent at or below -50 percent. All three KEEP lines are
met, so by the rule written on 3 Oct this is KEEP. Said plainly so the word does not do more work
than it should: the best-ten line passes by thirteen pence, so the whole edge sits in about ten
trades out of 403, and these are paper fills on Jupiter's quoted price with modelled impact and
slippage, not fills anyone took. KEEP means the book carries on and earns its next test, which is
whether the fills survive: the next step is a fill-realism check on the 403 (quoted price against
what the pool would actually have given at entry size), pre-registered in `DUE.md` tonight before
anyone runs it.
