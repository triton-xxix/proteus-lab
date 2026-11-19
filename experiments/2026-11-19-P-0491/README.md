# P-0491: mayhem coins alive at lunchtime, and how fast they are born

P-0470 caught the mayhem wallet working 19 coins at 23:47 UK, and P-0473 showed those 19 were all
born inside five minutes. Question: at lunchtime, how many coins is the agent working at once, how
old are they, and what does that say about how many are born an hour?

## Method

Keyless, public RPC, standard library, read only. Run 19 Nov 2026 at 12:39 UK.

- `alive.py` pulls the wallet's newest 1,000 signatures, fetches 60 of them spread evenly across the
  1,000, and lists the mints of the wallet's own token balances in each.
- For each mint, `getSignaturesForAddress` (limit 1,000). Fewer than 1,000 back means the oldest is
  the birth. Ages are taken at the end of the run, about a minute after the wallet pull.

## Numbers

- **1,000 signatures span 72 seconds: 13.9 transactions a second** (15.4 at midnight on 17 Nov). 4 of
  1,000 failed. So the rate holds at lunchtime.
- 60 of 60 transactions fetched, none refused, and all 60 carry a wallet token balance.
- **20 mayhem coins in 60 transactions** (19 in 142 trades at midnight). A 21st mint in the list is
  USDC (`EPjFWdd5...`), in one transaction; it is not a coin being worked and is left out below.
- **Median age 2.6 minutes.** 17 of 20 were born in the last five minutes, 19 of 20 in the last ten.
  Youngest 1.5 minutes, oldest 52.5 minutes (`HXgTg5Ub...`, 300 signatures, still trading 7 seconds
  before the read).
- Every one of the 20 has fewer than 1,000 signatures (23 to 428), so all 20 births were seen.
- Birth rate: 17 coins born in five minutes is a floor of about **200 an hour** (only coins the agent
  was seen trading in a 60-transaction sample). Live count over median age gives about 465 an hour.
  Call it 200 to 470; about 5,000 to 11,000 a day if lunchtime is typical.

## What it says

The agent is always on about 20 coins and almost all of them are under five minutes old. Midnight
was not a burst: it is a conveyor. With P-0473 (dead inside 35 minutes) and P-0490 (the agent is
half to two thirds of the trading), most of what the agent does is trade newborn coins that nobody
else stays for.

## What I did not do

- The birth rate is two rough estimates from one 72-second window, not a count. A real count needs
  the creations themselves, from the program's own stream.
- 60 transactions of 1,000: a coin the agent touched fewer than about 17 times in the window can be
  missed, so 20 is a floor on the live set.
- Why USDC shows up in one transaction is not looked at.
- Two points in the day (23:47 and 12:39), two days apart.

Shot (works, 0.70): about 15 coins, median age about 6 minutes, oldest about 30. Measured 20, 2.6
and 52.5: the count is near, the coins are less than half as old as I said.
