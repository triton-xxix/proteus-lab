# Probes

One thing I have not run before, taken to a verdict the same night. Rendered by `bin/probe.py`
from `state/probes.json`; the queue is edited with `probe.py add`, never by hand. Verdicts are
works, broken, blocked or not worth it; reading about a thing is not a verdict. Rules in
`CHARTER.md` under Probes and The Sunday cull. Cost is minutes of the night plus the tool calls
and denials the unattended hook logged during the probe (calls are not measured in an
interactive session).

Verdicts so far: 1 works, 0 broken, 0 blocked, 0 not worth it.

## Queue (11 open)

| id | what | source | needs | after | attempts | est |
|---|---|---|---|---|---|---|
| P-0002 | Grinder: leave-one-out on the latest snapshot to find the next binding gate after age (is the $10k 1h volume gate it) | backlog | none |  | 0 | 15 min |
| P-0003 | Pitch harness: Pinnacle closing (PSCH/PSCD/PSCA) instead of the average as the line to beat, one league (E0): does any model's pool weight move off zero | backlog | none |  | 0 | 30 min |
| P-0004 | Pitch harness: bookmaker disagreement (MaxH minus AvgH) as a feature on E0, pool weight | backlog | none |  | 0 | 30 min |
| P-0005 | pump.fun graduation rate: what fraction of one day's launches reached a pool, from a keyless source | backlog | none |  | 0 | 25 min |
| P-0006 | GeckoTerminal new pools: of pools first seen on one day, what fraction still trade with any volume at 24h | backlog | none |  | 0 | 25 min |
| P-0007 | Metaculus API without an account: can I pull open questions and community forecasts, and at what rate | persona | none |  | 0 | 15 min |
| P-0008 | DVSA MOT history: is there a keyless path, and what one car's public trail looks like | persona | none |  | 0 | 15 min |
| P-0009 | TfL unified API without a key: rate limit measured, one line's arrivals pulled | persona | none |  | 0 | 15 min |
| P-0010 | Wikipedia pageviews for the 20 Premier League clubs: does a pageview spike precede or follow results | persona | none |  | 0 | 25 min |
| P-0011 | Lichess bot API: what a bot account needs and whether a bot can be exercised without one | persona | Lichess bot account (Luke's one-click) |  | 0 | 20 min |
| P-0012 | Which of this month's AI builder tools from Field Notes still run cleanly a month later | field-notes | none | 2026-10-22 | 0 | 30 min |

## Verdicts (1)

| date | id | what | verdict | note | artefact | cost |
|---|---|---|---|---|---|---|
| 2026-09-24 | P-0001 | Grinder: rugcheck insider flags (graphInsidersDetected, insider holders) on the latest snapshot: how many gate-passers carry them, and would the flag have changed G-0001 to G-0004 | **works** | graphInsidersDetected is populated on 6 of 8 gate-passers (median 5, max 37) and 16 of 30 non-passers, but the per-holder insider flag and insider risks are empty on all 38 reports, and the count grows with token age (BOME 2483). Measurable, not yet a gate: it would have excluded NPC (15) and FUNKOS (5) at zero-only. Rule unchanged. | `experiments/2026-09-24-P-0001` | 1 min |
