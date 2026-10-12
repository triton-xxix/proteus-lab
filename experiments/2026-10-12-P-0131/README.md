# P-0131: API-Football injuries on the Free plan

**Question.** Does `/injuries` answer on the Free plan, and how many of the 100 daily requests does a round cost?

**Called shot.** blocked at 0.60, "no key". Wrong: the Api-Sports key Luke named on 30 Sep is already wired into
`pitch/apisports.py`, and I had not checked before calling it.

**Method.** `run.py` (with `.venv` python) spent five counted requests: injuries by date for today and tomorrow,
by league and season, a fixture list for tomorrow, and injuries for one fixture from it.

**Numbers** (`result.json`):

| call | answer | requests left after |
|---|---|---|
| /status | plan info | 100 (not counted) |
| /injuries date=2026-10-12 | 168 rows | 98 |
| /injuries date=2026-10-13 | 290 rows | 97 |
| /injuries league=39 season=2026 | refused: Free plan seasons 2022 to 2024 only | not shown |
| /fixtures date=2026-10-13 | 291 fixtures | 96 |
| /injuries fixture=1563192 | 20 rows | 95 |

So asked by date, the Free plan answers for the current day and the next, like fixtures and odds. One request
covers every fixture that day in every league. A Pitch round over a weekend is two or three requests, against
the 100 a day the nightly fetch already shares (fetch spends about 2 plus one per fixture for odds).

**Caveats.** This is an international-break week, so these rows are mostly not the nine Pitch leagues; I did
not count how many fall in them. One-day-ahead only: Friday's run sees Saturday, not Sunday.

**Not done.** Not wired into `apisports.py fetch` or the judgement book.
