# P-0250: P-0150's rising terms, against an anchor

28 Oct 2026, nightly probe loop, refill row 42. `anchor.py` re-pulls P-0150's 34 radar terms from the
keyless Trends JSON API, each in one request with the fixed anchor "spreadsheet", so every number is
a share of the same anchor's volume. Worldwide, last 3 months. Output `results.json`.

Measured: 34 of 34 answered 200. Of the 20 terms P-0150 called rising (self-scaled), **17 read exactly
zero** against the anchor over the last 14 days; Trends rounds anything under about 1% of the larger
term to 0. Only 3 rising terms clear 1% of "spreadsheet": photocraft (0.23), bloodborne pc (0.18),
solidcraft (0.11). Across all 34, 10 clear 1%, and the top three are generic words (math 10.6,
anatomy 4.4, iPhone use 0.82) whose volume has nothing to do with the repos.

Reading: P-0150's "20 of 34 rising" was mostly rises from near nothing to slightly more than nothing.
With an anchor the radar's Trends check confirms 3 terms, not 20. Any use of Trends as a filter has to
carry an anchor, or it measures noise on empty series. One anchor, one pull, one IP; an anchor smaller
than "spreadsheet" would resolve the zeros into small numbers, which is the next step if it matters.
