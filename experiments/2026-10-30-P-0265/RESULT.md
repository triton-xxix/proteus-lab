# P-0265 result

BTCUSDT daily closes, Binance spot, 2017-08-17 to 2026-10-29, 3361 days. Fee 0.10% a side.

| window | rule | multiple | CAGR | max DD | trades | hold multiple | hold CAGR | hold max DD | rule minus hold (CAGR) |
|---|---|---|---|---|---|---|---|---|---|
| all | 20/50 | 16.24x | +36.0% | 75% | 74 | 18.15x | +37.7% | 83% | -1.7 pts |
| all | 10/30 | 26.26x | +43.1% | 64% | 128 | 21.06x | +39.6% | 83% | +3.4 pts |
| all | 50/200 | 4.31x | +18.4% | 67% | 19 | 6.77x | +24.7% | 77% | -6.3 pts |
| last 3 years | 20/50 | 2.02x | +26.3% | 39% | 26 | 2.26x | +31.2% | 53% | -4.9 pts |
| last 3 years | 10/30 | 1.51x | +14.6% | 38% | 44 | 2.26x | +31.2% | 53% | -16.6 pts |
| last 3 years | 50/200 | 1.67x | +18.5% | 40% | 7 | 2.26x | +31.2% | 53% | -12.7 pts |
| last 1 year | 20/50 | 1.06x | +5.6% | 24% | 8 | 0.71x | -29.2% | 47% | +34.8 pts |
| last 1 year | 10/30 | 0.86x | -14.2% | 20% | 14 | 0.71x | -29.2% | 47% | +15.0 pts |
| last 1 year | 50/200 | 0.85x | -15.1% | 18% | 3 | 0.71x | -29.2% | 47% | +14.1 pts |

Rule: long when SMA(fast) > SMA(slow) at the close, else cash, filled at the next close. Hold pays the fee once at entry.
