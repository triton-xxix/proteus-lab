# P-0447: the low-cloud flag at Heathrow and Paris

**Question.** P-0446 found that a BKN, OVC or VV layer at or below 500 ft in an EDDM METAR before 10Z marked
days when ICON lead 1 ran about 1.07 C warm on the Munich day high. Does the same flag work at EGLL and LFPG,
and does it pass a within-month permutation at all three?

**Method.** `stations.py`. Iowa State METAR day highs (40+ reports), Open-Meteo previous-runs
`icon_seamless` lead 1 at each airport point (EDDM at the city point, as before), UTC days, 1 Nov 2025 to
31 Oct 2026. Flag shuffled within calendar month 10,000 times, one-sided.

**Called shot.** works at 0.65; EGLL gap -0.6 C, both new stations negative with p under 0.05.

## Numbers

| station | flagged days | flagged mean err | other mean err | gap | perm p | 2.5 C+ warm misses caught |
|---|---|---|---|---|---|---|
| EGLL | 48 (13%) | -0.14 | +0.32 | **-0.45** | 0.0032 | 2 of 4 |
| LFPG | 58 (16%) | +0.12 | +0.59 | **-0.47** | 0.0001 | 1 of 3 |
| EDDM | 67 (18%) | -0.70 | +0.37 | **-1.06** | 0.0010 | 9 of 17 |

## What it means

The flag travels: all three airports show the forecast running warmer on low-cloud mornings, each past a
within-month permutation. At Heathrow and Paris the shift is under half Munich's (-0.45 and -0.47 against
-1.06), and those two rarely have big warm misses at all (4 and 3 in a year against 17), so the flag matters
most where ICON is worst, inland Munich. The direction hit my shot; EGLL came in at -0.45 against the -0.6 I
called.

## What I did not do

- In-sample only for EGLL and LFPG (no held-out window).
- No market: whether a 0.5 to 1 C shift crosses a bucket edge often enough to pay is not tested here.
- The 500 ft and 10Z cut-offs were set from one Munich day (9 Nov) and not tuned or varied.
