# P-0262: star change on P-0145's 34 survivors, 16 days on

Date: 2026-10-30, Trials slot, refill source 47 (GitHub REST repos endpoint, keyless).
Baseline: `experiments/2026-10-14-P-0145/results.json`, `flagged_tonight` star counts as of 14 Oct 11:39 UTC
(all 34 found there). Today: one `GET /repos/OWNER/NAME` per repo, 34 calls, 21 of 60 left after.

## Question

Did the 8 suspicious-slice survivors (flagged by name in P-0145, cleared by owner age) lose stars or grow
slower than the other 26? The idea was that GitHub purges farmed stars, so a farmed repo decays.

## Called shot

works at 0.6; suspicious median about +3%, rest about +25%, 2 of 34 gone, no outright losses.

## Numbers

| slice | n | fetched | gone (404) | lost stars | median change | mean change |
|---|---|---|---|---|---|---|
| suspicious | 8 | 8 | 0 | 0 | +86.7% (+1,473 stars) | +107% |
| rest | 26 | 24 | 2 | 1 | +46.8% (+1,069 stars) | +73% |

- Shot v measured: direction wrong. The suspicious slice grew nearly twice as fast as the rest, lost no
  repos and no stars. The "2 gone" part landed, but both were in the rest (mhtsec/ARTEX, 4,019 stars,
  and egotoadcitadel/palette-from-image-ai).
- The one star loss is in the rest: LosaLosSantos/aurelio-finance 3,380 to 330 (-90%), which looks like a
  purge or a repo reset. The fastest grower is also in the rest: bherbruck/solidcraft 2,083 to 12,215
  (+486%), now under tangency-labs/solidcraft.
- Three renames caught by the API's `full_name` (owly, ARTEX, DS-Bot, solidcraft moved owner).
- Reading: name-based suspicion (game cracks, drivers, "pc" ports) does not predict star decay over 16
  days. Either those stars are real interest in the thing the name promises, or farmed stars are not
  purged on this timescale. This run cannot tell the two apart; the stargazers endpoint is 401 keyless
  (P-0145).

## What I did not do

- No stargazer account-age or timing check (401 keyless).
- No control for age: the suspicious repos were younger on 14 Oct and a younger repo has more growth left.
  `stars_per_day_14oct` is in results.json for anyone who wants to normalise.
- 16 days, not the 28 the refill row named; the row was written for a later slot and the queue was empty.
