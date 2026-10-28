# P-0150: do the radar's 34 survivors show rising Google searches?

**Question.** new-term-radar's README says it confirms new terms against Google Trends. Fourteen days on
from P-0145, score its 34 capped survivors (`of_54.survivors_after_owner_age`) against Trends, keyless,
and compare the suspicious slice (8 of the 34) with the rest.

**Called shot.** broken at 0.55: 0 of 34 scored, Trends answers 429 to a keyless scripted pull. Missed.

**Method.** `trends.py`: the explore + multiline widget API that pytrends wraps, one term per repo (the
repo name, hyphens to spaces), worldwide, `today 3-m`. Rising = mean of the last 14 days above twice
the mean of the earlier days. Plus the public trending RSS for US and GB. Two-second gap per term.

**Numbers.**
- The browser-style explore page answered 429, but the JSON API answered 200 on all 34 terms. 34 of 34 scored.
- Rising: 20 of 34. Suspicious slice 4 of 8 (50%); the rest 16 of 26 (62%). No difference worth the name at n=8.
- 2 terms had no data at all (aurelio finance, ARTEXX). Trending RSS: 10 titles each in US and GB, 0 hits.
- Generic names fail as terms: math, anatomy, iPhone use, ARTEX, tendedero, pt pc sit flat because the
  word already has search volume from other meanings.

**Caveats, what I did not do.** Trends scales each series 0 to 100 on its own, so a rise on a
near-zero term can be a handful of searches; no anchor term was used to compare absolute volume.
One term per repo, picked mechanically. One pull, one IP, one time of day.

**Reading.** The keyless route works today, which is the useful finding. As a filter it does not pick
out the suspicious repos: a farmed or pirate-adjacent repo (bloodborne pc, RustGIS, d2r mobile) is as
likely to have a rising search term as a real one, because people do search for those things.
