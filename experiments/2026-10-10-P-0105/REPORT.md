# P-0105: keep rugcheck's creator and insider fields every night

Date: 2026-10-10, nightly probe loop.

## Change
`grinder/scan.py`: `rug()` now also returns `insiders_of(report)`: creator, creator balance, creator
tokens (count, first 20), `graphInsidersDetected`, insider networks (count, first 20). No extra calls:
it is the report the scan already fetches. `snapshot()` writes one line per token to
`grinder/insiders/YYYY-MM-DD.jsonl`, which `preregister.py` commits with the night's snapshot (a .jsonl
under grinder/), so the fields are dated before any outcome.

## Test
`check.py` imports the edited scan and calls `rug()` on five tokens (tonight's four entries and G-0059).
It does not run `snapshot()`, so SNAPSHOTS.csv was not touched.

| Token | graphInsidersDetected | insider networks | creator tokens |
|---|---|---|---|
| qOMPUTE | 0 | 0 | 0 |
| CYBERINU | 0 | 0 | 0 |
| LLM | 12 | 2 | 0 |
| Altai | 55 | 6 | 0 |
| Gary (G-0059, stopped out at -53) | 206 | 2 | 0 |

## Verdict
Works: the fields are there and vary enough to test. One honest limit: `creatorTokens` was null on all
five, so the "serial creator" lead may have nothing in it on pump.fun tokens; the side file will show
within a week. The snapshot's own write path runs for the first time in tomorrow's step 2.
