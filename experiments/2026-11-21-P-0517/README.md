# P-0517: is the petitions constituency hole about size or the calendar?

**Question.** P-0516 found 2.64% of UK signatures on big 2019-24 petitions sit in no constituency,
peaking on 2020-21 petitions, and guessed signing load. Does the share track petition size, or the
date?

**Method.** `size_v_date.py`: keyless `archived/petitions.json?parliament=4&state=published`, which
is sorted by signature count, largest first (checked: true on all 17 pages). Took the 400 largest,
fetched each archived JSON, UK row minus constituency sum. Split by size band and opening era, and
by opening month. Run 12:39Z to 12:41Z, 21 Nov 2026; 399 of 400 read, 1 fetch error.

**Called shot:** works at 0.65; calendar wins, 2020-21 at least twice the 2023-24 share inside each
size band, little slope with size.

## Numbers

Unplaced share of UK signatures, by size band (rows) and opening era (columns):

| UK signatures | lockdown, Mar 2020 to Jun 2021 | Jul 2021 to 2022 | 2023 to 2024 |
|---|---|---|---|
| 10k to 50k | 2.81% (76) | 1.55% (33) | 0.76% (34) |
| 50k to 150k | 2.74% (121) | 1.76% (41) | 0.75% (30) |
| 150k and up | 3.13% (42) | 1.57% (13) | 0.68% (9) |

- **Size does nothing**: inside each era the three bands sit within half a point of each other.
- **The date does it, and as a step**: every month from Mar 2020 to Nov 2021 runs 2.3% to 3.9%.
  Dec 2021 1.83%, Jan 2022 1.51%, **Feb 2022 0.62%**, and every month after sits at 0.47% to 1.03%.
- No petition opened before Mar 2020 made the top 400 (parliament 4 began Dec 2019).

## Shot v measured

Called: lockdown share at least twice 2023-24 in each band, little size slope. Measured: 3.7x, 3.7x
and 4.6x, flat in size. Hit. My P-0516 guess (load) is now wrong on the evidence.

## What it says

Something changed in how signatures are placed in seats around January to February 2022, and
petitions opened before it carry about four times the hole. A step, not a slope, points to a system
change (a postcode lookup refresh, a backfill, a validation rule), not to traffic. The site's own
changelog or GitHub repo (alphagov/e-petitions) would say which; I did not look.

## What I did not do

- Top 400 by size only; small petitions under the 400th are not read.
- Did not check e-petitions commit history for Jan to Feb 2022.
- Whether a petition opened in 2021 that kept signing after Feb 2022 shows a mixed share: not split.
