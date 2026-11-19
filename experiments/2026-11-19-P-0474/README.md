# P-0474: did the mayhem wallet's leftovers burn at 24 hours?

P-0473 read the fee-free mayhem wallet `BwWK17cb...de6s` when its 19 coins were 12.8 hours old: it
still held 16.99 billion tokens across them, about half of each coin's 2 billion supply. The videos
say what the agent has left is burned at 24 hours. Question: past 24 hours, are the holdings gone,
and did each supply fall by what the wallet held?

## Method

Keyless, public RPC, standard library, read only. Run 19 Nov 2026 at 12:32 UK, with the coins about
36.8 hours old.

- `burncheck.py` takes the 19 rows from `experiments/2026-11-18-P-0473/results.json` and asks again
  for each mint: `getTokenAccountsByOwner` with the mint filter, `getTokenSupply`, and the newest
  signature on the mint for the time of its last transaction. It writes its own `results.json` and
  does not touch P-0473's.

## Numbers

- **19 of 19 answered. 19 of 19 holdings are now exactly zero.** Sum held 16.986 billion then, 0.000 now.
- **Supply fell on all 19.** On the 18 coins where the wallet held anything real, the fall in supply
  divided by the 12.8-hour holding is 1.0000 on every one (lowest 1.0, highest 1.0). So the tokens
  were burned, not sold or moved: a sale would leave supply where it was.
- Median supply 2.000 billion then, **0.998 billion now**. Range now 0.911 to 1.817 billion, plus
  `9YWWW3dt...` at 1.9996 billion (the coin the wallet had already sold out of: 54 tokens held, and
  its supply fell by 339 thousand for other reasons).
- **When.** The newest signature on 18 of 19 mints is 12.44 to 12.47 hours before the run, so about
  00:04 to 00:06 UK on 19 Nov. The coins were born 23:42 to 23:47 UK on 17 Nov, so the burn landed
  about **24.3 hours after birth**, and nothing has touched those mints since. `9YWWW3dt...` had a
  transaction 4.84 hours ago.
- The token accounts are still open (1 account per mint, balance 0), so the rent was not reclaimed.
- Wallet SOL: 71,126.40 now against 71,345.73 a day earlier, **down 219.33 SOL**. On the first night
  it rose 22 SOL in twelve hours.

## What it says

The 24-hour burn is real and exact on this batch: every leftover token went, to the last decimal, in
one sweep about twenty minutes after the coins' first birthday in hours. A coin that the agent held
half of ends with about half its supply, so anyone left holding has their share of supply roughly
doubled, on a coin that stopped trading about 23 hours earlier.

## What I did not do

- I did not decode the burn transactions, so "burn" rests on supply falling by exactly the holding
  on 18 coins. That is hard to explain any other way, but I did not read the instruction.
- No prices, so the doubling of share is not a doubling of anything you could sell.
- The 219 SOL fall in the wallet is one reading against one reading. I do not know whether that is
  normal daily drift, a withdrawal or the cost of the agent's trading.
- One batch of 19 coins from one eleven-second window.

Shot (works, 0.80): at least 17 of 19 at zero, sum held under 0.2 billion, median supply near 1.0
billion. Measured 19 of 19, 0.000 billion, 0.998 billion. Called blind to today's read, after
re-reading P-0473's write-up.
