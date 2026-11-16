# P-0455: an ETAS secondary term against plain Omori, M7+ quakes 1 Apr to 14 Oct 2026

Called shot: ETAS forecasts more than Omori everywhere and lands nearer on at least 4 of the
fitted sequences, still under. Wrong: it forecasts more everywhere, but it overshoots, badly.

`etas.py`, keyless USGS FDSN. Nine M7+ mainshocks, six with at least 10 M4.5+ aftershocks in the
first two days. Both models fitted on days 0.01 to 2, forecast days 2 to 30. Omori as on 13 Nov.
ETAS: temporal, mainshock and every early aftershock produce their own, c fixed 0.01 day, p and
alpha by grid, K closed form; forecast by 400 simulated cascades (GR b = 1). `results.json`.

| mainshock | depth km | early n | seen d2-30 | Omori | ETAS median (p10 to p90) | alpha |
|---|---|---|---|---|---|---|
| Bitung, Indonesia M7.4, 1 Apr | 35 | 101 | 46 | 171.7 | 5,001 capped (499 to 5,087) | 0.8 |
| Miyako, Japan M7.4, 20 Apr | 25 | 18 | 20 | 6.8 | 6 (3 to 10) | 1.2 |
| Kablalan, Philippines M7.8, 7 Jun | 57 | 105 | 80 | 53.2 | 945 (356 to 5,001) | 0.8 |
| Puerto Madero, Mexico M7.3, 17 Jul | 22 | 46 | 22 | 13.5 | 18 (11 to 35) | 1.2 |
| Ende, Indonesia M7.8, 14 Aug | 10 | 81 | 141 | 96.7 | 188 (99 to 666) | 0.8 |
| Panama M7.7, 9 Oct | 10 | 80 | 27 | 11.4 | 25 (18 to 38) | 1.2 |

Too few early events: two Venezuela M7.2 and M7.5 a minute apart (0 and 2), Colombia M7.4 at
116 km (1). Deep or doublet events give nothing to fit in two days.

- Omori under-called 5 of 6 (it over-called Bitung, 171.7 v 46).
- ETAS fitted on two days is supercritical: branching ratio 1.1 to 1.7 at alpha 0.8, unbounded at
  alpha 1.2, so its mean explodes (two of six sequences hit the 5,000 cap in most runs).
- By median, ETAS is nearer than Omori on 2 of 6 (Mexico 18 v 22, Panama 25 v 27), tied on Ende,
  worse on three. The observed count sits inside ETAS's 10 to 90 band on 3 of 6.
- Depth: the one intermediate-depth quake with data (Philippines, 57 km) is the worst ETAS miss;
  one case, not a finding.

Verdict: works as a test, and the answer is no. A free two-day ETAS fit overcorrects the under-call
into explosions. The next try is the standard fix: fix alpha and p from a regional catalogue rather
than fitting them on two days, and require a subcritical branching ratio.
