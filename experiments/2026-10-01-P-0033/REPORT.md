# P-0033: scoring the pump.fun poller v2 (P-0032)

Scored 1 Oct 2026 from the job's own files. Script `score.py`, numbers `result.json`. The job ran
28 Sep 22:54 to 29 Sep 22:52 UTC (23.97 h), stopped itself and wrote DONE. Nothing outside its folder.

## The count: works

- 566 polls, median gap 157 s (asked for 120; six pages with four-second gaps and retries take time).
- **26,645 pump.fun launches a day.** P-0014 saw 7,326 and I estimated 14,000 from its gaps. The
  estimate was itself half the truth. Still a floor: the last page was all new on 28 of 566 polls
  (5 percent, against 45 percent for P-0014).
- 305 of 566 polls logged at least one error, almost all a page needing its retry. The retry did
  its job; the count above is after it.
- Other launchpads in the same feed, per day: Meteora DBC 2,537, stonkfun 926, bags.fm 323,
  Raydium LaunchLab 171. Pump.fun is 72 percent of all new Solana pools.

## The graduation rate: broken by design

- 2,735 pumpswap pools, 10.3 per hundred launches, close to P-0014's one in ten. But a pumpswap pool
  is not proof of a graduation: anyone can open one.
- The poller never stored the base token address, so the matching fell back to names, and only
  8,717 of 26,608 launch names were unique. Matched graduates: 172, 0.65 percent. That is a
  floor set by the matching, not a rate. The v3 poller must keep the token address.

## Minute five: too thin to use

Only 3,231 launches got a five-minute snapshot (the six pages cover about five minutes of
launches, so most rolled off first), and only 16 of those were matched graduates. Medians,
graduates v the rest: 5-minute volume $10,109 v $126, buyers 6 v 2, FDV $11,170 v $3,376. The
direction is what anyone would guess and n = 16 proves nothing.

## Verdict

Works for the count, and the count is the number nobody had. The graduation question needs v3:
token address stored, and the five-minute snapshot taken from a per-token lookup rather than
hoping the pool is still on page six.
