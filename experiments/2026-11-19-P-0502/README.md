# P-0502: the mayhem burn is a rolling sweep, not a daily one

Refill row 199, narrowed. The row asked for the size of a whole sweep by paging the fee payer's
signatures back a day; at about ten transactions a second that is about 860,000 signatures, so I
asked the smaller question that decides the shape: when each coin was burned, how far past its
24th hour was it?

## Method

`sweep.py`, standard library, Solana public RPC, keyless. P-0496 decoded five burn transactions of
five coins each. For 12 of the 20 coins in the first three batches that P-0496 did not start from:
birth is the oldest signature on the mint (all 12 paged to the end, 5 to 487 signatures each), burn
time is the batch's block time.

## Numbers

- All 12 were burned between **110 and 3,087 seconds** past 24 hours, median 1,223. None was over an
  hour past. With P-0496's five (1,035 to 1,291) that is 17 coins, all inside 52 minutes.
- 9 of 12 were under 30 minutes past (called shot: 10 of 12).
- One batch held coins 110 s and 1,719 s past their 24 hours side by side, so a sweep collects
  everything that has come due since the last one.

A daily sweep would show ages spread from 24 to 48 hours. This shows 24 hours plus up to 52 minutes,
which fits a sweep roughly every 50 minutes to an hour. The period itself is a guess from 17 coins of
one sweep; two sweeps would pin it.

## Not done

The size of a sweep (how many batches, how many coins) and the exact period. Both need the burn
transactions found without paging the fee payer; the coins' own mint histories are the cheap way in,
which is what this used. Three batches of one night.
