# P-0014: pump.fun graduation rate over a full day

Started 27 Sep 2026 10:14 UTC, stopped itself 28 Sep 10:17 UTC. launchd job `com.proteus.p0014`,
plist loaded from this folder, every five minutes, GeckoTerminal `new_pools` pages 1 and 2 for
Solana, keyless. Scored 28 Sep 23:30 UTC by `sandbox/p0014_analyse.py`; numbers in `analysis.json`.

## Verdict: works

The long-running job pattern held for its first outing: 284 polls, gap 304 to 308 seconds, zero
fetch errors, stopped itself at 24 hours, nothing written outside this folder. No poll landed after
DONE was written, and `launchctl print` at 00:05 on 29 Sep finds no such service in the user
domain (`sandbox/p0014_launchd_check.py`), so the self-unload did what it said.

## Numbers

| | |
|---|---|
| Pools first seen in the window | 9,910 |
| of which pump.fun bonding-curve launches | 7,326 |
| of which pumpswap pools (graduations) | 757 |
| Raw graduations per launch | 10.3% |
| Launches seen per hour | 305 |
| Graduations per hour | 31.5, flat across the day (18 to 40) |
| Graduations matched by name to a launch seen in the window | 385 of 754 |
| Launch to graduation lag, matched pairs | median 11 minutes, p90 4.8 hours, p10 under a minute |
| Polls where all 40 rows were new | 129 of 284 |

## Reading the numbers honestly

- **The launch count is a floor.** Two pages is 40 rows and 129 polls came back with every row
  unseen, so the feed rolled over between polls almost half the time and launches in the gap were
  never listed. Only half of the graduations could be matched to a launch I saw, which says the
  same thing from the other side: about half the launches were missed. The fix is cheap: more
  pages per poll, or a two-minute interval.
- **The raw ratio is the better estimate.** Both launches and graduations are missed at roughly
  the same rate when the feed saturates, so the ratio of the two survives it; the matched figure
  (5.3%) is biased low by the miss rate and by name collisions (849 launch names were used more
  than once in the day). Call it one in ten, with the true number of launches nearer 14,000 a day
  than 7,300.
- **It is an upper bound on the rate over all launches.** GeckoTerminal lists a pool once it has
  traded; a launch nobody ever buys is never in the denominator. P-0005's 22 percent from a
  3.6-minute sample was the same bound taken over too short a window.
- **Graduation is fast or never.** Half of the matched graduations happened inside 11 minutes of
  launch and nine in ten inside five hours. A poller that wants the graduates at minute five (the
  backlog question) has to catch them inside the first poll, which the five-minute interval barely
  does.

## What it feeds

- The Grinder's age gate (1 to 48 hours) sits after the point where most graduations have already
  happened. Whether that matters for the paper book is a separate question; P-0013 is the one that
  splits outcomes.
- The backlog question "what did the graduates look like at minute five" is now answerable with a
  second poller that pulls each new pump-fun pool's attributes once, at first sight. Not queued
  tonight.

## Files

`polls.jsonl` one line per poll. `pools.jsonl` one line per pool first seen (id, dex, name,
created, seen). `analysis.json` the scoring output. `START`, `DONE`, `com.proteus.p0014.plist`,
`stderr.log` (empty). Poller: `sandbox/p0014_poller.py`. Scorer: `sandbox/p0014_analyse.py`.
