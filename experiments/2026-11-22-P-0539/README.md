# P-0539 Lichess acceptance fall: same bots declining more, or new never-yes bots?

Nightly 2026-11-22, refill 225, following P-0531 (which found the fall is by date, not by hour).

## What I ran

`cohort.py` on `games/lichess/CHALLENGES.csv` (1,531 asks, 133 bots, weeks 41 to 47, on disk).
Answerable asks only (accepted, declined, no answer; Lichess cap refusals left out). Veterans are bots
first asked in week 41, newcomers first asked later. Output `results.json`.

## Result

| week | answerable asks | accepted | veterans | newcomers | asks to bots that never said yes |
|---|---|---|---|---|---|
| 41 | 102 | 11.8% | 11.8% | none | 61.8% |
| 42 | 112 | 8.9% | 6.4% | 22.2% | 78.6% |
| 43 | 287 | 7.0% | 6.2% | 8.9% | 76.7% |
| 44 | 282 | 3.2% | 3.0% | 3.8% | 92.6% |
| 45 | 118 | 7.6% | 8.7% | 6.1% | 86.4% |
| 46 | 76 | 6.6% | 0.0% | 11.6% | 84.2% |
| 47 | 135 | 8.9% | 5.0% | 14.5% | 88.9% |

The 22 bots asked in three or more weeks on both sides of week 41: 0 of 46 then, 2 of 628 since.

## Verdict: works

Neither of the two framings: it is the house rule. Since 14 Oct a bot that accepts is never asked
again (one game per opponent), so every yes leaves the pool and the asks pile onto bots that always
say no: 62% of answerable asks went to never-yes bots in week 41, 84 to 93% since. The repeat asks are
almost pure waste (2 yeses in 628). Newcomers still accept at about 10 to 15% in weeks 46 and 47.
So acceptance is set by how many new bots appear, not by bots changing their minds; skipping bots
that have declined, say, five times would cut most of the wasted asks without touching the rule.
