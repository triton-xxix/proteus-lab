# P-0391: ICON lead-1 bias on the METAR high at four continental airports

**Question.** P-0383 put ICON's lead-1 METAR-high bias at +0.4 to +0.6 C at two UK airports; P-0387 read
Munich at -0.49 on 12 days. At EDDM, EHAM, LFPG and LEMD on the same 61 days (1 Sep to 31 Oct 2026),
which is it, and does any sit outside 2 se of zero?

**Shot.** works at 0.80: median of the four lead-1 biases about +0.3 C, two of four outside 2 se.

**Method.** `four.py`, P-0383's method: Iowa State keyless METAR archive (routine and special, whole
degrees, at least 12 reports a day, UTC days) against Open-Meteo previous-runs `icon_seamless` at each
airport's coordinates, hourly maxed per UTC day. Mean METAR minus forecast. 8 calls, raw pulls saved.

**Numbers** (results.json), METAR minus ICON, 61 days each:

| Airport | lead 0 mean (se) | lead 1 mean (sd, se) |
|---|---|---|
| EDDM Munich | +0.22 (0.06) | +0.41 (1.40, 0.18) |
| EHAM Amsterdam | +0.12 (0.06) | +0.23 (0.67, 0.09) |
| LFPG Paris CDG | +0.70 (0.07) | +0.88 (1.15, 0.15) |
| LEMD Madrid | +0.53 (0.08) | +1.00 (1.28, 0.16) |

Median of the four at lead 1 is +0.65, against my +0.3: a miss on the number. All four sit outside 2 se,
not two. Every airport has ICON cold on the METAR high, as at both UK airports; the range +0.23 to +1.00
brackets the UK's +0.41 and +0.58.

**Munich.** +0.41 here on 61 days at the airport grid point, against P-0387's -0.49 on 12 days. Different
day set and, I think, a different forecast point (P-0387 read the city point 48.137, 11.575 against
EDDM's METAR, 28 km apart). Not settled here; queued as a deepen.

**Caveats.** METAR whole degrees; UTC days; one model; two months of autumn.

**Not done.** No change to the exchange book's correction; that is a desk call, not a probe's.
