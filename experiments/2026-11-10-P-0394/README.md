# P-0394: GitHub tiny paste-link count, rerun with an id baseline

**Question.** P-0386 (9 Nov) counted 10 tiny (<50 KB) new repos with 50+ stars whose README carries a
paste-site link and a run-exe, inject or antivirus phrase, but saved counts only, so refill row 139's
48-hour takedown recheck had nothing to match. Rerun today, keep ids, and see whether the count holds.

**Shot.** works at 0.70: tiny paste-and-run matches between 6 and 14.

**Method.** `baseline.py`, P-0386's search, regexes and plain-text README read unchanged (read-only,
never follows a link). Counts to results.json here. Numeric repo ids, created time, stars and a README
sha256 for all 35 tiny repos to `sandbox/p0394-ids.json`, which is gitignored: no repo is named
anywhere committed, since a regex match proves nothing about one repo.

**Numbers** (results.json, run 12:44Z, window since 7 Nov). 119 repos, all READMEs read; 35 under 50 KB;
paste links in 8 of 35 tiny against 2 of 84 larger; 7 tiny with paste and run phrase (9 Nov: 10 of 38,
11 of 38, 3 of 114). Shot hit.

**Answer.** The pattern is steady day to day: a fifth of tiny starred new repos carry paste links,
against 2 to 3 pct of larger ones.

**Next.** Recheck queued for 12 Nov: ask the API for each saved id, count gone (404), README changed
(hash), stars moved.

**Not done.** Matches not audited by hand, nothing opened or run.
