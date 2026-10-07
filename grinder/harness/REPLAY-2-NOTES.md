# Round-2 replay, what it says (8 Oct 2026)

The table is `REPLAY-2.md` (rebuilt by `replay2.py`; this file is the reading, kept separate so a
rerun cannot overwrite it). Pre-registered 30 Sep in `VARIANTS-2.md`; first run 8 Oct, after Luke
asked why it had not been run. Population: 150 gate-passers from 13 nights, 89 rows since the
30 Sep cut; the seen variants use the 77 passers since then. Overlap counts from
`sandbox/readit/rugmarks.py` (copied to `experiments/2026-10-08-P-0096/`).

## Nothing qualifies, and the bar is why

The bar is V01 on the same rows plus 59 points of stake, from PASS-MARKS item 3 (10 plus one per
variant tried, N = 59). An entry filter cannot add 59 points to a book whose field averages
-£18.5: filters remove losers, they do not create winners. The bar was written for exit rules
and carried over unchanged. It stays as written for this round; the next pre-registration below
judges a filter on the thing a filter does.

## The rug cluster is visible before entry

Three markers, each pre-registered on 30 Sep, each read on the 77 passers since then:

| marker | rows carrying it | rugs among them | rows without it | rugs among those |
|---|---|---|---|---|
| rugcheck names a risk (not E02) | 17 | 13 | 60 | 5 |
| price up over the hour before entry (not E01) | 46 | 15 | 31 | 3 |
| no mention in the 23 Telegram channels (not M09) | 14 | 9 | 63 | 9 |

They stack. Zero markers: 29 rows, +£0.8 a position, 2 rugs, 12 wins. One: 28 rows, -£9.2, 2
rugs. Two: 11 rows, -£42.8, 7 rugs. Three: 9 rows, -£79.6, 7 rugs, 1 win. Eighteen of the field's
twenty rugs sit on rows with at least one marker, and the markers cost nothing to read: rugcheck
and the snapshot's 1h change are already in `SNAPSHOTS.csv`, Telegram is in `MENTIONS.csv`.

Two more from the mention data: tokens with no paid DexScreener promotion before the snapshot
(M05, 18 rows) rugged 13 times, so an unpromoted gate-passer is a rug candidate, not a bargain;
and tokens quiet on X did no worse than loud ones (M02, M07), which reverses the 30 Sep read
that silence kills. The X numbers cover only the 8 capped tokens a night, so they are thinner.

## What the filter does not do

It does not make the broad field profitable: the clean 29 average +£0.8 and go negative with the
best three removed. The live book's profit comes from the top 4 by 1h volume, and the overall
top-4 slice since 30 Sep made +£24.0 a position (24 rows) while the clean rows' own top-4 made
+£6.1. So some of the live book's wins were marked tokens that doubled before they died. A filter
that drops them trades profit for fewer rugs on this window. Which of those the book should
prefer is the forward test, not a replay.

## Pre-registered next (VARIANTS-3.md, DUE.md D-007)

R01: the v0.2 selection (top 4 by 1h volume among gate-passers) with any row carrying a marker
skipped and the next-ranked clean row taken instead, at the v0.2 exits, forward only from the
8 Oct snapshot, as a shadow book beside v0.2. Judged at 40 closed positions against v0.2 on the
same nights: rug rate, expectancy, and expectancy with the best three removed. Lines in the file.
