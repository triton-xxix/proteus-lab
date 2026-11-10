# P-0390: GeckoTerminal page v single endpoint at a two-second gap

**Question.** P-0384 found the single-pool endpoint reading one-hour volume above the new_pools page
(median 3.76 times) but its gaps were 23 to 154 s, too long to tell cache from real trading. At a
two-second gap, does the difference survive? If it does, the page is stale, not the market moving.

**Shot.** works at 0.75: single above page on 6 of 9 reads, median ratio about 2.

**Method.** `gap.py`: three rounds, each reads page 1 of Solana new_pools, takes the first 3 pools with
volume, then reads each pool's `/pools/ADDRESS` with a 2 s sleep between. Gap is measured from the page
read, so the second and third pick of each round sit further out. Keyless, 12 calls plus 4 rate-limit
waits of 15 s.

**Numbers** (results.json). 9 reads: single above page on 5, equal on 4, below on 0. Median ratio 1.56,
max 116.8. Gaps 2.1 to 36.8 s, median 17.2, longer than planned because of the 429 waits.

The clean read is TOAD: at a 2.5 s gap the page said 1 trade and $8.25 in the hour, the single endpoint
17 trades and $175. Round 1, about 25 s later, the page returned exactly the same 1 trade and $8.25 for
all three pools, and TOAD again 17 v 175 at 2.1 s. Sixteen trades do not happen in two seconds and then
stop; the page row was frozen at the pool's first trade. Suits (1 v 71 trades) and TITTIES (1 v 112)
show the same one-trade page row at 17 and 35 s.

**Answer.** It is cache on the new_pools page, not first-minute trading. Equal reads were pools whose
activity had already stopped (SPSC one trade, UODF nine).

**Caveats.** n 9 reads on 7 pools, one afternoon. The single endpoint may be cached too (TOAD identical
across rounds), so "single is current" is not shown, only "page is staler".

**Not done.** No change to the Grinder; the age gate keeps pools this young out of it (P-0384).
