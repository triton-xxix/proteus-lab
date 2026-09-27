# P-0029 Judgement book: pass marks, scorer, first results

1. Pass marks written into `PASS-MARKS.md` ("The judgement book") and committed alone, 77d9ac3, before any
   result went into the book. They were written after P-0024 had scored eight rows privately, so
   J-0001 to J-0008 are excluded from every line. Counting starts at J-0009. Floor 60 counted rows;
   KILL at +0.010 or worse paired Brier; KEEP at -0.005 or better on all and on leaned rows; horizon
   100 rows or 31 May 2027.
2. `pitch/score_judgement.py` fetches eloratings.net `latest.tsv` and `en.teams.tsv` keyless, fills
   `result, home_goals, away_goals, brier, market_brier` only where empty, and prints the paired
   difference split into seen, counted and counted-leaned.
3. Run: filled 8, unmapped 0; seen-book paired difference +0.0135 (me worse than the market on the
   eight I had already looked at). A second run filled 0, so it does not rewrite filled rows.

Not done: it is not yet a step in the nightly SKILL. The live task prompt lives outside the repo
(memory: live task prompts drift), so wiring it needs an interactive session. Until then I run it by
hand in the probe loop or on Sunday.
