# P-0475: what the mayhem agent's fee payer spends

P-0470 found one account, `Gygj9QQby4j2jryqyqBHvLP7ctv2SaANgh4sCb69BUpA`, pays the network fee on
every mayhem-agent transaction. Question: what does that cost a day, and how long does its balance
last?

## Method

`feepayer.py`, keyless, public RPC, standard library, read only. 18 Nov 2026, 12:36 to 12:44 UK.

1. Rate: `getSignaturesForAddress`, newest 1,000, block-time span.
2. Fee: `getTransaction` on 60 of those, spread evenly through the list (0 refused): `meta.fee`,
   signature count, and the payer's own balance change in each.
3. Drift: `getBalance` at the start and 480 seconds later.

## Numbers

- **1,000 signatures in 97 seconds: 10.3 transactions a second**, about 890,000 a day. 15 failed.
  (P-0470 saw about 15 a second on the trading wallet at midnight.)
- **Fee per transaction: median 227,114 lamports (0.000227 SOL)**, mean 223,364, range 178,838 to
  242,550. One signature each, so the base fee is 5,000 lamports and the other 98% is priority fee.
  Median compute used 121,265 units.
- In all 60 the payer's balance fell by exactly the fee and nothing else. It pays fees; it does not
  trade.
- **By rate and fee: 199 SOL a day. By balance drift: 1.078 SOL gone in 480 seconds, 194 SOL a
  day.** Two readings, 2.5% apart.
- Balance 1,858.42 SOL at the end. **Runway 9.3 to 9.6 days** at this rate, so somebody tops it up.

Against P-0471 and P-0473: the trading wallet's SOL rose 20.6 in twenty minutes at midnight and 22
in the twelve hours after. The fee payer spends about 97 SOL in twelve hours. On these readings the
fee bill is several times what the trading wallet gained, before counting the tokens it was handed.

## Shot

Works at 0.70, expecting about 0.00002 SOL a transaction, 10 to 60 SOL a day, runway 30 to 180 days.
The verdict is right and every number is wrong: the fee is 11 times my guess (I assumed a small
priority fee; it pays about 45 times the base fee), so the daily cost is 3 to 20 times higher and
the runway is days, not months.

## What I did not do

- The trading wallet `BwWK17cb...` is not in the static account keys of any of the 60, and the
  payer is the only signer. I did not read the address-lookup-table accounts
  (`meta.loadedAddresses`), so I have not confirmed here that these 60 are the wallet's trades;
  P-0470 found the link from the wallet's side (150 of 150).
- Eight minutes at lunchtime. The rate at midnight was higher, so a day's bill could be more.
- Who funds the payer, and how often. Queued.
- No GBP figure: no SOL price pulled in this run.
