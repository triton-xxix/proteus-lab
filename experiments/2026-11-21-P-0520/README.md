# P-0520: do old YouTube videos far above the 52k line lack a most-replayed graph?

**Question.** P-0515 put the heatmap line at about 52,000 views; P-0506's 2013 video at 339,919 has
none. Read 25 pre-2015 videos at 150k to 1m views: one outlier or a pattern?

**Method.** `old.py`: yt-dlp flat search on ten queries with old-leaning words ("2011", "iphone 4",
"harlem shake 2013"), keep ids at 150k to 1m flat views (31 candidates), `-J --skip-download`, keep
uploads before 2015. Run about 12:50Z, 21 Nov 2026.

**Called shot:** works at 0.60; 3 to 6 of 25 old videos lack a graph.

## What happened

- **Broken as a method.** Search ranks recent uploads first whatever year the query names: of 23
  videos read, **4 were uploaded before 2015**. Then one `-J` call returned `null` JSON and the
  script crashed on it (no guard for a parsed `None`), so no results.json was written. The rows
  below are from the console.
- The 4 old ones: 2 without a graph, both Harlem Shake uploads from Feb and Mar 2013 (418,689 and
  574,163 views); with one: a 2012 guitar lesson (328,965) and a 30-second 2013 Harlem Shake
  (274,568).
- Of the 19 newer ones, 1 lacks a graph: a 2019 Minecraft video at 387,655.
- So old high-view videos without a graph: 3 now on file (P-0506's plus these two), all from 2013.
  Thin, but more than one.

## Shot v measured

Called works with 3 to 6 of 25. Got 4 old videos, not 25, and a crash. Verdict broken: miss.

## What a rerun needs

- A source of old videos that does not go through search ranking: a channel's uploads list
  (`/@channel/videos` sorted oldest) for channels active in 2010 to 2014, filtered on views.
- Guard `info is None` after `json.loads`.
