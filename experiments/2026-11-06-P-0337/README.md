# P-0337: the matched MOT league before COVID (6 Nov 2026)

Refill row 100. P-0330 found the raw 2023 table flatters the Juke and the Fiat 500 by about 0.2 once age,
mileage and fuel are matched. Is that a 2023 artefact?

Shot: Juke flattered by about 0.15 in 2019 (0.22 in 2023), and a mean absolute move in matched ratio of about
0.06 across the families. Measured: **0.37, and 0.036.** The Juke half missed, the wrong way: the flattery is
bigger before COVID, not smaller.

## What I ran

`league_2019.py`, which is P-0330's `league.py` with the URL changed and the compression and delimiter read from
the file. The 2019 file differs from 2023's: Deflate rather than Deflate64, commas rather than pipes. First 8M
rows, 5,452,267 tests kept after the same filters.

## The window is not what I queued

The title says 1 Jan to about 6 Mar 2019. The first 8M rows of this file run **1 Apr to 8 Jun 2019**, and I only
learned that from the run. So this compares spring 2019 with winter 2023: the year and the season are tangled.
The fleet fail rate is 34.4% here against 30.1% in P-0330, and I cannot split that between the two.

## What I found

`flatter` is raw ratio minus matched ratio, so negative means the raw table flatters the model.

| Family | Matched 2019 | Matched 2023 | Move | Flatter 2019 | Flatter 2023 |
|---|---|---|---|---|---|
| Nissan Juke | 1.05 | 1.21 | +0.16 | -0.37 | -0.22 |
| Fiat 500 | 1.25 | 1.19 | -0.05 | -0.38 | -0.17 |
| Nissan Qashqai | 1.12 | 1.11 | -0.01 | -0.22 | -0.10 |
| Renault Clio | 1.32 | 1.38 | +0.06 | +0.09 | +0.09 |
| Land Rover Range | 0.77 | 0.71 | -0.05 | -0.09 | -0.08 |
| Mini | 0.90 | 0.92 | +0.02 | +0.13 | +0.31 |

1. **The matched table is stable across four years.** Mean absolute move 0.036 over all 20 families, and every
   family but one moves 0.07 or less. Clio is worst in both years, and Range Rover and the BMWs stay near the bottom.
2. **The flattery is not a 2023 artefact.** The raw table flatters the Juke and the 500 in both years, and by more
   in 2019. The likely reason, which I did not test: both were young models then, and a young fleet looks good in
   a raw rate. Their flattery shrinks as they age.
3. **The Juke is the one real mover,** 1.05 to 1.21. Matching on age should absorb plain ageing, so something
   else may be going on; this probe does not say what.

`results.json` has all 20 families.

## What I did not do

Align the seasons. A fair check would take spring 2023 or winter 2019 from a later part of each file; 2023 is
ordered by date, so that needs a longer stream. No sampling error is computed. With tens of thousands of tests
per family it is small beside these moves, but the year and season tangle is not.
