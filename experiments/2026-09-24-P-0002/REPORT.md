# P-0002: the next binding gate after age

## 2026-09-22T00:38:11Z: 23 rows, 8 in the age window, 0 pass everything

| gate | pass among in-window | drop it alone, entries become |
|---|---|---|
| mint revoked | 8 / 8 | 0 |
| freeze revoked | 8 / 8 | 0 |
| liq >= 20k | 4 / 8 | 0 |
| vol24 >= 200k | 4 / 8 | 0 |
| vol1h >= 10k | 4 / 8 | 0 |
| top10 <= 30pct | 0 / 8 | 0 |
| holders >= 300 | 0 / 8 | 0 |
| lp >= 90pct | 8 / 8 | 0 |
| price present | 8 / 8 | 0 |

Rows failing exactly one gate: none

In-window vol_h1 median $46896, top quartile $133108; vol_h24 median $208491, top quartile $1501662.

## 2026-09-22T01:27:31Z: 94 rows, 20 in the age window, 0 pass everything

| gate | pass among in-window | drop it alone, entries become |
|---|---|---|
| mint revoked | 20 / 20 | 0 |
| freeze revoked | 20 / 20 | 0 |
| liq >= 20k | 9 / 20 | 0 |
| vol24 >= 200k | 11 / 20 | 0 |
| vol1h >= 10k | 10 / 20 | 0 |
| top10 <= 30pct | 0 / 20 | 0 |
| holders >= 300 | 0 / 20 | 0 |
| lp >= 90pct | 20 / 20 | 0 |
| price present | 20 / 20 | 0 |

Rows failing exactly one gate: none

In-window vol_h1 median $12323, top quartile $70615; vol_h24 median $270143, top quartile $1551098.

## 2026-09-22T01:50:27Z: 40 rows, 6 in the age window, 0 pass everything

| gate | pass among in-window | drop it alone, entries become |
|---|---|---|
| mint revoked | 6 / 6 | 0 |
| freeze revoked | 6 / 6 | 0 |
| liq >= 20k | 2 / 6 | 0 |
| vol24 >= 200k | 2 / 6 | 0 |
| vol1h >= 10k | 2 / 6 | 0 |
| top10 <= 30pct | 0 / 6 | 0 |
| holders >= 300 | 6 / 6 | 0 |
| lp >= 90pct | 0 / 6 | 0 |
| price present | 6 / 6 | 0 |

Rows failing exactly one gate: none

In-window vol_h1 median $0, top quartile $7281541; vol_h24 median $38, top quartile $99771534.

## 2026-09-22T22:24:01Z: 108 rows, 63 in the age window, 0 pass everything

| gate | pass among in-window | drop it alone, entries become |
|---|---|---|
| mint revoked | 63 / 63 | 0 |
| freeze revoked | 63 / 63 | 0 |
| liq >= 20k | 0 / 63 | 0 |
| vol24 >= 200k | 11 / 63 | 0 |
| vol1h >= 10k | 1 / 63 | 0 |
| top10 <= 30pct | 0 / 63 | 0 |
| holders >= 300 | 63 / 63 | 0 |
| lp >= 90pct | 62 / 63 | 0 |
| price present | 63 / 63 | 0 |

Rows failing exactly one gate: none

In-window vol_h1 median $0, top quartile $47; vol_h24 median $46387, top quartile $170378.

## 2026-09-23T22:24:20Z: 58 rows, 29 in the age window, 0 pass everything

| gate | pass among in-window | drop it alone, entries become |
|---|---|---|
| mint revoked | 29 / 29 | 0 |
| freeze revoked | 29 / 29 | 0 |
| liq >= 20k | 0 / 29 | 0 |
| vol24 >= 200k | 0 / 29 | 0 |
| vol1h >= 10k | 0 / 29 | 0 |
| top10 <= 30pct | 1 / 29 | 0 |
| holders >= 300 | 21 / 29 | 0 |
| lp >= 90pct | 24 / 29 | 0 |
| price present | 29 / 29 | 0 |

Rows failing exactly one gate: none

In-window vol_h1 median $0, top quartile $0; vol_h24 median $5, top quartile $132.

## 2026-09-24T07:32:26Z: 105 rows, 72 in the age window, 8 pass everything

| gate | pass among in-window | drop it alone, entries become |
|---|---|---|
| mint revoked | 72 / 72 | 8 |
| freeze revoked | 72 / 72 | 8 |
| liq >= 20k | 17 / 72 | 8 |
| vol24 >= 200k | 37 / 72 | 8 |
| vol1h >= 10k | 17 / 72 | 9 |
| top10 <= 30pct | 11 / 72 | 11 |
| holders >= 300 | 46 / 72 | 8 |
| lp >= 90pct | 61 / 72 | 8 |
| price present | 72 / 72 | 8 |

Rows failing exactly one gate: top10 <= 30pct 3, vol1h >= 10k 1

In-window vol_h1 median $74, top quartile $9483; vol_h24 median $242001, top quartile $958363.


## What this says

- Before the feed fix (22 and 23 Sep) nothing in the window passed liquidity, so no single gate was "next": the feed was the story, as the backlog said.
- On the fixed feed (24 Sep, 72 in-window rows) the next binding gate is **top-10 share <= 30 percent**: 11 of 72 pass it, dropping it alone lifts entries from 8 to 11, and 3 rows fail on it and nothing else.
- The $10k 1h volume gate is not it. Dropping it alone gives 9, and only 1 row fails on it alone. It co-fails with liquidity (17 of 72 pass each) on the same quiet pools.
- Rule unchanged. The top-10 figure now comes from rugcheck with the pool account excluded; whether 30 percent is right for pump tokens at 1 to 48 hours is a question for scored outcomes.
