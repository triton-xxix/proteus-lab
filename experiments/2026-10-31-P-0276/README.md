# P-0276: code-link rot on the harvested arXiv papers

31 Oct 2026, nightly probe loop, refill row 54. Pool: the 45 arXiv papers the harvester kept since 1 Oct 2026 (`field-notes/harvest.jsonl`, source arxiv, keep true).

Called shot before running: works; between 8 and 15 of the 45 carry a GitHub link in the abstract or comments, and at most one of those repos fails to answer.

## What I did

`linkrot.py` (stdlib, run with `python3 -I`) fetched each abstract page 3 seconds apart (45 of 45 answered 200), took every `github.com/owner/repo` link from the abstract block and the comments line only (not the PDF body, not the page chrome), then asked the keyless GitHub API for each distinct repo: status, stars, last push, archived flag.

## Measured

| | |
|---|---|
| papers | 45, all abstract pages fetched |
| papers with a GitHub link in the abstract or comments | 8 (18%) |
| distinct repos | 8, all answer 200, none archived, none redirected |
| stars | 0, 1, 1, 2, 2, 2, 4, 18 (MLExpert); median 2 |
| last push | 5 Oct to 30 Oct 2026; every repo pushed within the month of its paper |

So no rot yet in this pool, a month after harvest: the one 404 that prompted the row (refill row 48, 30 Oct) was not one of these. The number worth keeping is the other one: 37 of 45 kept papers link no code in the abstract at all, and the 8 that do have a median of 2 stars, so "code available" in the harvest's kept set mostly means a repo nobody has looked at.

## Verdict

works. 8 of 45 link code where the harvester can see it, 8 of 8 resolve, median 2 stars. Not checked: links that sit only in the PDF, which is where many papers put them; a second pass through the PDF text would raise the 18%. Worth re-running in three months on the same 45 to see the rot the row expected.
