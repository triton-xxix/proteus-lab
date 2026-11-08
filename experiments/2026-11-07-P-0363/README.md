# P-0363: do Heathrow's :50 METARs behave like the :20s?

P-0352 matched only half of October's 1,488 EGLL METARs to a 10-minute SYNOP minute, and P-0353 found the cache
has no :50 SYNOPs. Refill 118 checked Ogimet itself: 20 Oct 2026 has 115 reports for 03772 at :00 to :40 and none
at :50, so they are absent at source, not dropped by the fetch. This sets each :50 METAR against the mean of the
:40 and next :00 tenths, with a control at :20 that measures what interpolating costs.
`interp.py`, `results.json`; METARs from Iowa Mesonet (one curl), SYNOPs from P-0352's cache.

| | n | METAR equals rounded tenths | mean METAR minus tenths | sd |
|---|---|---|---|---|
| :20, exact minute (P-0352's set) | 738 | 66.5% | -0.02 C | 0.56 |
| :20, interpolated from :10 and :30 | 703 | 66.6% | -0.04 C | 0.55 |
| :50, interpolated from :40 and :00 | 738 | 67.2% | -0.01 C | 0.55 |

Interpolating costs almost nothing: at :20 the mean of :10 and :30 sits 0.007 C from the exact reading (sd 0.18,
86% within 0.2 C). And the :50s behave like the :20s, so P-0352's finding (rounded about two thirds of the time,
no bias, a different sample of the air rather than truncation) now holds on 1,476 of 1,488 METARs, not half.

A trap found on the way: Iowa Mesonet files Heathrow's :50 METARs as report type 3 and the :20s as type 4, so a
request for type 3 alone returns 745 reports with only one at :20. The first run here did that. (The output key
`metars_routine` counts both types; the name is a leftover.)

October only, one station, whole-degree METARs against tenths.

Called shot (not committed; the nightly does not commit shots): :50 rate within 3 points of :20. Hit (0.7).
