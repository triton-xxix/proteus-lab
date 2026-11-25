# P-0483: ONAA store block recheck, a week on from P-0482

Nightly 25 Nov 2026, desk probe. On 18 Nov (P-0482) the API's own openapi.json listed six store and buying
GET paths that all answered 404, plus a 404 issuer JWKS. Question: still 404 a week on?

Called shot: 7 of 7 still 404, nothing else moved. Half right.

## What I ran

`paths.py` is P-0482's checker, copied here so its results land in this folder (keyless, read-only GETs
1.5 s apart, only status, size and type kept). `compare.py` diffs the two weeks and asks last week's seven
404s directly, since they were no longer in the spec.

## Result (`results.json`, `compare.json`)

- All seven still 404 when asked directly: `/stores.csv`, `/stores.json`, `/v1/buying/check`,
  `/v1/buying/stores`, `/v1/stores`, `/v1/stores/check`, `/.well-known/onaa/issuer-jwks.json`.
- But the spec changed under the same version string (0.1.0): 84 paths down to 78. The six store and
  buying paths and `/agent/ucp-profile.json` are gone from it; `/v1/market/ranges` and `/v1/market/rules`
  are new, both 401 without a key. The JWKS is still documented and still 404.
- Every path asked both weeks answered the same status (0 changed).

## Verdict: works

The recheck ran and answers the question: the store block is still 404, and the operator has since taken
those paths out of the published spec rather than bringing them up, so it now reads as withdrawn, not
broken. The store surface seems to have moved to an authenticated "market" area. The JWKS gap remains a
documented path that does not exist. The spec version did not change with the edit, so the version
string is no help for spotting change: diff the path list.
