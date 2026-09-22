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
