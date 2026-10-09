# Pre-listing week: rules and pass marks (v1, 9 Oct 2026)

Committed before the tracker starts. Paper only: no account, no wallet, no money. The research
behind every choice is `RESEARCH.md`. Scored by `week.py` the night after the poller stops (DUE D-011).

## What runs

`poller.py`, a launchd job loaded from this folder (`com.proteus.prelisting.plist`), every 60 s from
9 Oct 2026 until **17 Oct 2026 00:05 UTC**, then it stops itself. It also stops on `HALT` or a
`DONE` file. It writes only under `track/`, plus one git commit a day of that day's list.

Every poll reads the Upbit trade notices, the Binance new-listing catalogue and Bithumb's latest
notices; every five minutes it reads Coinbase's public `/currencies` and `/products`. A new notice
is logged with the time it was first seen.

## The scoring rule

`score.py` with the probabilities frozen in `scorer.json` (fitted on signals from 9 Oct 2025 to
24 Sep 2026; shrunk toward each venue's base rate with weight 20).

- **Universe:** coins with a USDT market on Binance (spot or USD-M perp), OKX (spot or swap) or Bybit
  (spot or perp), crypto only. Tokenized stocks, ETFs, commodities and forex are out (OKX
  instCategory not 1, Bybit symbolType stock, ETF, commodity or forex, Binance underlyingType not
  COIN, Binance Alpha stock or RWA tokens, Binance bStocks). Stablecoins out.
- **Targets:** Upbit KRW, Binance spot, Coinbase. A coin already on a target cannot score for it.
- **Signals**, each active for 14 days after it became public: new Binance USD-M perp, Binance
  Alpha listing, new OKX spot or swap market, new Bybit spot market or perp, new Gate market, Bithumb
  KRW listing, Coinbase trading start or new Coinbase currency, Upbit BTC/USDT-only listing, Upbit
  KRW listing (for the other two targets), Binance spot announcement (for the other two). Volume
  signals are not used (lift under 2).
- **Score** = 1 - product of (1 - p) over the coin's active signals and its open targets.
- **The list:** every day at the first poll after 00:00 UTC (and once at load on 9 Oct), the top 25
  by score (fewer if fewer score above zero), with a price snapshot of the whole universe, is
  written to `track/lists/YYYY-MM-DD.json` and committed. A list can only claim an announcement made
  after its commit time.

## The paper trade

- **The book:** the top 10 of each day's list, equal weight, valued from one list's price snapshot
  to the next. Entering or leaving the book costs 0.25% a side.
- **Selling into the pop:** when a book coin gets an Upbit KRW listing, a Binance spot listing or a
  new Coinbase currency or product, it is sold at the **low of the 1-minute bar containing the
  announcement + 3 minutes**, on Binance, else OKX, else Bybit, less 0.5% round trip, and leaves the
  book. The hold price for the pop is the close of the last full minute before the announcement.
- **Every listing is priced**, on the list or not: each Upbit KRW, Binance spot, Coinbase and
  Bithumb KRW listing of a coin with a prior USDT market, the same way, six minutes after it.

## Pass marks for the week

The week cannot settle the money question. At last year's rate the top 10 holds about one coin a
fortnight at the moment it is announced, and the backtest needs about 30 such hits before its
result means anything. So the week is judged on plumbing and on whether the pop is still there.

| | Mark | Pass |
|---|---|---|
| P1 | Polls that completed without a feed error, and the job ran to its end time | at least 95% and DONE written |
| P2 | Median lag from an Upbit or Binance listing notice's publish time to the poller seeing it | 90 s or less (no verdict if none) |
| P3 | Lists committed: 9 to 16 Oct, each after the first committed within 30 minutes of 00:00 UTC | 8 lists, none late |
| P4 | Median +3 minute pessimistic result on the week's Upbit KRW listings with a prior market | above zero (no verdict under 2 listings) |

Recorded, not judged: listings the list held at announcement (with rank and result), the number of
target listings in the week, the book's return against the universe held equal weight and against
200 random 10-coin books from the same day's scored pool.

## After the week

If P1 and P3 pass and P2 is not a fail, the tracker earns a 12-week paper run (new end date, same
rule, committed as RULES v2 before it starts). Its pass marks are fixed now, so the week's numbers
cannot move them:

- **KEEP** the idea for an executor proposal only if, after 12 weeks, the book made money after
  costs, beat the universe held equal weight, beat at least 95% of the random books, and held at
  least 10 coins at the moment of their announcement.
- **KILL** if the book is below zero after 12 weeks, or below -25% at any Sunday check.

If P1 or P3 fails, the 12 weeks wait until the plumbing is fixed and a second week passes.
