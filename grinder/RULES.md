# The Grinder: paper rules (v0.1, written before the first position)

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
