# P-0320: YouTube link rot in HN comments, by age

**Question.** P-0313 found 149 of 150 YouTube links in fresh HN comments resolve. How fast does that fall
with age? It is the number a HackerTV-style feed of old threads lives on.

**Method.** `rot.py`, P-0313's method with Algolia's `numericFilters=created_at_i<cut`. For each window, 400
comments (two queries, two pages), the first 100 unique video ids, YouTube oEmbed 1 s apart, 4 Nov 2026.

**Numbers.**

| comments from | ids | 200 | 404 gone | 403 private | 401 embed off | resolve share |
|---|---|---|---|---|---|---|
| last days of Nov 2026 (P-0313) | 150 | 149 | | | | 0.99 |
| 29 to 31 Dec 2021 | 100 | 88 | 11 | 1 | 0 | **0.88** |
| 28 to 31 Dec 2016 | 100 | 73 | 20 | 6 | 1 | **0.73** |

Shot: 0.72 for 2016 and 0.86 for 2021. Roughly 2.5 points of links lost a year, front-loaded: 11 in the first
five years, 15 more in the next five.

**Caveats.** 100 ids is a standard error near 4 to 4.5 points. Each window is three or four days at a year
end, not the whole year. 403 counts as lost for a feed (private or region-locked), and so does 401
(the video exists but will not embed).

**For a feed.** A feed of ten-year-old HN video links needs a resolve check per item and loses about one in
four; a five-year-old one loses about one in eight.
