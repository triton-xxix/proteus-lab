# P-0401: how stale is GeckoTerminal's single-pool endpoint?

Refill row 140, P-0390's open caveat: the new_pools page was frozen at first trade, but was the
single-pool endpoint cached too?

Method: `lag.py`. From a new_pools page read a minute earlier, the busiest pool under three hours old
(ELYSION / SOL, 1.4 minutes old, 332 one-hour transactions on the page). Then `/pools/ADDR` and
`/pools/ADDR/trades` read together at 0, 10, 30, 60 and 120 s. Keyless, 10 calls. `results.json`.

| read | single h1 tx | single price | trades list: newest trade age | oldest of 300 listed |
|---|---|---|---|---|
| 0 s | 663 | ...119596 | 2.9 s | 49.9 s |
| 10 s | 663 | same to 60 digits | 13.1 s | 60.1 s |
| 30 s | 663 | same | 33.0 s | 80.0 s |
| 60 s | 663 | same | 29.1 s | 97.1 s |
| 120 s | 924 | ...127967 | 5.2 s | 134.2 s |

What it says:

- The single endpoint served one frozen answer for at least 60 s and under 120 s, on a pool doing
  about six trades a second. Count, volume and price all identical across four reads. P-0390's worry
  was right: the single endpoint is cached as well, just for a shorter time than the page.
- The trades list is cached too. Its newest trade aged 2.9, 13.1, 33.0 s across the first three
  reads, which is the same response served three times; it had refreshed by 60 s.
- The page said 332 transactions; the single endpoint a minute later said 663.
- The list holds 300 trades and on this pool that is 47 seconds of trading, so the question as asked
  (single count against the list's count over an hour) cannot be answered from the list.

So on a pool in its first minutes, a keyless price from this API is between a few seconds and about
two minutes old and nothing in the response says which. For the Grinder that only matters if the age
gate ever comes down; today it keeps pools this young out.

Limits: one pool, one two-minute window, five reads. The cache length is bracketed (60 to 120 s), not
measured. A quieter pool may behave differently.
