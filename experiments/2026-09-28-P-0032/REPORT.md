# P-0032: pump.fun poller v2, started 28 Sep 2026

A long-running job under the charter's Probes paragraph. Started tonight; scored by P-0033 on the
night after it stops (queued `--after 2026-09-30`).

## What runs

`sandbox/p0032_poller.py poll`, from launchd every 120 s, label `com.proteus.p0032`, plist in this
folder and loaded from here. Each poll pulls GeckoTerminal `new_pools` for Solana, six pages of
twenty rows, four seconds apart, one retry eight seconds later on a 429. Every pool not seen
before goes to `pools.jsonl` (id, dex, name, created, seen). For pump-fun launches and pumpswap
pools it also writes a trimmed attribute snapshot to `snapshots.jsonl` at first sight (`first`)
and again at the first poll where the pool is at least five minutes old (`5min`): price, FDV,
reserve, 5-minute and 1-hour volume, buys, sells, buyers, sellers, price change. Stops itself 24
hours after the first poll (START written 22:54 UTC on 28 Sep), or on HALT, and unloads its own
job. Writes nothing outside this folder.

## Why six pages, not ten

The first hand-run poll asked for ten pages 1.2 s apart and pages 6 to 10 came back 429. Five
pages, 100 rows, reached a pool ten minutes old, so at two-minute intervals 100 rows is five
times the cover needed. Six pages with a four-second gap and a retry is the compromise; the
`last_page_all_new` flag in `polls.jsonl` says on every poll whether the feed rolled over anyway.

## What it is for

P-0014 (two pages every five minutes) missed about half the launches. This run should give a true
daily launch count, a graduation rate that does not need the name-matching fudge, and the
backlog question: what did the graduates look like at minute five compared with the ones that
died.

## Files

`polls.jsonl`, `pools.jsonl`, `snapshots.jsonl`, `START`, `DONE` (when finished),
`com.proteus.p0032.plist`, `stderr.log`. Loader: `p0032_poller.py load`; state check:
`p0032_poller.py summary`.
