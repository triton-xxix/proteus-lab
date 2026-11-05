# P-0330: a matched MOT league table, 20 most-tested model families (5 Nov 2026)

Follows P-0326. `league.py` streams DVSA's 2023 results zip (Deflate64, pipe-delimited) and
aggregates as it reads: the first 8,000,000 rows, tests dated 1 Jan to 6 Mar 2023, 5,783,039 class 4
normal tests of petrol or diesel cars aged 3 to 25. Initial fail = F or PRS. Fleet rate 30.1%.

Each family's **matched ratio** is its fails over the fails it would have at the fleet's rate for its
own mix of age (year), mileage (20k bands) and fuel. 1.00 is fleet average for that mix. The **raw
ratio** is its plain fail rate over the fleet's. Raw minus matched is how much the raw table
misleads: negative means the raw table flatters the car, positive means it is harsher than the car deserves.

| Family | Tests | Raw | Raw ratio | Matched ratio | Raw minus matched |
|---|---|---|---|---|---|
| Land Rover Range | 71,498 | 19.1% | 0.64 | **0.71** | -0.08 |
| BMW 3 | 80,177 | 28.4% | 0.94 | **0.76** | +0.18 |
| Mercedes C | 72,425 | 25.5% | 0.85 | 0.83 | +0.02 |
| Audi A3 | 81,926 | 26.4% | 0.88 | 0.83 | +0.04 |
| Honda Jazz | 63,440 | 25.7% | 0.85 | 0.83 | +0.02 |
| VW Golf | 171,985 | 27.8% | 0.92 | 0.85 | +0.07 |
| BMW 1 Series | 57,855 | 26.8% | 0.89 | 0.85 | +0.04 |
| Mini | 61,758 | 37.0% | 1.23 | 0.92 | **+0.31** |
| Honda Civic | 57,983 | 33.5% | 1.11 | 0.93 | +0.18 |
| Toyota Yaris | 69,050 | 31.9% | 1.06 | 0.95 | +0.10 |
| Ford Focus | 196,434 | 33.1% | 1.10 | 0.99 | +0.11 |
| Vauxhall Astra | 140,959 | 35.4% | 1.18 | 1.03 | +0.14 |
| Nissan Qashqai | 100,660 | 30.5% | 1.01 | 1.11 | -0.10 |
| Ford Fiesta | 275,510 | 34.3% | 1.14 | 1.13 | +0.01 |
| VW Polo | 114,945 | 34.8% | 1.16 | 1.14 | +0.02 |
| Ford Transit | 112,092 | 35.6% | 1.18 | 1.17 | +0.01 |
| Fiat 500 | 59,219 | 30.7% | 1.02 | 1.19 | -0.17 |
| Nissan Juke | 53,452 | 29.8% | 0.99 | 1.21 | **-0.22** |
| Vauxhall Corsa | 175,515 | 37.3% | 1.24 | 1.22 | +0.02 |
| Renault Clio | 63,607 | 44.2% | 1.47 | **1.38** | +0.09 |

## What it says

- The raw table flatters the young cars: Nissan Juke and Fiat 500 look fleet-average raw (0.99,
  1.02) and fail about 20% more than cars of their own age and mileage (1.21, 1.19). Qashqai the same, smaller.
- It is harshest on old, high-mileage survivors: the Mini looks 23% worse than the fleet raw and is
  8% better once matched; the 3 Series and Civic gain 0.18 each.
- The Clio is the worst of the twenty either way (1.38 matched). Range Rover and 3 Series are best matched.
- P-0326 again from a different method: Corsa 1.22 over 3 Series 0.76 is 1.61, against 1.62 there.

## Caveats

Ten winter weeks, not the year. Families are make plus first model word, so "Range" mixes Range
Rover, Sport and Evoque and Transit includes class 4 vans. PRS counts as a fail. No confidence
intervals; with 50k to 275k tests a family, the ratios' sampling noise is around 0.01 to 0.02,
smaller than the differences discussed, but the strata are coarse (20k-mile bands).
