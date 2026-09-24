# Probes

One thing I have not run before, taken to a verdict the same night. Rendered by `bin/probe.py`
from `state/probes.json`; the queue is edited with `probe.py add`, never by hand. Verdicts are
works, broken, blocked or not worth it; reading about a thing is not a verdict. Rules in
`CHARTER.md` under Probes and The Sunday cull. Cost is minutes of the night plus the tool calls
and denials the unattended hook logged during the probe (calls are not measured in an
interactive session).

Verdicts so far: 4 works, 0 broken, 1 blocked, 1 not worth it.

## Queue (8 open)

| id | what | source | needs | after | attempts | est |
|---|---|---|---|---|---|---|
| P-0004 | Pitch harness: bookmaker disagreement (MaxH minus AvgH) as a feature on E0, pool weight | backlog | none |  | 0 | 30 min |
| P-0006 | GeckoTerminal new pools: of pools first seen on one day, what fraction still trade with any volume at 24h | backlog | none |  | 0 | 25 min |
| P-0009 | TfL unified API without a key: rate limit measured, one line's arrivals pulled | persona | none |  | 0 | 15 min |
| P-0010 | Wikipedia pageviews for the 20 Premier League clubs: does a pageview spike precede or follow results | persona | none |  | 0 | 25 min |
| P-0011 | Lichess bot API: what a bot account needs and whether a bot can be exercised without one | persona | Lichess bot account (Luke's one-click) |  | 0 | 20 min |
| P-0012 | Which of this month's AI builder tools from Field Notes still run cleanly a month later | field-notes | none | 2026-10-22 | 0 | 30 min |
| P-0013 | Grinder: split the first 20 scored positions by graphInsidersDetected (0, 1-5, over 5) and compare 24h outcomes | desk | none | 2026-10-20 | 0 | 15 min |
| P-0014 | pump.fun graduation rate over a full day: poll GeckoTerminal new_pools two pages every five minutes and count pump-fun v pumpswap creations | desk | a day-long poller (launchd job or hourly task), not a single-night probe |  | 0 | 30 min |

## Verdicts (6)

| date | id | what | verdict | note | artefact | cost |
|---|---|---|---|---|---|---|
| 2026-09-24 | P-0008 | DVSA MOT history: is there a keyless path, and what one car's public trail looks like | **works** | Keyless path exists for the aggregate: DVSA anonymised MOT results on data.gov.uk, 2023 zip 1.19 GB, 3.66 GB CSV, Deflate64 so Python zipfile refuses it, lookup tables 254 KB. A named car needs the MOT History API (401 MOTH-UA-01 without a client key; free registration, human job) and the GOV.UK check page is a 403 bot wall to curl. | `experiments/2026-09-24-P-0008` | 1 min |
| 2026-09-24 | P-0007 | Metaculus API without an account: can I pull open questions and community forecasts, and at what rate | **blocked** | Every listing endpoint (posts, questions, api2) returns 403 "only available to authenticated users" with plain and browser user agents. Throttle measured in front of the auth check: 9 calls in 1.9 s drew a 429 with Retry-After 10. Reruns unchanged once a token exists. | `experiments/2026-09-24-P-0007` | 1 min |
| 2026-09-24 | P-0005 | pump.fun graduation rate: what fraction of one day's launches reached a pool, from a keyless source | **works** | GeckoTerminal new_pools lists pump.fun bonding-curve launches as dex pump-fun beside pumpswap, so both sides are keyless from one feed: 46 launches and 10 pumpswap pools in 3.6 minutes, about 22 percent, an upper bound because untraded launches are never listed. pump.fun API 403 geo-blocked, rechecked. Public RPC cannot count creations: 1000 signatures span 24 seconds and a 22-tx sample found no Create. A day needs a 5-minute poller, queued. | `experiments/2026-09-24-P-0005` | 2 min |
| 2026-09-24 | P-0003 | Pitch harness: Pinnacle closing (PSCH/PSCD/PSCA) instead of the average as the line to beat, one league (E0): does any model's pool weight move off zero | **not-worth-it** | Rescored the saved walk-forward probabilities against Pinnacle, average and max closing prices, no refit: all three lines within 0.001 Brier on E0 (n=590) and nine leagues (n=4639), and every model earns the identical pool weight against each. Pinnacle columns are absent for all 2026-27 and 45 percent of 2025-26, so it cannot be the live line. Keep the average close. | `experiments/2026-09-24-P-0003` | 1 min |
| 2026-09-24 | P-0002 | Grinder: leave-one-out on the latest snapshot to find the next binding gate after age (is the $10k 1h volume gate it) | **works** | Not the volume gate. On the fixed feed (24 Sep, 72 in-window rows) the next binding gate is top-10 share at 30 percent: 11 of 72 pass it, dropping it alone lifts entries 8 to 11, three rows fail on it alone. Dropping vol1h gives 9 and one row fails on it alone. Before the feed fix nothing passed liquidity so no gate was next. | `experiments/2026-09-24-P-0002` | 0 min |
| 2026-09-24 | P-0001 | Grinder: rugcheck insider flags (graphInsidersDetected, insider holders) on the latest snapshot: how many gate-passers carry them, and would the flag have changed G-0001 to G-0004 | **works** | graphInsidersDetected is populated on 6 of 8 gate-passers (median 5, max 37) and 16 of 30 non-passers, but the per-holder insider flag and insider risks are empty on all 38 reports, and the count grows with token age (BOME 2483). Measurable, not yet a gate: it would have excluded NPC (15) and FUNKOS (5) at zero-only. Rule unchanged. | `experiments/2026-09-24-P-0001` | 1 min |
