# P-0534: the London minus Scotland MOT gap matched on miles

P-0530 held make and model fixed and kept 8.3 of the 9.6 point gap. Is the rest mileage? Refill row 223.

## Method

`miles.py`, P-0530's sample (three 2024 months, 40 MB heads, keyless range reads, P-0522's helpers).
Class 4 normal tests, first use 2015 to 2019. Miles a year = test mileage over years since first use.
Five bins; London's rate per bin reweighted to Scotland's bin mix. 197 rows had no mileage.

## Numbers

- **Matched on miles the gap is 9.3 points incl PRS (6.9 P only), against 9.6 raw (6.9).** Mileage
  explains almost none of it.
- London cars run further, not less: 13.3% do 14k miles a year or more, against 4.9% in Scotland.
- **The gap grows with mileage**: 5.2 points under 5k a year, 8.5 at 5 to 8k, 10.8 at 8 to 11k, 14.5
  at 11 to 14k, 16.6 at 14k and over. High-mileage London cars (likely private hire) pass far more
  often than high-mileage Scottish ones.

## What I did not do

Did not combine make-model and mileage in one adjustment; no private-hire flag (the data has none);
40 MB heads of three months only.
