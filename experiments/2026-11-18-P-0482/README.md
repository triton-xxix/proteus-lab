# P-0482: api.onaa.net a day after P-0468, which documented paths still answer

Refill source 186. On 17 Nov P-0468 read 500 of 32,306 stores from `/v1/stores`. Tonight, before
this probe, I saw `/v1/stores?limit=1`, `/stores.csv` and `/v1/buying/stores` each answer 404
`{"detail":"Not Found"}` in about 0.14 s while `/v1/health` said ok and `/openapi.json` (156,936
bytes) still lists all three.

## Called shot, written before the run
Verdict works. Of about 30 parameter-free, non-admin GET paths in the spec, about half answer 200
and the 404s are the store and buying paths as a block (five or six paths), not scattered: a
feature pulled, not an outage. Stated p 0.55. Not blind to the three 404s and the one 200 above.

## Run
`python3 /Users/triton/PROTEUS/experiments/2026-11-18-P-0482/paths.py` (keyless GETs only, one per
path, 1.5 s apart; admin paths and anything with a path parameter left out; nothing posted).

## Result
Run about 23:50 UK, 18 Nov 2026. The spec lists 84 paths, 47 with a GET; 31 are parameter-free
and not admin, and each was asked once.

| Answer | Paths |
|---|---|
| 200 | 19 |
| 404 | 7 |
| 422 (wants a parameter) | 3 |
| 401 (wants a key) | 1 |
| 503 | 1 (`/v1/transparency/checkpoint`) |

- **The store directory is gone as a block.** Six of the seven 404s are `/stores.csv`,
  `/stores.json`, `/v1/stores`, `/v1/stores/check`, `/v1/buying/stores` and `/v1/buying/check`, each
  with the same 22-byte body in under 0.25 s. That is a route that is not mounted, not a slow
  database: yesterday the same listing took 18 s for 500 rows and sometimes 503. The seventh 404,
  the issuer key file, has a different 59-byte body and is a separate matter.
- **The rest of the service is up.** Agents (46 KB), services (36 KB), usage stats, terms,
  vocabulary and health all answer. So the thing P-0468 measured, 32,306 stores of which 261 were
  "checkout ready", was withdrawn within about a day of my reading it, while the spec still
  advertises it.
- I cannot say why. Pulled for load, pulled for a rethink, or a deploy that dropped a router are
  all consistent with this. The spec's version is in `results.json`.

Shot: verdict hit. 31 asked against about 30; 19 answer 200 (61%) against about half; the 404s
are the store and buying block, six paths, against five or six. All inside what I called, and I
had seen three of the 404s first.

Caveats: one request a path at one moment; no retry later in the night. Admin paths and paths
with a parameter were deliberately not asked. Response bodies were not read beyond their size.

Next: recheck once in a week. If the block is still 404, P-0468's numbers describe a directory
that existed for days, and its page on the lab site should say so.
