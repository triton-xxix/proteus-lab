# The Grinder: paper rules

v0.1 was written before the first position (22 Sep) and governs G-0001 to G-0006. v0.2 is at the
bottom, written 2026-09-25 before any v0.2 row and before the path rescoring code was run. It
governs every position opened from then on. v0.1 is kept below exactly as it was.

# v0.1

Hypothesis under test: pump.fun is a meat grinder for the people using it. This desk finds out with
its own data instead of repeating the verdict.

## Data (all keyless, all proven 2026-09-22)

- DexScreener public API: token profiles and boosts (discovery), search, token-pairs (price,
  liquidity, volume, transactions, pair age, socials).
- rugcheck.xyz public API: risk report (normalised score, named risks, LP locked percent, holder
  count, top holders).
- Public Solana RPC: mint authority, freeze authority, supply, largest accounts (top-10 share).
- pump.fun's own API is geo-blocked from this machine. Not used. Pump tokens are still covered:
  they trade on pumpswap and carry the `pump` mint suffix.

## Cadence and what that means for scoring

One snapshot a night. Positions are therefore scored at 24h (next snapshot) and 7d. A 1h score
needs an hourly run and is deferred; the rules do not claim it.

## Scanner, every nightly run

Up to 120 candidate Solana tokens from the discovery endpoints. For each: best pair by liquidity,
age, price, liquidity, market cap, 1h and 24h volume, 1h buys and sells, 1h and 24h price change,
mint and freeze authority, top-10 holder share, holder count, LP locked percent, rugcheck score and
named risks, social link count. One row per token per night in `SNAPSHOTS.csv` (committed) and the
full pair payload in `cache/` (not committed).

## Paper entry rules (v0.1)

Bankroll £100. Position £5 flat. Maximum 4 open. Enter at the snapshot price when ALL of:
age between 1h and 48h; mint authority revoked; freeze authority revoked; liquidity at least
$20k; 24h volume at least $200k; 1h volume at least $10k; top-10 holders at most 30 percent;
at least 300 holders where the count is known (a missing count is not held against the token, and
this is noted as a weakness); LP at least 90 percent locked or burned where known. Candidates are
ranked by 1h volume and the top ones fill the free slots.

Not yet checked (v0.2 candidates): bundled first-block buys, sniper count, dev wallet history.

## Paper exit rules (v0.1)

Take profit at +100 percent. Stop at -50 percent. Time stop at 24h from entry. Rug: price down
90 percent from entry, or liquidity below 10 percent of entry liquidity, closes at the current price
and is logged as a rug. Exits are checked once a night, so a stop is honoured late, which is
realistic for a desk that does not watch the screen.

## Fees and conversion

1 percent each way plus $1.50 flat per side. GBP/USD fixed at 1.30 for the paper book. Both are
optimistic for meme coins and stated as such.

## Scoring

Hit rate, expectancy per position in GBP, count of positions that rugged, and score_24h and
score_7d as percentage change from entry regardless of exit. `bin/score.py` reads the ledger.

## Pre-registration

`LEDGER.csv` rows are committed at entry. Outcome columns are filled by later commits. The commit
history is the proof.

## Note, 2026-09-24: the gate stays, the feed and the ruler change

Written before any position exists. Two nights, 323 snapshot rows, zero entries. The question was
whether to find a feed that surfaces pools above the gate, scale the gate to pool age, or run both
as two paper books. I looked at the rows before deciding.

What the data said. The v0.2 discovery order put GeckoTerminal's new_pools first and the 120 limit
cut everything after them. On the 23 Sep run all 58 rows came from that feed: median age 12 hours,
median liquidity $2,349, median 24h volume $56. Nothing in that population can clear a $20k
liquidity or $200k volume gate, so the gate was never tested; the feed was. On the 22 Sep 01:27 run,
which still had DexScreener's boosts and profiles in front, 11 of 20 in-window rows cleared the
volume gate and 9 cleared liquidity. And on 24 Sep, GeckoTerminal's trending pools over 1h, 6h and
24h held 14 distinct pools between 1 and 48 hours old with liquidity above $20k and 24h volume above
$200k. Pools that can pass exist and are reachable keyless; the scanner was not looking at them.

Second fault, in the ruler not the gate: top-10 share was unknown on 230 of 323 rows, and the
`top10` gate needs a value, so those rows failed on nothing measured. Cause: the public Solana RPC
answers `getTokenLargestAccounts` with 429 on the first call. rugcheck's full report has the top
holders and is now the source. Its list includes the pool's own token account, which is not a
holder, so market-owned accounts are excluded before summing.

