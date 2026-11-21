# P-0522: the MOT "postcode lottery", checked against DVSA's own data

Claim (MOTFaults YouTube short, harvested 21 Nov 2026): cars built 2015 to 2019 pass 81.4% in
Scotland and 89.8% in London, 8.4 points between best and worst region.

## What I ran

`sample.py` reads DVSA's anonymised MOT results for 2024 (data.gov.uk, a 1.5 GB zip of twelve
monthly CSVs) without downloading it: it reads the zip's central directory by HTTP range request,
then streams the first 40 MB of three monthly members (Aug, Jun, Nov 2024) through raw inflate.
Filter: normal tests (`NT`), class 4 (cars), `first_use_date` 2015 to 2019. Region from the test
station's `postcode_area`: London is E, EC, N, NW, SE, SW, W, WC only (outer London areas such as
BR, CR, HA, IG fall in the rest of England); Scotland is the 16 Scottish areas, TD included.
Output `results.json`.

## Result (1,600,254 tests)

| Region | Tests | Pass first time (P) | Pass incl. fixed at station (P + PRS) |
|---|---|---|---|
| London (inner areas) | 61,037 | 83.94% | 89.48% |
| rest of England | 1,223,470 | 81.92% | 85.74% |
| North East | 69,218 | 80.32% | 84.16% |
| Wales | 82,187 | 78.96% | 83.08% |
| Scotland | 164,342 | 77.01% | 79.91% |
| All | 1,600,254 | 81.27% | 85.08% |

The video's numbers match the P + PRS definition: London 89.5% against its 89.8%, Scotland 79.9%
against its 81.4%. The ranking holds (London best, Scotland worst) and the gap is wider in my
sample, 9.6 points not 8.4. On first-time passes alone it is 6.9 points.

## Caveats

- A sample: the head of three monthly files, not the year. Files may be ordered by station or
  date, so the head is not random; the video's year (unstated) may differ.
- "London" by postcode area is not Greater London. Outer London would likely pull it down.
- Same cars is not quite true: region also changes the mix of makes, mileage and how often
  PRS (repair on the spot) is used, which is itself a station habit: London's PRS share is 5.5%
  of tests, Scotland's 2.9%. Half the London edge is garages fixing on the spot.

## Verdict

Works. The open data reproduces the claim's direction and size (9.6 v 8.4 points); the spread is
real, and a good part of it is a difference in how stations record repairs, not only in the cars.
