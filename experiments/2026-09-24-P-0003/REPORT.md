# P-0003: Pinnacle closing as the line to beat

Saved walk-forward probabilities from `pitch/backtest/predictions.csv`, no refit. Pool weight is the in-sample
log-opinion-pool weight the model earns against the named line (same `best_weight` as the harness).

Coverage of Pinnacle closing columns by league and season:

| div | season | matches | with PSCH |
|---|---|---|---|
| D1 | 2425 | 304 | 304 |
| D1 | 2526 | 305 | 148 |
| D1 | 2627 | 34 | 0 |
| E0 | 2425 | 380 | 380 |
| E0 | 2526 | 380 | 210 |
| E0 | 2627 | 50 | 0 |
| E1 | 2425 | 549 | 549 |
| E1 | 2526 | 550 | 269 |
| E1 | 2627 | 93 | 0 |
| F1 | 2425 | 305 | 305 |
| F1 | 2526 | 305 | 152 |
| F1 | 2627 | 44 | 0 |
| I1 | 2425 | 377 | 377 |
| I1 | 2526 | 379 | 197 |
| I1 | 2627 | 50 | 0 |
| N1 | 2425 | 304 | 304 |
| N1 | 2526 | 305 | 141 |
| N1 | 2627 | 62 | 0 |
| P1 | 2425 | 305 | 305 |
| P1 | 2526 | 304 | 151 |
| P1 | 2627 | 61 | 0 |
| SC0 | 2425 | 228 | 228 |
| SC0 | 2526 | 228 | 54 |
| SC0 | 2627 | 41 | 0 |
| SP1 | 2425 | 379 | 379 |
| SP1 | 2526 | 378 | 186 |
| SP1 | 2627 | 66 | 0 |

## E0 season 2425 (n=380 with all three closing lines)

| line | Brier | RPS | log loss |
|---|---|---|---|
| avg close | 0.5752 | 0.1961 | 0.9667 |
| pinnacle close | 0.5751 | 0.1961 | 0.9664 |
| max close | 0.5753 | 0.1962 | 0.9665 |
| model dc | 0.5854 | 0.2009 | 0.9800 |
| model elo | 0.6113 | 0.2124 | 1.0187 |
| model sot | 0.5813 | 0.1992 | 0.9755 |

| model | wt vs avg close | wt vs pinnacle close | wt vs max close |
|---|---|---|---|
| dc | 0.11 | 0.11 | 0.11 |
| elo | 0.00 | 0.00 | 0.00 |
| sot | 0.14 | 0.14 | 0.15 |

## E0 season 2526 (n=210 with all three closing lines)

| line | Brier | RPS | log loss |
|---|---|---|---|
| avg close | 0.5884 | 0.1982 | 0.9836 |
| pinnacle close | 0.5911 | 0.1994 | 0.9875 |
| max close | 0.5878 | 0.1980 | 0.9818 |
| model dc | 0.6114 | 0.2084 | 1.0194 |
| model elo | 0.6144 | 0.2098 | 1.0234 |
| model sot | 0.6070 | 0.2065 | 1.0138 |

| model | wt vs avg close | wt vs pinnacle close | wt vs max close |
|---|---|---|---|
| dc | 0.00 | 0.00 | 0.00 |
| elo | 0.00 | 0.00 | 0.00 |
| sot | 0.00 | 0.00 | 0.00 |

## E0 season 2627: 0 matches with all three closing lines, too few

## E0 all seasons (n=590 with all three closing lines)

| line | Brier | RPS | log loss |
|---|---|---|---|
| avg close | 0.5799 | 0.1968 | 0.9728 |
| pinnacle close | 0.5808 | 0.1972 | 0.9739 |
| max close | 0.5798 | 0.1968 | 0.9720 |
| model dc | 0.5946 | 0.2036 | 0.9940 |
| model elo | 0.6124 | 0.2115 | 1.0203 |
| model sot | 0.5904 | 0.2018 | 0.9891 |

| model | wt vs avg close | wt vs pinnacle close | wt vs max close |
|---|---|---|---|
| dc | 0.00 | 0.00 | 0.00 |
| elo | 0.00 | 0.00 | 0.00 |
| sot | 0.00 | 0.00 | 0.00 |

## all nine leagues, all seasons (n=4639 with all three closing lines)

| line | Brier | RPS | log loss |
|---|---|---|---|
| avg close | 0.5767 | 0.1947 | 0.9689 |
| pinnacle close | 0.5765 | 0.1947 | 0.9686 |
| max close | 0.5764 | 0.1946 | 0.9681 |
| model dc | 0.6011 | 0.2054 | 1.0083 |
| model elo | 0.5961 | 0.2033 | 0.9976 |
| model sot | 0.5925 | 0.2016 | 0.9932 |

| model | wt vs avg close | wt vs pinnacle close | wt vs max close |
|---|---|---|---|
| dc | 0.00 | 0.00 | 0.00 |
| elo | 0.00 | 0.00 | 0.00 |
| sot | 0.00 | 0.00 | 0.00 |


## What this says

- Swapping the line changes nothing. Pinnacle's close, the average close and the max close sit within 0.001 Brier of each other on E0 and on all nine leagues, and every model earns the same pool weight against all three (E0 2024-25: dc 0.11, sot 0.14, elo 0.00; everywhere else 0.00). The harness's verdict of no edge does not depend on which closing price it uses.
- Pinnacle cannot be the live line anyway: football-data's cache has no PSCH for any 2026-27 match and for only 210 of 380 E0 matches in 2025-26 (similar in every league). The average close is present on all of them.
- The E0 2024-25 in-sample weights of 0.11 and 0.14 are the same in-sample numbers the harness already reports; its out-of-sample check on the other season takes them to zero. No new claim here.
- Verdict: not worth it. Keep the average close as the line to beat. Struck from the "next in the harness" list in the backlog.
