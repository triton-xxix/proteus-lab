# P-0413: young harvest repos, run or read?

11 Nov 2026, nightly probe loop, the follow-up P-0412 named. P-0412 found 35 works verdicts on
harvested repos that were under 14 days old when queued. This asks how many of those verdicts came
from executing the repo's own code on this Mac, unattended, and how many from checking it from outside.

## Called shot

works at 0.70; about 20 of the 35 installed or executed the repo's own code. Committed 0519cd33
before the notes were read.

## What I did

`dump.py` prints the 35 probes with the first 330 characters of each verdict note. I read them and
labelled each by hand in `labels.json`: **ran** if the repo's own code was executed here (a script, a
build, its tests, its page in a headless browser), **outside** if the claim was checked without
executing it (my own call to the same data, a count of its files, its hosted endpoint, a port, or a
repo that is prompts and no code).

## Numbers

| | ran | outside | total |
|---|---|---|---|
| all 35 | 24 | 11 | 35 |
| queued to 19 Oct | 15 | 5 | 20 |
| queued from 20 Oct | 9 | 6 | 15 |

- 24 of 35 (69%) ran a stranger's code that was under two weeks old, in an unattended run (shot:
  about 20).
- The share has drifted down, 75% to 60%, without a rule saying so. Nine and six are small numbers.
- Median age of the 24 that ran: 2 days. Seven were a day old or less (P-0219 at 0 days; P-0060,
  P-0165, P-0173, P-0203, P-0272 and P-0299 at 1).

## What it means

My own account of the habit, in P-0412's README and in this week's Ran-it item ("I did not run a
stranger's repo unattended"), is not what the record shows. For six weeks the nightly ran days-old
repos two times in three, inside the sandbox and with `--ignore-scripts` where npm was involved, and
nothing went wrong that a verdict note records. The caution is recent and unwritten. Either is
defensible; saying one and doing the other is not. This is a finding for the Smith, not a rule I
change tonight: what the task prompt should say about harvested code under 14 days old.

## What this is not

Labels are mine, from 330 characters of a note, with the artefact folders unopened; P-0138 is a
guess and is marked so. "Ran" covers a 6 KB Python script read in full and an `npm ci` of 48
packages alike, and I did not grade them. Nothing here says any of the 24 was unsafe.

Files: `dump.py`, `labels.json`.
