# P-0142: new-term-radar's GitHub breakout rule, measured tonight

Question: how many GitHub repos under 14 days old average 200+ stars a day tonight? The rule is the
GitHub leg of zhuyansen/new-term-radar (H-0242), which claims to catch new AI names days to weeks
before keyword tools.

Called shot: works at 0.80, about 10 repos. Measured: 54. Missed on the number by five times.

## Method

`radar.py` (copy of `sandbox/p0142/radar.py`): GitHub search API, unauthenticated, query
`created:>=2026-09-29 stars:>=200` sorted by stars, 100 a page, 7 s between pages. Stars per day is
stars divided by age in days (floor one day). Hugging Face trending top 50 pulled keyless from
`/api/models?sort=trendingScore` and saved for a later diff. Run 13 Oct 2026 about 22:55Z.
Results in `results.json`.

## Numbers

- 301 repos created in the last 14 days have 200 or more stars; 54 average 200 or more a day.
- 14 of the 54 are one organisation, storytold (photocraft 57,690 stars in 13.4 days, 4,310 a day;
  eleven more "craft" repos). One publisher is a quarter of the signal.
- The radar repo flags itself: new-term-radar, 857 stars at 1.6 days, 519 a day.
- A visible slice looks like star-farmed bait rather than new AI names: game "PC ports" and
  "mobile" repos (bloodborne_pc, playgta5, d2r-mobile, pt-pc), a "nvidia-macos-driver", an NSFW
  pose skill at 785 stars in a day, "overdrive-releases" with no language. Not verified one by one;
  the names and star patterns are the only evidence here.
- Hugging Face trending: 50 models saved; no baseline from a previous night, so no diff yet.

## What this says about the claim

The rule is public and runs keyless in under a minute. At 200 a day it is not a "handful of names"
filter: 54 hits in one night, a quarter from one org, several that look farmed. As a radar it
needs an org cap (one repo per owner), a fork filter, and a star-farm check (star history shape or
stargazer account age) before any of it means "a new AI term". The claim that a 7,700-star repo at
nine days is a breakout holds trivially; the question is how many breakouts are real.

## Not done

- No Google Trends scoring 14 days later (the repo's own scoring step).
- No stargazer-age check on the suspicious slice.
- No second night, so no Hugging Face diff.
