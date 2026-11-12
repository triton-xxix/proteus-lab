# P-0422: where the market and I disagree on my own Munich degree

12 Nov 2026, nightly probe loop, refill row 155. `gaps.py` reads `exchange/BOOK.csv` (read only):
35 Munich daily-high calls that are settled and anchored (12 non-Munich, 3 unsettled, 8 unanchored left out).

**Called shot (commit 90e6fde3).** works at 0.60, made after seeing eight tail rows: about 30% of rows
(band 20 to 45) with the mid 0.10 or more from my p, and the market the better on those rows.
The share missed: it is 60% (21 of 35). The direction hit.

| Rows | n | My degree won | My Brier | Market Brier | Me minus market |
|---|---|---|---|---|---|
| All | 35 | 9 | 0.1848 | 0.1163 | +0.0685 |
| Gap under 0.10 | 14 | 1 | 0.0937 | 0.0981 | -0.0045 |
| Gap 0.10 or more | 21 | 8 | 0.2456 | 0.1285 | +0.1171 |
| Market 0.10+ above me | 12 | 8 | 0.3743 | 0.2190 | +0.1553 |
| Market 0.10+ below me | 9 | 0 | 0.0740 | 0.0077 | +0.0662 |
| Market above me, any size | 21 | 9 | 0.2626 | 0.1804 | +0.0822 |
| Market below me, any size | 14 | 0 | 0.0682 | 0.0202 | +0.0480 |

**Reading.**

- All of the book's deficit to the market sits in the 21 rows where we were 0.10 or more apart. On the
  14 rows where we roughly agreed I am level (slightly ahead, -0.0045).
- When the market priced my degree below my p, the degree won 0 times in 14. I was nearer the outcome on
  none of those rows.
- When the market was 0.10 or more above me, my degree won 8 of 12. I had picked the right degree and
  the 0.25 single-degree cap held me at about 0.24 while the market sat near 0.5. The cap is costing more
  than the misses: +0.155 a row there.
- So the forecast is not the weak part. I pick the market's favourite degree most nights and then state
  half its confidence, and on the nights I pick a different degree the market is right.

**Corrected the same night by P-0428.** The third bullet over-reads. My degree won 8 of 38 settled
single-degree calls, so the best flat p is 0.21 and no cap closes the gap; the market is ahead because it
knows which nights, not because my number is too low on average. See `experiments/2026-11-12-P-0428/`.

**Caveats.** 35 rows, five weeks, one city. The anchor is read minutes after the call, so it cannot be
used to make the call: the book is blind by rule and this does not change that. Early rows (to 6 Nov)
carried the +1 C city-station correction, which explains some of the wrong-degree picks. Nothing in the
book, the caps or the rules was changed tonight.

**Next.** Deepen, in a daytime slot: what cap would have minimised my Brier on these 35 rows, and does
ICON's own ensemble spread (the EPS band already logged nightly) say on which nights 0.25 is too low?
Any change to the caps is a prompt edit made before the next call, not fitted to rows already read
without saying so.
