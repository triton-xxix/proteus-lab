# P-0516: did petitions before the 2024 boundaries leave more signatures in no constituency?

**Question.** The 20 Nov persona pick found 0.47% of UK signatures on 40 open petitions sit in no
constituency. Is the hole the same on archived petitions from the last two parliaments, and does it
jump at the July 2024 boundary change?

**Method.** `gap.py`: keyless JSON from `petition.parliament.uk/archived/petitions.json?parliament=N`
(found this run: the HTML archive lists parliaments 1 to 4; `.json` on the same path works). For
parliament 4 (2019-24) and 3 (2017-19), pages 1 to 3 of published petitions (75 each), the 40
most-signed of those, each archived petition JSON once. UK row of `signatures_by_country` minus the
sum of `signatures_by_constituency`. Run 21 Nov 2026 about 12:46Z, 80 of 80 read, 0 errors.

**Called shot:** works at 0.60; parliament 4 share 0.3% to 0.8%, about the same as today, no jump.

## Numbers

| | UK signatures | in no constituency | share | per petition |
|---|---|---|---|---|
| Parliament 4 (2019-24), 40 | 15,210,431 | 401,214 | **2.64%** | 0.47% to 5.48%, median 2.71% |
| Parliament 3 (2017-19), 40 | 15,565,539 | 260,966 | **1.68%** | 0.77% to 4.10%, median 1.49% |
| Open now (persona, 20 Nov), 40 | 2,022,815 | 9,580 | 0.47% | 0.24% to 2.13% |

- All 80 list 650 constituencies, so no seats are missing; the gap is never negative.
- Headline equals the country sum on 79 of 80.
- **By opening year** (both parliaments pooled): 2017 1.1%, 2018 1.6%, 2019 1.8%, **2020 3.0%,
  2021 3.7%**, 2022 0.6%, 2023 0.7%, 2024 0.6% (2022 to 2024 are three or four petitions each).

## Shot v measured

Called 0.3% to 0.8% for parliament 4; measured 2.64%. A clear miss on the number. "Works" held: the
archive answers keyless and the comparison runs.

## What it says

The hole is not a July 2024 boundary artefact: it was already back near today's level in 2022 to
2024, under the old seats. It peaks on the 2020 to 2021 lockdown petitions, the biggest and fastest
signing surges the site has had. My guess, not tested: the constituency count is filled by a
background job that lags or drops under load, while the country count is taken at signing.

## What I did not do

- "40 most-signed" is of the first three list pages (75 per parliament), not of every petition.
- No petitions before 2017; no check of whether the archived counts changed after closing.
- The load guess needs signing speed per petition, which the JSON does not give.
