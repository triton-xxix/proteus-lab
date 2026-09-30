# Buy at launch, sell 20 to 30 minutes in (30 Sep 2026)

Luke's questions: can we buy right at the start and sell 20 to 30 minutes in, and why only pump.fun?
Data: every new Solana pool P-0032 logged over 24 hours (28 to 29 Sep), random samples per launchpad,
GeckoTerminal minute candles from each pool's first minute. Paper, £100 stake, v0.2 cost model,
in-sample, one day. Per-launchpad tables in `REPORT-<dex>.md`, code `flip.py`.

Three entries: the open of the first traded minute (a fantasy: in practice snipers take it inside the
first block), one minute later (a fast bot), and when our two-minute poller first saw the pool
(what we could actually do today).

## Data fault found on the way

Single-trade candles 10x to 30,000x the running price, often a pool's last trade in its first hour,
were being used as exit prices: one PumpSwap trade showed +£893,000. `clean()` now drops an isolated
candle more than 5x above its neighbours' median close. Downward prints are kept, because a lone low
print can be a real rug. The first published tables (before the fix) were wrong and are superseded.

## Result, at the entry we could actually get (poller), selling at 20 min

| Launchpad | Sample | Exp £ per trade | Winners | Best 3 removed |
|---|---|---|---|---|
| pump.fun launches | 300 | -11.3 | 2% | -12.7 |
| bags.fm launches | 100 | -9.7 | 3% | -10.7 |
| PumpSwap (tokens just graduated from pump.fun) | 150 | +6.3 (+11.5 with a -50% stop) | 50% | -5.1 (+0.1 with the stop) |
| Meteora DBC launches (letsbonk and similar) | 150 | -2.8 | 6% | -6.1 |
| stonkfun launches | 100 | -10.8 | 4% | -11.8 |

Meteora DBC's first-minute fill shows +£36.9 (33% winners), but 96% of DBC pools traded in five or fewer
minutes and the depth used for its curve is assumed, so that fantasy row is the least trustworthy number here.

Most launches never trade again: 77% of pump.fun launches trade in five or fewer of their first 75
minutes. Buying new launches loses at every entry we could get. Even the fantasy first-minute fill
on pump.fun is only just positive (+£4.1, 16% winners) and negative with the best three removed.

The one lead is graduations. Bought one minute after a token moves to PumpSwap and sold at 20 to 30
minutes: +£19 to +£27 a trade, about 60% winners, still positive (+£3 to +£10) with the best three
removed. By the time a two-minute poller sees it, most of that is gone. One day, 150 pools,
in-sample: a lead for a forward paper test, not a result.

## Correction, 30 Sep 2026 evening: the graduation lead looks like an artefact

The graduation book (`grinder/graduates/`) started forward the same afternoon. After 98 counted
trades, entered 1 to 8 seconds after each migration at Jupiter prices that match GeckoTerminal's
candles, the primary exit is **-£32.8 a trade**, with 22% winners and 70% of trades at or below -50%
within 20 minutes.

The likely reason this study looked positive: the first PumpSwap minute candle often opens at a
pool-seeding price nobody trades at. One example: dnt9SMdP opened at 0.0000494, then traded at
0.000244 in the same minute. Entries at "the first traded minute" and, less so, "one minute later"
inherited that low price. The forward book has no such bias. It keeps running to its pre-registered
200-trade check, where -£10 or worse is a KILL.
