# P-0387: is ICON's Munich point forecast inside its own ensemble band? (9 Nov 2026)

On 9 Nov the deterministic ICON high for 10 Nov read 10.1 C while the ICON-EPS 10 to 90 band said 8.28 to 9.52. `band.py` asks whether that is usual, using the 13 band days captured in `exchange/icon_eps_band.jsonl`, the lead-1 point from Open-Meteo previous-runs, and the EDDM METAR high on the 12 that have settled.

- The point sat outside the band on 3 of 13 days (2 above, 1 below). A random member would fall outside about 20% of the time, so 23% is not unusual. Tonight's 10.1 against 9.52 is the same kind of day.
- Against the METAR high, MAE was point 0.82, band median 0.80, control member 1.06. The point and the median are a coin toss (point closer on 5, median closer on 6, one tie).
- On the 3 outside days, the median was closer on 2 and the point on 1. That is too few to lean on.
- The METAR high fell inside the 10 to 90 band on 6 of 12 days, against the 80% a calibrated band would hold. It is whole degrees and the band is narrow, about 1.2 C wide at the moment, so some of this is the rounding.
- Mean METAR minus point was -0.49 C on these 12 days. That does not agree with P-0335's +0.03 C at lead 1 over 24 days. These 12 days overlap P-0335's only in part and 12 days is few, so I am not changing tonight's rule on it, but it should be looked at again as a re-check with the same day set.

Limits: 13 days, one point, one autumn; the band was captured at about 23:25 UTC the night before and the previous-runs "day 1" value is a slightly different cycle. No call was changed by this.
