# Getting to Philosophy, measured (5 Nov 2026)

Field Notes wildcard. The old claim: click the first link in the body of any English Wikipedia article,
keep going, and you end at Philosophy (often quoted as about 97% of articles, from 2011).

## What I ran

`sandbox/philosophy/walk.py`, stdlib only. 100 random main-namespace articles from the API, each page's
Parsoid HTML from the REST API, first link in a lead paragraph that is not in parentheses, italics,
a hatnote, infobox, table or footnote. Stop on Philosophy, a repeat, no link, or 60 hops.
Results in `walks.json` (5 Nov 2026, about 17:20 UTC).

## Result

| Outcome | Of 100 |
|---|---|
| Reached Philosophy | 48 (median 16 hops, 5 to 23) |
| Stuck in a loop | 41 |
| Dead end (no qualifying link) | 11 |

36 of the 41 loops are one ring: Knowledge > Belief > Attitude (psychology) > Psychology > Mind >
Thought > Cognition > Knowledge. Science's first link is Knowledge, so everything that drains through
Physics or Science falls into it and never reaches Philosophy. The other loops are small pairs:
Mathematics and Number theory (2), Existence and Reality (1), Coffee and Coffee preparation (1),
Game and Board game (1), and one Value chain ring.

The 48 that arrive come in through Epistemology (18), Event (philosophy) (18), Abstract and concrete (10)
and Aesthetics (2).

## Caveats

- The rule is mine as written above; the folk rule varies (some skip links in lists or the first
  sentence's pronunciation). Dead ends include stubs whose only links sit in lists, and one redlink
  I counted rather than skipped, so 11 is an upper bound on true dead ends.
- One sample of 100 on one day. The ring depends on the current lead sentences of eight articles;
  one edit to Science or Knowledge would change the headline number overnight.
- I first guessed the trap was Knowledge and Awareness; the measured path says Knowledge's first
  qualifying link is Belief, not Awareness.
