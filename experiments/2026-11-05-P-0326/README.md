# P-0326: does a Corsa fail its MOT about 60% more than a 3 Series? (5 Nov 2026)

From tonight's harvest (H-0534, YouTube `zeTGescbQak`): a UK MOT video says a Vauxhall Corsa fails
"almost 60 percent more often" than a BMW 3 Series, with age, mileage and fuel matched.

## What I ran

DVSA's anonymised MOT results for 2023 (`data.dft.gov.uk/anonymised-mot-test/test_data/dft_test_result_2023.zip`,
1.19 GB). The zip is Deflate64 (method 9), which Python's zlib cannot read, so `sandbox/mot/stream.py`
inflates it with `inflate64` 1.0.4 as it downloads and stops after 8,000,000 rows: test dates
1 Jan to 6 Mar 2023. `sandbox/mot/compare.py` keeps class 4 normal tests of Corsas and 3 Series
(models 3xx), petrol or diesel, age 3 to 25, and counts F and PRS as an initial fail.
Matching: strata of whole years of age x 20,000-mile bands x fuel, 248 strata with at least 20 tests
of each car.

## Result (`result.json`)

| | Corsa | 3 Series | Ratio |
|---|---|---|---|
| Raw initial fail rate | 37.4% (176,577 tests) | 26.9% (91,746) | 1.39 |
| Standardised to the 3 Series mix | 41.9% | 26.4% | 1.59 |
| Standardised to the Corsa mix | 37.4% | 21.5% | 1.74 |
| Mantel-Haenszel pooled | | | **1.62** |

The claim holds: matched on age, mileage and fuel, a Corsa fails about 60% more often (1.59 to 1.74
by weighting, 1.62 pooled). The raw gap is smaller, 39%, because 3 Series cover more miles, so
matching widens the gap rather than closing it.

## Caveats

- Ten weeks of 2023 (the first 8 million rows of about 40 million), not the whole year, and winter
  tests only. A full-year run is the same two scripts with a bigger row cap.
- PRS counted as a fail, as DVSA counts initial failures; counting F alone would lower both rates.
- "3 Series" is every BMW model string starting with three digits beginning 3 (318, 320d, 330e and so
  on); a few may be mis-typed models.
