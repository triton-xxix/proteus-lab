# The Grinder: paper rules (v0, written before the first position)

Hypothesis under test: pump.fun is a meat grinder for the people using it. This desk finds out with
its own data instead of repeating the verdict.

## Data

- DexScreener public API (token profiles, pairs, boosts). No key.
- pump.fun public endpoints for launches and graduation state. No key.
- Public Solana RPC for mint and freeze authority, supply, top holders. No key; rate limited.
- Birdeye free tier if the above are too thin (key would go in 1Password tagged `proteus`).

## Scanner, every nightly run

For every Solana token first seen in the last 24 hours and in the top 200 by 1h volume:
mint authority (revoked or not), freeze authority, LP status (burned, locked, held), top-10 holder
share, number of holders, dev wallet's previous launches, bundled buys in the first block, sniper
count in the first minute, age at graduation if graduated, social links present, and price and
volume at 5m, 1h, 6h, 24h. Stored as one row per token per snapshot in `grinder/cache/`.

## Paper entry rules (v0)

Bankroll £100. Position size £5 flat. Maximum 4 open positions. Enter at the next snapshot price
when ALL of: mint authority revoked, freeze authority revoked, LP burned or locked, top-10 holders
under 30 percent, at least 300 holders, no bundled first block, dev wallet with no prior rug, age
between 1h and 6h, 1h volume above $50k.

## Paper exit rules (v0)

Take profit at +100 percent. Stop at -50 percent. Time stop at 24h. Rug detection (LP pulled,
price down 90 percent in one snapshot) closes at the snapshot price and is logged as a rug.

## Scoring

Every position scored at 1h, 24h and 7d from entry. Hit rate, expectancy per position, and the two
confusion numbers: flagged-as-rug that rugged, passed-as-clean that rugged. Fees and slippage are
modelled at 1 percent each way plus a flat 0.01 SOL, which is optimistic for meme coins and stated
as such.

## Pre-registration

`LEDGER.csv` rows are committed at entry with the entry snapshot. Outcome columns are filled by
later commits. The commit history is the proof.
