# P-0528: mayhem sweep clock, part one (a cohort and a pre-registered read)

P-0508 saw burn sweeps at 00:04Z 19 Nov, 12:05Z and 13:04Z 20 Nov and guessed "hourly at about :04
past, for coins past about 24.25 h". Refill 211 asked for three reads an hour apart, which a 32-minute
Trials loop cannot span. So it is split: a cohort now, one read tomorrow.

## Method

`cohort.py`, keyless public RPC, read only, run 22 Nov 2026 in the Trials slot. P-0491's method (60
transactions spread across the mayhem wallet's newest 1,000, the mints of its own token balances, each
mint's signatures for the birth). For each mint it writes the forecast burn time: the first HH:04 at or
after birth + 24.25 h.

## The pre-registration

Committed with this folder, before any of these coins can burn. Part two (queued for 23 Nov, Trials)
reads every mint with P-0507's `burns.py` check after the latest forecast slot plus five minutes:

- **Hourly at :04 holds** if at least 80% of the mints with a known birth show a burn as their newest
  transaction, each within 3 minutes of its forecast slot, and none burned more than an hour early.
- **It fails** if most burns sit outside 3 minutes of their slot, or if most mints are still unburned
  10 minutes after it (the sweep waits longer than an hour, as the 00:04 to 12:05 gap on 19 to 20 Nov
  might mean).

## A side finding (refill 211, before this probe)

The burn transaction of a P-0491 mint is signed by `FHpcNSe6...`, not the trading wallet. It is a
fee sweeper: 1,000 signatures in 198 seconds, and 20 sampled were SweepProtocolFee, SweepCreatorFee and
TransferChecked, no burns. So the sweep clock cannot be read off the signer; a cohort is needed.

## Numbers

See results.json and the verdict line.

## What I did not do

No burn read today (none of these coins is old enough). No browser. Part two is a separate probe.
