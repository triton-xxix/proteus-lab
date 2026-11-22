# P-0530: the London minus Scotland MOT gap with the car held fixed

P-0522 found cars first used 2015 to 2019 passing at 89.5% in London's inner postcode areas and 79.9%
in Scotland (pass including PRS), a 9.6 point gap. Is that the cars (mix of makes and models) or the
place (testing, roads, weather)? Refill row 219.

## Method

`fixed.py`, keyless. P-0522's own helpers (loaded from its `sample.py` without running its main) and
the same sample: three 2024 monthly members of the DVSA results zip, first 40 MB of each, by S3 byte
ranges. Class 4 normal tests, first use 2015 to 2019, London and Scotland only, results P, F and PRS.

- The gap for all cars, then for the three make-model pairs with the most tests across both regions.
- PRS (failed, fixed at the station, passed) shown separately, so the gap is given P only and P plus PRS.
- A mix-adjusted gap: London's rate per make-model weighted by Scotland's mix, over pairs with 30 or
  more tests in each region.

## Numbers

See results.json and the verdict line.

## What I did not do

No mileage control (Scottish cars may run further), no full year (a 40 MB head of three months), no
test-station effect beyond PRS. Model strings are DVSA's raw text, not cleaned.
