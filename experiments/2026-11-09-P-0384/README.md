# P-0384: GeckoTerminal's new_pools page against the single-pool endpoint (9 Nov 2026)

Twelve Solana pools from page 1 of `new_pools`, then each pool's own endpoint, three rounds a minute apart (`lag.py`, `direction.py`).

- 19 HTTP 429s and backoff, so the single reads came 23 to 154 s after the page, median 78 s, not the "seconds" the probe asked about.
- Rounds 1 and 2 are empty: every chosen pool had already left page 1 of new_pools within a minute. Only round 0's 12 pairs exist.
- Every pool was about a minute old at the read. Against the page, the single endpoint's one-hour volume was higher on 10 of 12 and equal on 2, never lower.
- Larger over smaller: median 3.76 times, 90th percentile about 30, max 83.8 times.

What this says: on pools a minute old, a page reading of one-hour volume is out of date as soon as it is read, because the number is a running total of a pool's first trades. Volume can only go up, so "stale cache" and "real trading in the gap" look the same here and I cannot split them. The answer to P-0372's question is therefore partial: the 20-times difference is about the size real first-minute growth can produce, and the two reads were too far apart to show a cache age.

Reserve moved both ways, and on one pool (DRILLING) it read 14,716 on the page and 0 on the single endpoint, which would be worth a check by any gate that trusts it.

Why it does not matter much for the Grinder's book: the age gate rejects pools this young anyway, so the gate never reads these first-minute numbers. To split cache from real, a future run needs a read gap of a second or two, which needs fewer pools or a slower cadence than the free tier gave tonight.
