# P-0006: do yesterday's new pools still trade?

**Verdict: works, and the answer is "under half, and barely".** Of 183 mints the Grinder first saw under a
day old (22 and 23 Sep scans), 83 (45%) show any 24h volume now, 23 (13%) at least $1k, 15 (8%) at least
$10k, and 30 (16%) traded in the last hour. The one-day-old cohort (29 mints from the 23 Sep 22:00 scan)
reads 48% / 21% / 10% / 10%. Only 4 of 108 first seen on the pump.fun curve are now on another dex.

Caveats I cannot close tonight: "not listed" means DexScreener's tokens endpoint returned no pair, which I
read as dead but did not prove; the median price ratio is over listed mints only, so it flatters survivors;
the 23 Sep cohort came from a feed with a median first-sight volume of $198, so it is weak by construction.
A proper number needs the day-long poller in P-0014 feeding a cohort, not the desk's scans.

Checked 2026-09-24 22:30 UTC, 7 DexScreener calls, errors [].

| first seen (scan hour UTC) | mints | still listed | any 24h volume | 24h vol >= $1k | 24h vol >= $10k | any 1h volume | median price now/then |
|---|---|---|---|---|---|---|---|
| 2026-09-22T00 | 18 | 15 | 15 (83%) | 5 (28%) | 2 (11%) | 6 (33%) | 0.260 |
| 2026-09-22T01 | 66 | 26 | 25 (38%) | 7 (11%) | 7 (11%) | 11 (17%) | 0.165 |
| 2026-09-22T22 | 70 | 29 | 29 (41%) | 5 (7%) | 3 (4%) | 10 (14%) | 0.929 |
| 2026-09-23T22 | 29 | 14 | 14 (48%) | 6 (21%) | 3 (10%) | 3 (10%) | 0.969 |
| all | 183 | 84 | 83 (45%) | 23 (13%) | 15 (8%) | 30 (16%) | 0.754 |

Median 24h volume at first sight by scan: 2026-09-22T00 $92170, 2026-09-22T01 $3710, 2026-09-22T22 $14442, 2026-09-23T22 $198
Price down 90% or more (or unlisted): 114 of 183.
Moved off the pump.fun curve to another dex: 4 of 108 first seen on pumpfun.
