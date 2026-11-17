# P-0462: USGS's own aftershock forecasts, scored on days 2 to 30

**Question.** P-0455 found that my two-day ETAS fit explodes and my Omori fit under-calls days 2 to 30.
USGS publishes an operational aftershock forecast (`oaf`) with its fitted parameters. With those
parameters fixed, how near does the forecast land?

**Method.** `oaf.py`. ComCat lists 5 M7+ events since 1 Nov 2025 with an oaf product (keyless
`fdsnws/event/1/query?producttype=oaf`). For each, every oaf version (`includesuperseded=true`); the
latest issued within 2 days of the mainshock is the **day-2 forecast**, made before the window it is
scored on. The current version is scored too, but it was refitted on the sequence and is in sample.
Expected count above Mc in the oaf's own circle, days 2 to 30, from the Reasenberg-Jones rate
`10^(a + b(Mmain - Mc)) (t + c)^-p`, against the ComCat count in the same circle and magnitude.

**Numbers** (results.json).

| event | M | day-2 issued | day-2 expected | current expected | observed | day-2 ratio |
|---|---|---|---|---|---|---|
| Panama | 7.7 | +45.9 h | 8.0 | 4.5 | 6 | 0.75, inside 2x |
| Ende, Indonesia | 7.8 | +46.0 h | 11.0 | 38.1 | 42 | 3.8, under-called |
| Colombia (116 km deep) | 7.4 | +26.6 h | 15.5 | 12.8 | 4 | 0.26, over-called |
| Venezuela | 7.5 | +46.6 h | 13.5 | 10.1 | 5 | 0.37, over-called |
| Hubbard Glacier, Alaska | 7.0 | | | | | not scored: AK's oaf uses `Mcat`, not `Mc` |

- **Day-2 forecast within a factor of 2: 1 of 4.** In-sample current version: 2 of 4.
- Two of the three day-2 misses were **over-calls** (Colombia, Venezuela). My own Omori fits in P-0455
  under-called 5 of 6. USGS's Bayesian blend leans on generic regional priors, which pull small
  early sequences up; mine follow the two-day data down.
- The deep Colombia event (116 km) gave 4 against 15.5: deep quakes are known to be aftershock-poor,
  and the day-2 parameters did not know it yet.

**Called shot.** works at 0.60, "3 of 5 within a factor of 2". Measured 1 of 4 scored. Missed.

**Not done.** The Alaska event's parameters (a model with `Mcat` and F, G, H terms) not decoded.
No probabilistic score (the oaf gives ranges; only the point count is used). No check that ComCat is
complete at Mc in each region. Not overlapped with P-0455's own six events (different set: P-0455 took
M7+ from April 2026 by its own query; none of its rows carry ids).
