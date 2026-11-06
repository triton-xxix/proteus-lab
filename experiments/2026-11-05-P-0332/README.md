# Dating the Knowledge ring (P-0332, night of 5 to 6 Nov 2026)

This afternoon's walk found 36 of 100 random articles trapped in a ring through Knowledge, Belief and
Psychology. I replayed the same first-link rule on Wikipedia as it stood on five past dates, from the
same 100 starts, to see when that ring formed.

## Result

| Date | Walked | Article existed | Reached Philosophy | Share of those that existed | Loops | Dead ends | Biggest trap |
|---|---|---|---|---|---|---|---|
| 1 Jul 2011 | 100 | 47 | 22 | 47% | 0 | 25 | none |
| 1 Jul 2014 | 100 | 59 | 50 | 85% | 0 | 9 | none |
| 1 Jul 2016 | 100 | 66 | 12 | 18% | 1 | 53 | dead end at Attribute (27 in the first pass) |
| 1 Jul 2018 | 100 | 75 | 4 | 5% | 53 | 18 | ring: Mathematics, Quantity, Counting, Element (52) |
| 1 Jul 2021 | 68 of 100 | 62 | 34 | 55% | 13 | 15 | ring: United Kingdom, Sovereign state, Polity (7) |
| 5 Nov 2026 | 100 | 100 | 48 | 48% | 41 | 11 | ring: Knowledge, Belief, Psychology and on (36) |

The Knowledge ring is recent. On 1 Jul 2021 Science's first link was Scientific method, and Science,
Knowledge and Belief all reached Philosophy. No walk at any earlier date ends in that ring. So it formed
some time between July 2021 and today; six samples cannot date it closer.

The bigger finding is that there is no stable arrival rate. It swings between 5% and 85% across samples,
and each collapse is one hub's lead sentence. In 2016 the route out of Knowledge ran into Attribute, which
offered no qualifying link. In 2018 it ran into a Mathematics ring that caught 52 walks.

I could not reproduce the folk 97% for 2011. My 47% is not a refutation, for the reasons below.

## Caveats

- **Dead ends are an upper bound, 2011 most of all.** A page moved later can leave a title with no history
  on that date. I follow today's redirect to recover it, which fixed the worst case (`Social sciences`, 13
  false dead ends in the first pass), but a title with neither history nor a redirect still reads as a
  dead end. `Academia` in 2011 is one I saw.
- **Old wikitext renders through today's templates**, so a template changed since can move a link.
- **Survivors only.** The starts are articles that exist today, not a random draw from 2011's Wikipedia.
- **2021 is partial**: 68 of 100, cut off by the time cap, so its rate could move.
- **2026 comes from the 17:18 walk**, not this script, though the rule and starts are the same. Its figures
  use the 5 Nov revisions rather than a dated lookup.
- **Six snapshots, not a series.** A 1 July sample can land on a bad week for one hub, so the swings show
  how fragile the result is, not a trend. The rule itself is mine; the folk rule varies.
- Red links are followed and counted as dead ends, as in the 5 Nov walk.

## Two faults found on the way

1. Dead ends read 39 of 47 in 2011 on the first pass. That was the page-move gap above, not the parser.
2. Six threads hit rate limits and turned up to 36 walks a date into errors. The pages load fine when asked
   again (`errors.py`). `finish.py` re-walked those rows at three threads; `final.json` has no error rows.

## Files

`ringdate.py` the walker on dated revisions, `walk_rule.py` the 5 Nov parser, `finish.py` the re-walk,
`results.json` the first full pass, `final.json` the numbers above, `deadends.py`, `errors.py` and
`inspect_page.py` the checks. About 5,500 keyless Wikipedia calls in all.
