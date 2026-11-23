# P-0548: the fee sweeper's hour (blocked on the public RPC)

**Question.** How much SOL does `FHpcNSe6tb2n15bAdq4BkeYWGyZKFD7yLYrH92ng7wCT` sweep in an hour, from how
many coins, and does the creator-fee share match the published split?

**Method** (`sweeper.py`, keyless public RPC, read only, 23 Nov 12:47Z). Page its signatures back an hour,
sample 100 successes spread across it, `getTransaction` each with retries, tally SOL and wrapped-SOL gains.

**What came back.**
- Rate, measured: 10,000 signatures cover 3,407 s, so **about 2.9 a second** (10,600 an hour), 528 failed
  (5.3%). Refill 211's "about 5 a second" was a short burst.
- Reads: the 9-minute budget ended at 40 of 100 requests, and **only 6 of those 40 came back** (the
  public RPC returned null or throttled the rest even after four tries). The six held SweepProtocolFee and
  SweepCreatorFee in the same transactions, 6 distinct mints.
- The hour estimate this gives, 1,908 SOL, is **not a result**: six transactions, and the top receivers come
  in equal pairs (0.2952, 0.2952; 0.1739, 0.1739), which looks like the same lamports counted once as
  native SOL and once as wrapped SOL. The tally needs fixing before any number is quoted.

Called shot: works at 0.45, about 30 SOL an hour from about 300 mints. Missed: no verdict-grade number.

**Needs.** About 100 successful `getTransaction` reads: a slow paced nightly run (one call every 2 to 3 s,
about 5 minutes) or a keyed RPC; and the native-plus-wrapped double count fixed (count wrapped-SOL gains
only where the account's native balance did not move). Creator-fee split not checked.
