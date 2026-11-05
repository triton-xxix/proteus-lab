# P-0328: YouTube link rot in HN comments at 12 and 14 years (5 Nov 2026)

P-0320's `rot.py` with only the windows changed: comments from the last days of 2011 and of 2013,
100 unique YouTube ids each, checked by oEmbed one a second. `results.json` has every id.

| Comments from | Age | Resolve | 404 gone | 403 private | Source |
|---|---|---|---|---|---|
| late Dec 2011 | ~14 years | 0.72 | 17 | 11 | tonight |
| late Dec 2013 | ~12 years | 0.67 | 25 | 7 (+1 embed off) | tonight |
| late Dec 2016 | ~10 years | 0.72 | | | P-0320 |
| late Dec 2021 | ~5 years | 0.86 | | | P-0320 |
| recent | days | 0.99 | | | P-0313 |

**Verdict: the loss flattens.** About 2.5 points a year for the first ten years, then nothing
measurable: 12 and 14 years sit at 0.67 and 0.72, within one standard error (about 4.5 points at
n = 100) of ten years. A link that survived its first decade is about as likely to survive the
next four. The shot was a continued slide to about 0.62 at 2011; it did not happen.

Caveats: 100 ids a window, a few days at each year end, one night's oEmbed answers. 403 is counted
lost (private or restricted), as in P-0320.
