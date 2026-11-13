# P-0440: pump.fun creates per minute on a public RPC, and the dev's stake

Harvest H-0640 (a pump.fun sniper repo). I did not run the sniper; I ran its listening half,
read-only: `listen.py`, the P-0042 filter (logsSubscribe on the pump.fun mint authority, logs with
"Instruction: Create"), on `api.mainnet-beta.solana.com`, keyless, 13 Nov 2026 about 23:42 UTC.

Results (`results.json`):
- 5.0 minutes, 158 log messages, 148 creates: 29.6 a minute, about one every two seconds.
- 20 creates sampled evenly across the window, getTransaction at one every 2 s (the public limit
  P-0042 found). All 20 resolved a mint. 19 distinct creators.
- Creator's own holding at the end of the creation transaction, as a share of 1 billion: median
  0.43%, largest 6.63%. Buckets: 0 on 1, under 1% on 14, 1 to 5% on 3, 5 to 10% on 2, none at 10%
  or more.

What this does not see: a dev's same-slot bundle from other wallets (P-0180 found 9 of 20 creates
had one), and anything bought after the creation transaction. So "large dev stake" by the creator's
own wallet is rare here (2 of 20 over 5%); the dev's true stake is a floor at these numbers.

Verdict: works. A public RPC carries the whole create stream (about 30 a minute) to a keyless
listener; the bottleneck for a sniper is the 2 s getTransaction pace, which reads about one create
in fifteen. 19 of 20 creators bought in their own create (95%), against 83% on 30 Sep (P-0042).
One five-minute window, late on a Friday UTC.
