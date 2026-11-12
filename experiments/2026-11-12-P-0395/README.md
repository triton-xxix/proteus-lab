# P-0395: GitHub takedown recheck, 48 hours on

**Question.** P-0394 saved the ids of 35 tiny (<50 KB) new repos with 50+ stars on 10 Nov 12:44Z, 7 of
them matching the paste-link plus run-phrase pattern. Two days later: how many are gone, how many
READMEs changed, and do the 7 matches go faster than the other 28?

**Called shot.** works at 0.60, "3 of 35 gone (inside 1 to 6), and the 7 matches gone at a higher rate
than the other 28". Hit on both, the second only just.

**Method.** `recheck.py` asks `api.github.com/repositories/ID` keyless for each id (35 calls, none rate
limited), counts 404 as gone, and for the rest reads README.md as plain text and compares its sha256
with the saved one. Read-only, no link followed, nothing run. Counts in `results.json`; ids and per-repo
rows stay in `sandbox/` (gitignored), because a regex match proves nothing about one repo.
Run 12 Nov 12:43Z, 47 hours 59 minutes after the baseline.

## Numbers

| Group | n | Gone (404) | Share | README changed | Stars fell | Median star move |
|---|---|---|---|---|---|---|
| All tiny | 35 | 5 | 14% | 1 | 9 of 30 | 0 |
| Paste link and run phrase | 7 | 2 | 29% | 0 | 4 of 5 | -160 |
| The other 28 | 28 | 3 | 11% | 1 | 5 of 25 | 0 |
| Any paste link | 8 | 3 | 38% | 0 | 4 of 5 | -160 |
| No paste link | 27 | 2 | 7% | 1 | 5 of 25 | 0 |

One-sided hypergeometric chance of a split at least this lopsided if removal ignored the label: 0.26
for the 7 matches (2 of the 5 gone), 0.07 for the 8 with any paste link (3 of the 5 gone). Worked by
hand from the counts above.

## What it says

- One in seven tiny starred new repos is gone inside two days. That is a fast base rate.
- The matches do go faster (29% v 11%) but 2 of 7 is not evidence; the plain paste-link flag separates
  better (38% v 7%) and still only reaches 0.07.
- The clearer signal is the stars, not the takedowns: of the 5 matches still up, 4 lost stars and the
  median move is -160, while the other 25 survivors sit at a median of 0. Stars being stripped from
  repos that stay up fits fake stars being purged before the repo is.
- READMEs barely move: 1 of 30 changed, none among the matches. Nobody is cleaning these up; they are
  either left or removed.

## Not done

- 404 does not say who removed it: GitHub, or the owner deleting or making it private.
- No hand audit of any repo, and no check of where the lost stars went.
- 35 repos, one window. A second baseline is needed before the 38% v 7% means anything.
