# P-0451: BTC daily moves on FOMC and CPI days, 2023 to 15 Nov 2026

Called shot: yes for both, release-day mean |move| about 1.2x an ordinary day, pooled p under 0.10.

`release_days.py`, keyless: FOMC decision days from P-0227's parse of federalreserve.gov, CPI
release days from the BLS CPI archive page (bls.gov returns 403 to curl, so the Wayback copy),
BTCUSDT UTC daily candles from data-api.binance.vision. Move is |close/open - 1| on the release's
UTC day. Results in `results.json`.

| set | n | mean abs move | median | mean ratio v ordinary | perm p |
|---|---|---|---|---|---|
| ordinary days | 1,340 | 1.67% | 1.15% | | |
| FOMC | 31 | 1.99% | 1.41% | 1.19 | 0.16 |
| CPI | 45 | 1.80% | 1.34% | 1.08 | 0.31 |
| either | 75 | 1.89% | 1.34% | 1.13 | 0.15 |

By year the FOMC lift is 2023 and 2024 only (2.04% and 3.29% against 1.54% and 1.98%); in 2025
and 2026 FOMC days moved less than ordinary days (1.44% v 1.56%, 1.08% v 1.61%). CPI days ran a
little above ordinary in 2024 to 2026 and below in 2023.

Verdict: works as a measurement, and the called shot was half right. Release days are slightly
bigger, about 1.1x to 1.2x, but nothing clears p 0.10, and the FOMC effect has faded since 2025.
As a news filter on a daily bar it would skip about 5% of days for a lift that is mostly noise.
