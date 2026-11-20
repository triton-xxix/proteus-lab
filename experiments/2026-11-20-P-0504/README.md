# P-0504: how long did yesterday's mayhem coins live?

**Question.** P-0491 caught 20 mayhem coins at 12:39Z on 19 Nov, median 2.6 minutes old. A day on,
how long did each one trade, what share was dead inside 10 minutes, and did the 52-minute survivor
keep going?

**Method.** `lifetimes.py`: keyless public Solana RPC, `getSignaturesForAddress` on each mint, paged
back to the first signature (all 20 came back complete under one or two pages). Birth = first
signature, end = newest successful signature, lifetime = the gap. Run 12:33Z on 20 Nov. Numbers in
`results.json`.

**Called shot:** works at 0.80, median lifetime 20 minutes, 18 of 20 quiet for over 12 hours.

## Numbers

- **Median lifetime 9.75 minutes** (birth to last signature). Shot said 20: half that.
- **10 of 20 dead inside 10 minutes, 13 of 20 inside 15.** Lifetimes 3.1 to 13.4 minutes for those 13.
- **16 of 20 quiet for over 12 hours** (shot said 18). One quiet under an hour.
- Last-signature lifetime overstates the long ones. Four of the seven "long" coins end on one lone
  late call after a gap of 4 to 19 hours (`ACauv` 238 min gap, `GgTG` 766, `7km9` 1,140, `6MvtQ` two
  gaps near 40). Read as trading life, they all died at about 8 to 10 minutes. Counting that way,
  **17 of 20 were done inside 15 minutes.**
- Real survivors: `7JuG` traded to about 37 minutes then one call at 116; `Fszpx` had a burst of
  trades about 12 hours on (its last five calls are minutes apart at 731 minutes).
- **The 52-minute survivor (`HXgTg5...`, born 11:48Z) kept going**: 1,658 signatures (924 after the
  catch), last signature 24.3 hours after birth, 28 minutes before this run. Its gaps were long by
  the end (133, 407, 205 minutes). The last call lands at the 24.3-hour burn time in the source row,
  so it may be the burn, not a trade.
- Median 194 signatures a coin (P-0473: 111).

## Beside P-0473

P-0473 said the first batch was dead within about 35 minutes. That was an upper bound read from
last-traded hours. This batch, read from birth, says most coins are done in under 10 minutes, so the
35 was loose. Both batches carry one or two long tails out of about twenty.

## What I did not do

- Did not fetch transactions, so "lone late call" is read from timing, not from what the call was
  (could be a sell, a burn or a dust transfer).
- The 21st row in P-0491 is USDC (`EPjFWdd5...`), a balance the wallet holds, not a mayhem coin; it
  hit the page cap and is left out.
- One batch of 20 from one lunchtime. No claim about night or weekend cohorts.
