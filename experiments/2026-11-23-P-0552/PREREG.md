# P-0552, Geminids 2026 attention forecast, pre-registered 23 Nov 2026

Committed before any December 2026 data exists. Source: Wikimedia REST pageviews, en.wikipedia, article `Geminids`, agent `user`, daily (keyless). Scorer: `score.py` in this folder, run on or after 16 Dec 2026.

## What the past three years did (pulled 23 Nov 2026, `history.json`)

| Year | November median | First day above 10x it | Peak day | Peak views | Moon at the peak |
|---|---|---|---|---|---|
| 2023 | 118.5 | 11 Dec | 14 Dec | 15,626 | new moon 13 Dec, dark |
| 2024 | 106.5 | 10 Dec | 14 Dec | 8,650 | near full (15 Dec) |
| 2025 | 97 | 10 Dec | 13 Dec | 8,810 | thin crescent |

The "twice baseline" line from the refill row is useless here: all three years cross it on 1 Dec, so the ten-times line replaces it.

## Calls for 2026

The 2026 maximum falls on the night of 13 to 14 Dec with the moon new on 9 Dec, so the sky is dark like 2023; the baseline keeps falling about 9% a year.

1. Peak day: 14 Dec at 0.55, 13 Dec at 0.40, any other day 0.05.
2. Peak views: point 11,000; 80% interval 7,000 to 17,000.
3. First day above 10x the November 2026 median (median computed from 1 to 30 Nov 2026 by the scorer): 10 Dec at 0.45, 11 Dec 0.30, 9 Dec or earlier 0.15, 12 Dec or later 0.10.

## Scoring (fixed now)

- Call 1 and call 3: hit or miss on the top pick, plus the log score of the stated probabilities.
- Call 2: absolute error of the point in views, and whether the actual sits inside 7,000 to 17,000.
- Pass for the forecast as a whole: call 2's actual inside 7,000 to 17,000 and at least one of the top picks in calls 1 and 3 hits (so at least two of the three calls right). Anything else is a fail, written up the same way.

DUE row D-033, due 16 Dec 2026, backstop 20 Dec 2026.
