# P-0331: which defects carry the Corsa v 3 Series MOT gap? (5 Nov 2026)

P-0326 found a Corsa fails its MOT about 1.6 times as often as a 3 Series of the same age, mileage
and fuel. This splits that gap by defect section.

## What I ran

`defects.py`: P-0326's 268,323 tests (1 Jan to 6 Mar 2023, same filters and strata), DVSA's
`dft_test_item_2023.zip` streamed whole (460 MB, 89,302,632 item rows), rows kept for those test
ids where the item is a failure (F) or fixed at the station (P). Each item's section comes from
`lookup.zip` (item_detail's section id named from item_group). Join check: 90,677 tests have a
failure item, exactly P-0326's 66,009 + 24,668 initial fails. Each car's share of tests failing in a
section is standardised to the 3 Series mix of age, mileage and fuel. `defects.json` has every
section; `defects-hits.json` is the joined test-to-section list.

## Result

| Section | Corsa | 3 Series | Ratio | Share of the gap |
|---|---|---|---|---|
| Suspension | 16.2% | 6.5% | 2.5x | 27% |
| Lamps, reflectors and electrical | 19.4% | 9.9% | 2.0x | 26% |
| Body, chassis, structure | 6.2% | 1.2% | 5.1x | 14% |
| Visibility | 8.3% | 4.0% | 2.1x | 12% |
| Brakes | 9.8% | 6.9% | 1.4x | 8% |
| Steering | 3.2% | 0.5% | 5.9x | 7% |
| Noise, emissions and leaks | 5.3% | 3.0% | 1.8x | 7% |
| Tyres | 8.3% | 7.7% | 1.1x | 2% |
| Road wheels | 0.4% | 1.2% | 0.3x | -2% |

(Share: each section's difference over the sum of differences; a test can fail in several sections.)

**Verdict: suspension and lamps carry half the gap; tyres carry almost none.** The sections that
track how a car is kept (tyres, seat belts) are level between the two. The gap sits in the parts
that wear with the build: suspension, body and chassis (5x) and steering (6x). The 3 Series fails
more only on road wheels.

## Caveats

Ten winter weeks of 2023, two models, as P-0326. "Lamps" includes bulbs a driver could have
changed, so part of that row is upkeep rather than build. Steering at 3.2% against 0.5% is a large
ratio on a small base.
