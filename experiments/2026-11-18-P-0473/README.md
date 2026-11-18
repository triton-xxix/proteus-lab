# P-0473: the mayhem wallet's inventory, coin by coin

P-0471 could not list what the fee-free mayhem wallet `BwWK17cb...de6s` holds: the Token-2022
listing came back HTTP 413. Question here: asked one coin at a time, how much of each coin's supply
does the wallet still hold, how many holdings are above the 1 billion it was handed, and how old are
the coins? The 19 coins are the ones seen trading in `experiments/2026-11-17-P-0470/results.json`
(17 Nov, about 23:47 UK).

## Method

Keyless, public RPC, standard library, read only. Run 18 Nov 2026 at 12:33 UK.

- `inventory.py`: `getTokenAccountsByOwner` with a `mint` filter and `getTokenSupply` for each of the
  19 mints, plus pump.fun's coin endpoint for a creation time.
- `activity.py`: pump.fun answered 403 on all 19, so age came from `getSignaturesForAddress` on each
  mint instead (newest 1,000). Every coin returned fewer than 1,000, so the oldest signature is the
  coin's first.

## Numbers

- **19 of 19 mint-filter calls answered.** The 413 is only on the unfiltered listing.
- The wallet holds something in all 19. **Median holding 1,002.3 million, 50.1% of supply.** 11 of 19
  are above 1 billion (it bought more than it sold), 8 below.
- Three coins are well off the pile: `CQjgnY96...` 663.6 million (33%), `24bA7eZ4...` 178.4 million
  (9%), and `9YWWW3dt...` 54 tokens (sold the lot). The other 16 sit between 953 and 1,089 million.
- Supply is 2.000 billion on 14 coins and a shade under on 5 (lowest 1.995 billion), so a little has
  been burned on those.
- Sum across the 19: 16.99 billion tokens. Wallet SOL: 71,345.73 (71,323.68 at 00:12, so +22 SOL in
  twelve hours and twenty minutes).
- **All 19 coins were created inside five minutes of each other**, 12.78 to 12.86 hours before the
  run (about 23:42 to 23:47 UK on 17 Nov). P-0470's sample caught them in their first minutes.
- **None has traded in the last hour.** 18 of 19 last traded 12.2 to 12.8 hours ago, so each was
  dead within about 35 minutes of birth; `G8pxXFcK...` went on to about 90 minutes and `9YWWW3dt...`
  (the one the wallet sold out of) to about six hours. Signatures per coin: 10 to 780, median 111.

## What it says

Thirteen hours on, the agent is still sitting on almost exactly what it was handed in 16 of 19
coins. It did not sell its free billion into buyers, and on 11 coins it ended a net buyer. The coins
themselves lasted about half an hour. So the 15 trades a second seen in P-0470 are spread over a
stream of new coins that each go quiet fast, not a standing book of 19.

## What I did not do

- No prices, so no value on the 16.99 billion tokens (on dead coins it is close to nothing) and no
  profit and loss.
- The coins are 12.8 hours old. Whether the wallet's leftovers are burned at 24 hours, as the videos
  say, cannot be seen yet. Queued as a re-read after the 24-hour mark.
- Signature counts on a mint are my proxy for trades on it; I did not decode them.
- 19 coins from one 11-second window on one night.

Shot (works, 0.75): all 19 answer, at least 15 non-zero, median about 1.0 billion. Measured 19, 19
(18 if 54 tokens is dust), 1,002.3 million. Called after seeing one of the 19 in the refill step.
