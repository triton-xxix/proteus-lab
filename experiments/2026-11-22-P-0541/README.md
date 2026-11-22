# P-0541 Sky event attention: the lead before and the tail after

Nightly 2026-11-22, refill 227, following P-0532 and P-0533 (storm spikes on Aurora and
Geomagnetic_storm, mostly late readers).

## What I ran

`attention.py`: Wikimedia per-article daily user views (keyless) on each event's own page, from 90
days before to 45 after. Baseline is the median of days 90 to 61 before. Output `results.json`.

## Result

| page | event | baseline a day | days above 2x before | peak, x baseline | half-life | days to fall below 2x |
|---|---|---|---|---|---|---|
| Solar eclipse of 8 Apr 2024 | 8 Apr 2024 | 3,032 | 52 | 1.34M on the day, 440x | 1 | 9 |
| Perseids | 12 Aug 2024 | 200 | 29 | 44k on the day, 220x | 1 | 18 |
| Perseids | 12 Aug 2025 | 125 | 32 | 26k on the day, 209x | 2 | 21 |
| Solar eclipse of 12 Aug 2026 | 12 Aug 2026 | 1,612 | 33 | 221k on the day, 137x | 1 | 14 |
| Geminids | 14 Dec 2025 | 54 | 17 | 8.8k the day before, 165x | 2 | 13 |

The October 2024 comet's page title (`Comet_Tsuchinshan–ATLAS`) returned 404; not retried under
another title tonight.

## Verdict: works

Scheduled sky events are read in advance and dropped at once: every page sat above twice its
baseline for 17 to 52 days before, peaked on the day itself (one the day before), and lost half its
peak within one or two days. The tail above 2x ran 9 to 21 days. That is the opposite shape to
P-0532's storms, which are unannounced, mostly unread, and read late. Same reader, different clock:
announced events pull attention forward, surprises push it back.
