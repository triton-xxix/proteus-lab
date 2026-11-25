# D-020: Munich day-ahead bands, ECMWF IFS ensemble against ICON-EPS, read 25 Nov 2026

Registered 28 Oct (`experiments/2026-10-28-P-0249/README.md`): at 20 scored days each, which raw 10 to
90 band holds the DWD Stadt high (station 10865) nearer 80%, and each one's share above its band.
Read on its backstop from the two capture scripts' own `score` output in tonight's nightly
(observations to 23 Nov).

| band | scored days | inside raw | inside +0.5 C | above band |
|---|---|---|---|---|
| ICON-EPS (P-0232) | 24 | 12 (50%) | 13 (54%) | 10 (42%) |
| ECMWF IFS ens (P-0249) | 23 | 8 (35%) | 8 (35%) | 13 (57%) |

Answer: ICON-EPS is nearer 80%, by 15 points, and both are far short of it. Both miss mostly on the
warm side: the high landed above the band on 42% and 57% of days, so neither band is fit to price a
degree from as it stands, and a flat +0.5 C barely moves either. This matches P-0309 (IFS runs about
2 C cold at its grid point) and P-0310's first six days.

What follows: P-0561 (queued tonight) tries the order from arXiv 2610.42130, each band shifted by its
own leave-one-out past miss, then pooled. No call rule changes from this read; calls stay on ICON
seamless alone as `tasks/nightly.md` says.
