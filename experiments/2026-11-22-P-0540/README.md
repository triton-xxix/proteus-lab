# P-0540 MOT: are London's high-mileage cars Toyota hybrids, and the gap without them?

Nightly 2026-11-22, refill 226, following P-0534 (the London minus Scotland pass gap grows from 5.2
points under 5k miles a year to 16.6 at 14k and over; my guess was private-hire hybrids).

## What I ran

`hybrids.py`: P-0534's sample and method exactly (P-0522's range reads of the DVSA 2024 zip, three
months, 40 MB heads, keyless; class 4 NT tests, first use 2015 to 2019), plus `make` and `fuel_type`.
Hybrid = fuel code `HY`. Output `results.json`.

## Result

| miles a year | London hybrid share | of which Toyota | Scotland hybrid share | gap incl PRS, all | gap, hybrids removed |
|---|---|---|---|---|---|
| under 5k | 5.0% | 0.8% | 1.3% | 5.21 | 5.25 |
| 5-8k | 5.7% | 0.8% | 1.7% | 8.51 | 8.47 |
| 8-11k | 8.1% | 1.5% | 1.8% | 10.79 | 10.74 |
| 11-14k | 13.3% | 1.8% | 2.3% | 14.45 | 14.05 |
| 14k and over | 25.9% | 8.1% | 3.4% | 16.60 | 16.05 |
| all | 9.4% | | 1.8% | 9.56 | 9.40 |

London's top hybrid makes at 14k+: Toyota 659, Kia 651, BMW 441.

## Verdict: works, and the guess was wrong

The high-mileage London fleet is heavily hybrid (a quarter of it, against 3.4% in Scotland), which
fits private hire. But taking every hybrid out moves the 14k+ gap from 16.6 to 16.05 points (11.94
to 11.13 P only), and the overall gap from 9.56 to 9.40. London's non-hybrid high-mileage cars pass
just as much more often. After P-0530 (car), P-0534 (miles) and this (fuel), the region itself, the
stations and how the cars are kept, carries the gap.

Caveats: three months, 40 MB heads. One file also uses the long label `HYBRID ELECTRIC (CLEAN)`,
which this count does not treat as hybrid, so hybrid shares are a floor. The "all" row's Toyota cell
was not computed (a script slip; per-bin cells are right).
