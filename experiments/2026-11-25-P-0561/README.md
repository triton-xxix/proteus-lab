# P-0561: bias-correct, then pool, the Munich ICON-EPS and ECMWF bands

Nightly 25 Nov 2026 (second run on the date), desk probe from the night's read-it item (arXiv 2610.42130:
calibrate each source, blend, recalibrate). D-020 closed this morning with both raw 10 to 90 bands too
narrow and cold (ICON-EPS 50%, ECMWF 35% inside on their backstop).

Called shot: past-only shifts bring each band nearer 80%, and the shifted union lands about 60 to 75%
inside, best of the variants. The union part was right; it did better than called (79%).

## What I ran

`pool.py` on the 24 days scored in both `exchange/icon_eps_band.jsonl` and `exchange/ecmwf_ens_band.jsonl`
(29 Oct to 24 Nov), against the same DWD 03379 daily highs the capture scripts score with. A band's shift
is its own mean miss (observed minus p50). **past** uses only earlier days (at least 5), which is what I
could have used that night; **loo** uses every other day, future included, so it is an upper bound.
The "recalibrate" step widens the mean of the shifted bands by the smallest factor that put 80% of
earlier days inside.

## Result (`results.json`)

Mean miss over the 24 days: ICON +0.63°C, ECMWF +1.11°C (both cold, as D-020 found).

| band | past-only (19 days) | width | leave-one-out (24) | width |
|---|---|---|---|---|
| raw ICON-EPS | 10, 53% | 1.26°C | 11, 46% | 1.24 |
| raw ECMWF | 7, 37% | 1.49 | 8, 33% | 1.45 |
| shifted ICON | 12, 63% | 1.26 | 14, 58% | 1.24 |
| shifted ECMWF | 11, 58% | 1.49 | 13, 54% | 1.45 |
| **union of shifted** | **15, 79%** | **2.17** | **19, 79%** | **2.08** |
| mean of shifted | 11, 58% | 1.38 | 13, 54% | 1.35 |
| mean, recalibrated | 11 of 14, 79% | 2.76 | 16 of 19, 84% | 3.14 |

## Verdict: works

Shifting alone fixes only about a third of the gap; the spread is the bigger problem. Averaging the
shifted bands keeps them as narrow as either and gains nothing. Their union reaches 80% coverage at about
2.1 to 2.2°C wide, while the paper's blend-then-recalibrate order needs 2.8 to 3.1°C for the same
coverage, so on this data the union is the efficient one. But 19 days is thin and the shifts were fitted
on the same season, so this is in-sample. Forward test registered below and in `DUE.md` (D-035). Nothing
changes in how calls are made until it is read.

## Pre-registered forward test (D-035, written 25 Nov 2026 before any target day exists)

- Target days: every day from 2026-11-26 that both band files capture and DWD 03379 has observed, until
  20 such days are scored.
- Band: the union of ICON-EPS and ECMWF 10 to 90 bands, each shifted by its own mean miss over all earlier
  scored days (past-only, exactly `pool.py`'s `past` mode), scored by `pool.py --forward`.
- Pass: 14 to 18 of 20 inside (70 to 90%). Below 14 is a fail (still too narrow); above 18 is a fail too
  (wider than it needs to be).
- Reported beside it, not scored: raw ICON-EPS and shifted ICON on the same days.
