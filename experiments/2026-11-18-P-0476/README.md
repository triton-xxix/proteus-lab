# P-0476: who tops up the mayhem fee payer

P-0475 found the fee payer `Gygj9QQb...BUpA` spends about 195 SOL a day from 1,858 SOL, under ten
days of runway. Two questions: who refills it, and is the trading wallet `BwWK17cb...de6s` really in
its transactions (it was not in the static keys of the 60 read in P-0475)?

## Method

`topups.py`, keyless, public RPC, read only. 18 Nov 2026, 12:45 to 12:51 UTC.

1. Three pages of 1,000 signatures, to see how far back paging reaches.
2. `getTransaction` on 20 of the newest 1,000: static keys, `meta.loadedAddresses`, programs called.
3. The payer's balance 13 times, 25 seconds apart; any rise is an inbound transfer.

## Numbers

- **The link holds: the trading wallet is in 20 of 20**, never in the static keys, always loaded
  through one address lookup table, `Hyif6eWb...UcyP`.
- All 20 call one program, `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e`, plus two compute-budget
  instructions. The fee payer is the only signer (P-0475: one signature in 60 of 60). So the
  "wallet" does not sign its own trades: it is an account the mayhem program moves, and the fee
  payer is the key that drives it.
- **Top-ups: none seen.** 13 balance readings over 301 seconds, every step down, 0 rises; -170 SOL a
  day over the window (P-0475: -194).
- **Paging cannot find them.** 3,000 signatures reach back 207 seconds (14.5 a second now, against
  10.3 twenty minutes earlier). A day back is about 1,250 pages, and the top-up would still have to
  be picked out of about 1.25 million rows by fetching transactions one at a time.

## Verdict

Blocked on the question asked. The lookup-table check is answered; who funds the payer is not, and
cannot be from the public RPC in a probe. What would answer it: an indexed transaction API that
filters by transfer (keyed), or a balance sampler on the payer every five minutes for a few days,
which needs a long-running job started from an attended session. With under ten days of runway a
few days of sampling should catch one refill.

## What I did not do

- Read the lookup table's contents or the mayhem program's accounts for an authority or funder.
- Check whether the payer's first-ever funding transaction is reachable (it is not by paging).

Shot (blocked, 0.65): 0 top-ups seen, wallet in loaded addresses in at least 18 of 20. Measured 0
and 20 of 20; my page estimate of 890 for a day was low, it is about 1,250 at this hour's rate.
