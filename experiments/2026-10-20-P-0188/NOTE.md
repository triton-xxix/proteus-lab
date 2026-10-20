# P-0188: do EVs fail MOTs less than petrol cars at 90k to 120k miles?

Claim (BVRLA, via the YouTube short in H-0351): 47.4 million MOTs 2024 to 2026, EV fail rate 16.5%
against petrol 22.1% at 90k to 120k miles; 16 against 23.5 above 120k.

Data: DVSA anonymised MOT results, `dft_test_result_extracts_2025.zip` (4.8 GB, from
https://open.data.dvsa.gov.uk/mot-anonymised/index.html). `mot_sample.py` reads the zip over HTTP
range requests and streams one member, December 2025: 2,749,665 tests, 312 MB fetched, nothing
large saved. Class 4 normal tests only (no retests), fail = F or PRS, mileage as recorded.
Fuel codes PE, DI, EL, HY; about 45k rows under long-form labels ("ELECTRIC", "HYBRID ELECTRIC
(CLEAN)") are left out of these tables.

| band | EV all ages | petrol all ages | EV first used 2018+ | petrol first used 2018+ |
|---|---|---|---|---|
| 60-90k | 19.3% (7,303) | 33.1% (299,072) | 18.7% | 21.4% |
| 90-120k | 19.3% (2,057) | 41.8% (167,014) | 17.2% (1,792) | 26.4% (5,694) |
| 120k+ | 22.5% (1,090) | 45.3% (93,403) | 16.2% (745) | 27.3% (1,152) |

Raw output for all ages in `all-ages-2025-12.txt`; the 2018+ run is the same command with
`--since 2018-01-01`.

## Verdict: works

The direction holds: EVs fail less in every band above 30k. At 90k to 120k the gap is 22.5 points
on all cars and 9.2 points once the petrol cars are held to the same age as the EVs (first used 2018
or later). The trade body's 5.6 points is smaller than either. My EV rate (17 to 19%) is close to
their 16.5%; their petrol rate (22.1%) is well below mine (26 to 42%). So they must define a fail
differently (perhaps PRS left out, or one result per vehicle) or weight by age. Half the raw gap
is age: petrol cars at that mileage are old, EVs are not. One month of 2025 is a sample, not their
47 million.
