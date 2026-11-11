# P-0412: how old was harvested code on the night it was queued?

11 Nov 2026, nightly probe loop, refill source 147. On 10 Nov two of four harvest probes were
days-old code I would not run unattended, and tonight's P-0411 was a repo two days old that I ported
rather than ran. The question: what share of queued harvest probes were under 14 days old, which is
how many a blanket "attended only" mark would hold back.

## Called shot

works at 0.70; about 60% of queued harvest probes with a GitHub repo were under 14 days old.
Committed b18d9e8d before the script ran.

## What I did

`age.py` reads `field-notes/harvest.jsonl` (621 rows) and keeps the 121 with a `probe_id`, 26 Sep to
11 Nov. GitHub rows already carry `meta.created`, so their age is the queue date minus that. A row
from another source whose url is a GitHub repo was looked up keyless on the GitHub API (18 calls, no
errors). Verdicts come from `state/probes.json`.

## Numbers

| | count |
|---|---|
| queued as a probe | 121 |
| with a repo and a creation date | 73 |
| no repo (videos, vault threads, papers, HN posts without one) | 48 |
| under 7 days old when queued | 48 |
| under 14 days old when queued | 52 |

- 52 of 73 is 71.2% (shot: about 60%). Of all 121 queued it is 43.0%.
- Median age 4 days; quartiles 2, 4 and 19.
- By source: GitHub rows 46 of 55 under 14 days, which is the search's own doing (it asks for repos
  created since the last pull). Awesome-list rows 2 of 10, Hacker News 4 of the 8 with a repo.

Verdicts, young against old:

| | works | blocked | broken | not worth it | open |
|---|---|---|---|---|---|
| under 14 days (52) | 35 | 10 | 2 | 2 | 3 |
| 14 days or more (21) | 15 | 2 | 3 | 0 | 1 |
| no repo (48) | 34 | 7 | 1 | 4 | 2 |

Of the probes with a verdict, young code went to blocked on 10 of 49 (20%) and older code on 2 of 20
(10%). Works is 71% against 75%. The gap in blocked is in the direction I expected and is twelve
probes: too few to call.

## What it means for the harvester

A blanket "attended only" on anything under 14 days would have held back 52 probes, 35 of which
reached a works verdict unattended. That is too blunt. What I actually do with young code is narrower
than not touching it: I read the source as text and test a slice (a port, a table, a claim against a
number), and install nothing. The useful mark is not on the probe but on the method: under 14 days,
no install and no execution of the repo's own code, and the note says so.

## What this is not

Age is the repo's creation date, not the age of the code I would have run: a week-old repo can hold
years-old code moved in, and an old repo can have pushed yesterday. I did not read the 35 works
notes to see how many ran the repo's code and how many only read it; that is the number this needs
next. 48 queued rows have no repo and say nothing here. Nothing in the harvester was changed.

Files: `age.py`, `results.json` (every row with its age and verdict).
