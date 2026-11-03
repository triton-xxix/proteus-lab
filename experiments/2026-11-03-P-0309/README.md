# P-0309: ECMWF IFS lead curve at Munich, beside ICON

**Question.** P-0293 and P-0307 measured ICON only. Does ECMWF IFS (0.25 deg) lose skill more slowly at
leads 3 to 6, where ICON's +1.0 hit falls away?

**Method.** One keyless previous-runs call (`models=ecmwf_ifs025`, 48.1374, 11.5755, hourly, 1 Sep to
31 Oct 2026, timezone Europe/Berlin, `temperature_2m` and `_previous_day1` to `_day6`), saved to
`sandbox/om-prevruns-munich-ifs-lead0-6.json`. The grid point came back 48.25, 11.5 (about 13 km NNW of
the city). `lead_curve.py` is P-0293's against DWD 03379 Muenchen-Stadt, 61 days, 0 nulls at every lead,
plus a least-squares slope of sd on lead for both models. (The `utc_offset_seconds` of 3600 is the
offset now, in November; the hourly times are local with DST, so the day boundary is right.)

**Numbers.**

| lead | IFS bias | IFS sd | IFS hit +1 | IFS hit at its own bias | ICON bias | ICON sd | ICON hit +1 |
|---|---|---|---|---|---|---|---|
| 0 | +1.98 | 1.15 | 25% | 39% | +0.66 | 0.68 | 59% |
| 1 | +1.96 | 1.38 | 16% | 41% | +0.83 | 1.32 | 39% |
| 2 | +2.01 | 1.35 | 20% | 26% | +1.00 | 1.35 | 39% |
| 3 | +2.08 | 1.66 | 15% | 20% | +1.18 | 1.78 | 30% |
| 4 | +1.95 | 1.79 | 26% | 18% | +1.10 | 2.21 | 28% |
| 5 | +1.75 | 2.69 | 12% | 15% | +1.09 | 2.64 | 16% |
| 6 | +1.61 | 3.27 | 21% | 16% | +1.12 | 2.74 | 13% |

sd slope per day of lead: **IFS +0.336, ICON +0.346**.

**Reading.** IFS does not hold up better at long leads: its error spread grows at the same rate as
ICON's, and at the same leads its sd is no smaller (bigger at 0, 5 and 6). It runs twice as cold as
ICON (+2.0 against the city station, partly the coarser grid and the point 13 km out), so the +1.0
correction is wrong for it; even at its own in-sample bias its day-before hit (41%) only matches ICON's
39% at +1.0, and below lead 2 it is worse. For the exchange book's day-high calls, ICON stays the model.

**Called shot.** works at 0.75, "IFS sd grows about +0.3 a day (ICON +0.4)". Hit: +0.336, and ICON's
fitted slope is +0.346, not the +0.4 I had read off by eye.

**Not done.** IFS at the airport point, the 9 km HRES (`ecmwf_ifs` if served), a blend of the two
models, more than one autumn.
