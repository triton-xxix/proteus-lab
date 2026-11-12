# P-0348: the first-link walk, one week on

**Question.** P-0332 found the share of walks reaching Philosophy swinging between 5% and 85% across
yearly snapshots. How much moves in an ordinary week? Same 100 starts as 5 Nov 17:18, same rule,
today's revisions (12 Nov 12:42 UTC).

**Called shot.** works at 0.70, "at most 5 of the 100 starts change outcome class; Philosophy 46 to 50
against 48". Hit: 0 changed, 48.

**Method.** `rewalk.py` imports the 5 Nov parser (`experiments/2026-11-05-P-0332/walk_rule.py`)
unchanged, walks the starts from `experiments/2026-11-05-philosophy/walks.json` and compares each walk
with the old one: outcome class, end page, whole path, and the page where a changed path first departs.
Fetch errors other than 404 are retried; none were left. 504 pages fetched (505 on 5 Nov).

## Numbers

| | 5 Nov | 12 Nov |
|---|---|---|
| Reached Philosophy | 48 | 48 |
| Loop | 41 | 41 |
| Dead end | 11 | 11 |

- Outcome class changed: **0 of 100**. End page changed: 0 of 100.
- Path changed: 2 of 100, both still reaching Philosophy.
  - `Betty Todd`: first link was New York City, now Birth name.
  - `Indo-Aryan peoples` (on Waman Lakshman Kulkarni's walk): first link was People, now
    Indo-European studies.
- So 2 first links moved among about 504 pages walked in seven days, roughly 0.4% of pages a week,
  and neither was a hub.

## What it says

A week of ordinary editing moves nothing at the level that counts. The yearly swings in P-0332 are
not the sum of many small edits drifting the result; they are rare single edits to a hub's lead
sentence. With 0 of 100 in one week, a hub flip is rarer than about one week in a few, which is all one
sample can say. The Knowledge ring that holds 36 of the 41 loops is intact.

## Not done

- One week, one sample. It bounds nothing about how often a hub flips; a monthly rerun of this script
  would, and it costs about 500 keyless calls and three minutes.
- Did not check whether the two changed links were reverted edits or settled ones.
- The 11 dead ends were not re-examined; they are the same 11.
