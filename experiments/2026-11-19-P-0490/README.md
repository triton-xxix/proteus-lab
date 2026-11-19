# P-0490: how much of the trading on a mayhem coin is the agent itself?

P-0473 found each of 19 mayhem coins had 10 to 780 signatures and went quiet in about 35 minutes.
Question: on the three busiest, what share of the coin's transactions touch the mayhem wallet's own
token account, and does the agent get there before or after anyone else?

## Method

Keyless, public RPC, standard library, read only. Run 19 Nov 2026 at 12:37 UK.

- `share.py` takes the three mints with the most signatures in P-0473's results, re-reads the
  wallet's token account for each (the accounts are still open after the burn, P-0474), and pages
  `getSignaturesForAddress` on the mint and on that token account until each list ends.
- Agent share = signatures on the mint that are also on the agent's token account, over all
  signatures on the mint. Nothing is decoded.

## Numbers

| coin | signatures | agent's | share | failed | share of the ones that landed |
|---|---|---|---|---|---|
| `9YWWW3dt...` | 782 | 385 | 49.2% | 229 | 53.4% |
| `Bq5R3YNq...` | 465 | 321 | 69.0% | 26 | 73.1% |
| `24bA7eZ4...` | 395 | 229 | 58.0% | 34 | 63.2% |

- **Median agent share 58.0%** (49 to 69). Of the transactions that did not fail, 63.2%.
- Every signature on the agent's token account is also on the mint (0 strays on all three), so the
  two lists are measuring the same thing and both are complete.
- **The agent is there from the first slot on all three.** Its account's first signature is in the
  coin's birth slot, 0 seconds after birth. On two coins the first signature that does not touch the
  agent's account comes 4 seconds later (18 and 21 slots). On the third both kinds share the birth
  slot, so the order inside the slot is not known from this.
- All but one to three signatures per coin fall in the first hour; the late ones are the 24.3-hour
  burn (P-0474), and on `9YWWW3dt...` one more at 31.9 hours.
- `9YWWW3dt...`, the coin the agent sold out of, is the one with 229 failed transactions (29%)
  against 6% and 9% on the other two.

## What it says

On its busiest coins the agent is somewhere between half and two thirds of everything that happens.
So the "volume" a buyer sees on a mayhem coin in its first half hour is mostly the agent trading,
and the outside interest is the other 30 to 50 percent: on these three, 144 to 397 signatures in
all, some of which failed.

## What I did not do

- No decoding, so a signature is a transaction, not a trade, and I do not know buys from sells or
  size. An outsider's transaction that happens to carry the agent's account would count as the
  agent's; I do not think the program does that but did not check.
- Share by count, not by SOL.
- Who the failed transactions on `9YWWW3dt...` belong to beyond the agent's share is not split out.
- Three coins, the busiest three, from one night. The quiet coins (10 signatures) may be nearly all
  agent or nearly none.

Shot (works, 0.75): agent in about 55% of the mint's signatures, first touched at birth or within 5
seconds. Measured 58.0% and the birth slot on 3 of 3.