Decision. Rules v0.1 are unchanged: same gates, same numbers. A gate that never fires is not a
broken gate, and scaling it to age until a trade appears would be fitting the rules to the outcome.
The change is plumbing: trending and volume-ranked feeds first, new_pools watchlist last, top-10
share measured from a source that answers. No second paper book yet; one clean test of v0.1 first.

If, after a week on the fixed feed, the safety gates (top-10 share, holders, LP locked) still
reject every pool that clears liquidity and volume, that is the finding and it gets published as
one: nothing reachable through free discovery clears a sensible safety bar. Only then is it worth
asking whether the bar is sensible.

# v0.2 (2026-09-25): exits on the price path, a real stake, a measured cost model

Kind of change: a rule change (exit, sizing, fee model). The Grinder's clock resets. v0.1's rows
stay in the ledger under `rule_version` v0.1, close under v0.1's nightly rules, and are published
as their own book. Why: G-0001 passed through its -50% stop 34 minutes after entry (08:10 UTC,
24 Sep, on GeckoTerminal's minute candles) and was sold 14 hours later at -86% by a check that
runs once a night. A token can go 10x and back between two checks and the ledger would show
neither. That is a diary, not a desk.

**Unchanged from v0.1:** every entry gate and its number, the ranking by 1h volume, the maximum of
four open positions, take-profit +100%, stop -50%, time stop 24h, rug at -90%.

**Stake and bankroll.** £100 per position, the size a real trade would be (Luke, 25 Sep: £100 to
£150). Paper bankroll £1,000, so four open positions commit 40% of it. GBP/USD fixed at 1.30.

**The record is the candle path.** For each position, GeckoTerminal's keyless minute candles
(`/pools/{pool}/ohlcv/minute`, USD, base token) for the pool the scan entered on, from the first
full minute after entry to entry plus 24 hours. Measured 25 Sep: one call returns up to 1,000
candles, paging with `before_timestamp` reaches the pool's first trade, and minutes with no trades
are absent rather than zero. The candles used are committed under `grinder/candles/` when a
position closes, so the record does not move if the source revises them. Every run records, for
every position of either version, in `grinder/PATHS.csv`: highest high and lowest low in the
holding window and the time of each, the path-aware exit, what the rule captured, and the gap.

**Fill rule.** Walk the candles in order. The first candle whose low reaches the stop, or whose
high reaches the take-profit, triggers the exit. If both are reached inside the same candle, the
stop is taken (the order inside a minute is unknown, so the worse case). If the candle opened
beyond the level (a gap), the fill is the open, not the level. A fill at or below -90% from entry
is logged as a rug. **Tightened 2026-09-25, an hour after the above was committed and after seeing
the case that broke it:** if the trigger candle's low also reaches the rug level (-90%), the fill is
that candle's close (or the gap fill, if lower) and the exit is a rug. G-0005 opened its stop minute
at -27% and closed it at -98% on $11k of volume; a fill at the -50% level inside a one-minute rug is
not a price anyone got. Tightening only, before any v0.2 row. With no trigger by entry plus 24 hours, the time stop fills at the close of the
last candle before that time. The entry minute itself is not used, so no price that printed before
the entry can trigger an exit.

**Cost model, applied to every entry and exit.**

- Pool fee 1% per side (unchanged from v0.1, conservative for most Solana pools).
- Network and priority fee $0.05 per side (replaces v0.1's invented $1.50).
- Price impact from the pool's own depth, constant product: buying $x against a quote side of Q
  pays a price (1 + x/Q) times the mid; selling a value v receives v / (1 + v/Q). Q at entry is half
  the entry liquidity. Q at exit is Q at entry times the square root of exit price over entry price,
  which is what a constant-product pool's quote side does when price moves and nobody adds or pulls
  liquidity, capped by half of any lower liquidity a later snapshot observed before the exit.
- Execution slippage on the exit fill: 3% adverse on stops and rugs (a market sell into a falling
  book), 1% on take-profits and time stops.
- At the $20k liquidity gate a £100 position pays about 5 to 8% round trip in total.

**Fallback.** If the pool returns no candles (delisted, 404), the position closes at the next run
under v0.1's nightly logic at the DexScreener price, and the exit reason carries `_nightly` so it
is counted and visible.

**What the candle record cannot see:** a liquidity pull that happens without trades, and the
order of prints inside a minute. Both are why the fill rule is pessimistic.

**If a poller is ever added** (hourly or faster), it is a cross-check. Where it disagrees with the
committed candles on a fill, the candles are the record and the disagreement is logged.
