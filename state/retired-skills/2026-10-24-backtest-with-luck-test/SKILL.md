---
name: backtest-with-luck-test
description: Rebuild a trading rule someone claims works (a video, a paper, a forum post), check whether their numbers replicate, then test it against luck with a permutation test and a random-entry control. Use for any "does this strategy really work" probe on daily bars, and before any rule joins a Proteus paper book.
---

# Backtest with a luck test

The method of P-0082 to P-0091 (7 Oct 2026), which replicated Quantified Strategies five for five and
built the systems book. Templates: `experiments/2026-10-07-P-0082/` (fetch, replicate, permutation),
`experiments/2026-10-07-P-0089/p0089.py` (random-entry control, walk-forward with selection re-run).

## Order of work

1. **Write the rules down before any run**, in the README: entry, exit, filter, universe, dates,
   fills (next open), costs. If the source withholds a rule, say so and recover it only by stating
   the guess before testing it. A parameter chosen from a sweep must be swept again inside every
   shuffle, or the luck test flatters it.
2. **Data:** `experiments/2026-10-07-P-0082/fetch_prices.py SYM ...` (Yahoo chart endpoint, keyless,
   writes `sandbox/p0082/data/<SYM>.csv`). Stooq is behind a bot check; do not use it. Say whether
   OHLC are total-return scaled or price only; sources usually use price only.
3. **Replicate first.** Their numbers beside mine in one table: trades, profit factor, average trade,
   drawdown, growth. Within a few percent and one or two trades is a replication. If it does not
   replicate, that is the finding; stop there.
4. **Luck test:** the neurotrader888 Monte Carlo permutation (gaps and intrabar moves shuffled
   separately, series rebuilt), as in `p0082.py`. 1,000 shuffles for fixed rules, 500 if a parameter
   was searched. p is the share of shuffles at least as good.
5. **Random-entry control** (P-0089): same filter, same exit, same trade count, random entry days,
   10,000 draws. If random entries earn about the same, the exit is the edge, not the signal (P-0086).
6. **Out of sample:** since 2009 separately; across the nine-ETF basket, not just SPY; walk-forward
   with any selection re-run inside each shuffle.
7. **Against holding:** always show buy-and-hold and 60/40 beside it. Beating luck and losing to
   holding is a common, honest result (P-0084, P-0090).

## Verdict lines

- works: replicates and passes the luck test on more than the market it was found on.
- not-worth-it: replicates but fails luck, or passes luck and loses badly to holding with no hedge use.
- A rule that earns a book goes through `preregister-a-book` before its first live trade.

Numbers in notes: trades, mean per trade, p, and the holding comparison. Never quote a Sharpe without
re-running it (D-004: P-0084 recorded 0.28, the same script later gave 0.35).
