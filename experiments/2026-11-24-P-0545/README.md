# P-0545: mayhem sweep clock, part two (the pre-registered read)

## Question

P-0528 (22 Nov) took 22 mayhem mints, forecast each one's burn as the first HH:04 at or after birth +
24.25 h, and pre-registered a rule: hourly at :04 holds if at least 80% of the mints with a known birth
show a burn as their newest transaction, each within 3 minutes of its slot, none more than an hour early.

## Method

`sweep.py`, run 24 Nov 2026 12:33Z in the Trials slot (about 23.5 h after the last slot). Keyless public
Solana RPC, read only. P-0507's `is_burn` check imported unchanged. For each mint: the newest 20
signatures, then `getTransaction` on up to the newest 6 until one is a burn on that mint.

## Numbers

- 22 mints, 21 with a known birth. 21 of 21 burned.
- Strict rule (newest transaction is the burn, within 3 min): 18 of 21 = 86%. The other 3 burned on slot
  too, but saw later transactions (index 1, 2 and 5 in their signature list). **Rule passes either way.**
- Offset from the forecast HH:04:00: 0.00 to +1.35 min, median +0.88 min. None early at all.
- Two slots were in the cohort: 20 mints forecast 13:04Z 23 Nov, burned 13:04:00 to 13:05:21; one mint
  forecast 09:04Z, burned 09:04:55. So the clock is hourly, not only the 13:04 hour.
- Age at burn: 24.457 to 24.834 h, median 24.485 h. Consistent with an age cut of about 24.25 h then the
  next :04 sweep (youngest burned coin was 24.457 h, born 12:36:52, so the cut sits before 24.45 h).
- The undated mint (12VzE...) also burned at 13:04:55, the same sweep.

## Called shot

broken at p 0.55, "about 50% within 3 min". Measured 100% (86% strict). Miss.

## What I did not do

No read of the sweeper wallet, no attempt to pin the age cut tighter than the cohort allows, no trading.
The 00:04 to 12:05 gap seen 19 to 20 Nov stays unexplained (no coins old enough in those hours is the
simplest reading). No browser.
