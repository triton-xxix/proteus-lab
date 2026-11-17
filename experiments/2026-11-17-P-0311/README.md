# P-0311: the ensemble bands moved up 1.0 C

**Question.** P-0310 (3 Nov) found the ICON-EPS and ECMWF lead-1 10-90 bands for the Muenchen-Stadt high
caught 3 of 11 days, every miss above. Does moving both bands up 1.0 C bring capture near the 80% a
calibrated band holds?

**Method.** `score_shifted.py` reads `exchange/icon_eps_band.jsonl` and `exchange/ecmwf_ens_band.jsonl`
against DWD 03379 highs (last obs 16 Nov; bands scored through 14 Nov), unshifted and +1.0 C. The +1.0 was
picked on 3 Nov from days up to 2 Nov, so days from 3 Nov are out of sample for it (22 band-days).
A 0.0 to 3.0 C shift grid on all days is saved for the record; that grid is in sample.

**Numbers** (results.json).

| | n | unshifted inside | +1.0 inside |
|---|---|---|---|
| ICON-EPS, all | 17 | 9 (53%) | 9 (53%) |
| ECMWF, all | 16 | 6 (38%) | 10 (63%) |
| Pooled, all | 33 | 15 (45%) | 19 (58%) |
| Pooled, from 3 Nov (out of sample) | 22 | 12 (55%) | 13 (59%) |

- Out of sample the shifted misses are **0 above, 9 below**: the shift overcorrects. The warm bias shrank
  after 3 Nov (median obs minus p50: ICON +0.5 all, +0.3 from 3 Nov; ECMWF +0.95 all, +0.6 from 3 Nov).
- Best in-sample shift on the grid: +0.9 C, 61%. No shift reaches 80%.
- Median band width 1.24 C (ICON), 1.32 C (ECMWF).

**Reading.** The bands are too narrow, not just cold. Fixing the centre buys 4 to 12 points; the other
20-odd points of capture need a wider band. P-0310's 3 of 11 was the worst stretch of a bias that then
eased, which is why the unshifted rate climbed from 27% to 45% with more days.

**Called shot.** works at 0.55, "shifted about 50% v unshifted about 25%, still under 80". Shifted 58% and
under 80 as called; unshifted 45%, not 25%, so the comparison half of the number missed.

**Not done.** Widening the band (scale p10-p90 about p50) and testing that out of sample; queued as a
deepen at the 40-day mark. No new forecast pull.
