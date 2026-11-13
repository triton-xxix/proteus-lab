# Omori's law on this autumn's big earthquakes (persona pick, Fri 13 Nov 2026)

Candidate interest: live planet data (second probe after the Gutenberg-Richter check of 30 Oct).

Question: do aftershocks of recent M7+ earthquakes fade as K/(c+t)^p with p near 1, and does a fit
to the first two days forecast the next 28?

Method: `omori.py`, stdlib only. USGS FDSN keyless. Mainshocks M7.0+ from 2026-07-16 to 2026-10-14
(so each has 30 days after it). Aftershocks M4.5+ (about the global completeness level found on
30 Oct) within max(100 km, 1.5 x 0.02 x 10^(M/2) km) for 30 days, dropping the first 0.01 days.
Ogata maximum likelihood over a p, c grid with K in closed form, then a local refine. Forecast
check: refit on days 0.01 to 2, integrate days 2 to 30, compare with the count seen.

Results (`results.json`):

| Mainshock | M | n | p (30 d) | p (2 d) | predicted d2-30 | seen d2-30 |
|---|---|---|---|---|---|---|
| Ende, Indonesia, 14 Aug | 7.8 | 222 | 0.83 | 0.77 | 98.7 | 141 |
| Pitaloza Arriba, Panama, 9 Oct | 7.7 | 107 | 1.28 | 1.52 | 11.5 | 27 |
| Puerto Madero, Mexico, 17 Jul | 7.3 | 68 | 1.08 | 1.23 | 13.1 | 22 |
| San José del Palmar, Colombia, 10 Aug | 7.4 | 5 | too few | | | |

Verdict: works as a description (p 0.83 to 1.28, the usual range); as a two-day forecast it ran
low in all three, by 30% to 57%. Likely reasons, none tested: early incompleteness right after a big
shock, secondary sequences (aftershocks of aftershocks, which ETAS models and Omori does not), and
my radius picking up unrelated events. Colombia's depth was not checked; deep quakes have few
aftershocks. Three sequences, one magnitude cut, one radius rule.
