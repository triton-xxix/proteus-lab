# P-0005: pump.fun graduation rate, keyless

GeckoTerminal page 5 failed: HTTP Error 429: Too Many Requests
## Numerator: new pools on GeckoTerminal

80 pools over 4 pages, spanning 0.06 hours (08:25 to 08:29). By dex: pump-fun 46, meteora-damm-v2 12, pumpswap 10, meteora-dbc 4, bags-fm 4, raydium-launchlab 3, orca 1.
pumpswap pools per hour: **176.5**

## Denominator: creations on the pump.fun program, public RPC

Last 1000 signatures span 0.4 minutes: **163636 transactions per hour** on the program.
Sample of 22 transactions fetched (8 failed): 0 carry `Instruction: Create`, fraction 0.000.
Estimated creations per hour: **0** (wide error bars: 0 of 22).

## Graduation rate

Not computable: a zero in the chain above.
Both rates are measured over windows of under an hour at different times of day; this is one reading, not the answer.


## What this says

- pump.fun's API is geo-blocked from this machine, rechecked: 403 with a redirect to static.pump.fun/blocked on both the v3 and the older frontend host. pumpportal has no keyless coins feed (404).
- The find: GeckoTerminal's `new_pools` feed lists pump.fun bonding-curve tokens as pools on a dex called `pump-fun`, beside `pumpswap` where the graduates go. Both sides of the ratio come keyless from one feed. In the 3.6 minutes the four pages covered: 46 pump-fun launches, 10 pumpswap pools, so a naive reading of **about 22 percent** graduating. That is far above the 1 to 2 percent usually quoted, and the likely reason is that GeckoTerminal only lists a bonding-curve pool once it has trades, so the denominator misses the launches that die at zero. Treat 22 percent as an upper bound on "launches anyone traded".
- The RPC route does not work at this scale: 1,000 signatures cover 24 seconds (about 160k transactions an hour on the program), and a 22-transaction sample found no `Create` instruction, which only says the create fraction is under about 5 percent. Counting creations properly means fetching thousands of transactions, and the public endpoint 429s well before that.
- Rate limit: GeckoTerminal answered 429 on the fifth page inside ten seconds. A day's reading needs a poller that takes two pages every five minutes, about 600 calls, inside its 30-a-minute limit. That is a small daemon, not a probe, and it is queued with that need declared.
