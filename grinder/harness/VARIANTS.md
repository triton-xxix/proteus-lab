# Grinder rule candidates: variants for the replay

Written 30 Sep 2026, before `replay.py` exists and before any replay has run. Governed by
`PASS-MARKS.md`, "The Grinder: rule candidates, the replay, and promotion".

## Declared up front: 25 of these have already been looked at

At about 00:30 on 30 Sep I ran a what-if (`sandbox/grinder_timing.py`) over the 16 closed v0.2
positions' saved candles, for Luke, before this file existed. That breaks item 1 of the procedure
(list before run). The honest repair is to count every variant I looked at in N, mark them seen,
and replay them on a wider population than the one I looked at. V01 to V25 are those. The best of
them on the 16 was V05 (TP +50, SL -20, +£36 total, hindsight). V26 to V29 are new tonight.

N = 29. So a variant's replay expectancy has to beat V01's by 10 + 19 = **29 points of stake**,
and clear every other line in item 3, to open a second book.

## The replay, fixed before it runs

- **Population.** Every row of every nightly snapshot in `grinder/SNAPSHOTS.csv` that passes the
  v0.2 entry gates (`paper.passes`), from the first snapshot to the last one whose 24-hour window
  has closed when the replay runs. A mint enters once, on the first snapshot it passes. This is
  wider than the live book: the live book takes four a night and skips mints it has ever held.
- **Entry.** The snapshot's `price_usd` at the snapshot time, `entry_liq` from the same row.
- **Candles.** GeckoTerminal keyless minute candles for the snapshot's pair, first full minute
  after entry to entry plus 24 hours, saved under `grinder/harness/candles/` and committed.
  A pool that returns nothing is counted as missing, not dropped silently.
- **Fills.** The v0.2 fill rule (`paths.walk`), unchanged: stop before take-profit inside one
  candle, gap fills at the open, rug inside the trigger minute fills at the close. A trailing stop
  is a stop whose level is the running high of earlier candles times (1 - trail), active only once
  that high is above entry; the effective stop is the higher of the fixed stop and the trail level,
  and it fills and slips like a stop (3%). A time stop fills at the last close before its horizon.
- **Costs.** `paths.pnl_v02`, unchanged. £100 stake.
- **Selections reported.** All passing rows (no slot cap); the top 4 by 1h volume each night (the
  live selection without the ever-held rule); the top 8 by 1h volume each night. Item 3 is judged
  on the all-passing selection. The other two are reported, not judged.
- **Lines (PASS-MARKS item 3).** At least 40 closed replayed positions; expectancy at least +10% of
  stake; expectancy at or above zero with the best three removed; expectancy at least 29 points of
  stake above V01's. Only the single best qualifying variant by trimmed expectancy opens a book.

## Variants

| ID | Entry delay | Take-profit | Stop | Trail | Time stop | Seen on the 16 |
|---|---|---|---|---|---|---|
| V01 | 0 | +100% | -50% | none | 24h | yes (current v0.2) |
| V02 | 0 | +30% | -20% | none | 24h | yes |
| V03 | 0 | +30% | -30% | none | 24h | yes |
| V04 | 0 | +30% | -50% | none | 24h | yes |
| V05 | 0 | +50% | -20% | none | 24h | yes |
| V06 | 0 | +50% | -30% | none | 24h | yes |
| V07 | 0 | +50% | -50% | none | 24h | yes |
| V08 | 0 | +100% | -20% | none | 24h | yes |
| V09 | 0 | +100% | -30% | none | 24h | yes |
| V10 | 0 | +200% | -20% | none | 24h | yes |
| V11 | 0 | +200% | -30% | none | 24h | yes |
| V12 | 0 | +200% | -50% | none | 24h | yes |
| V13 | 0 | none | -50% | 20% | 24h | yes |
| V14 | 0 | none | -50% | 30% | 24h | yes |
| V15 | 0 | none | -50% | 40% | 24h | yes |
| V16 | 0 | none | none | none | 1h | yes |
| V17 | 0 | none | none | none | 4h | yes |
| V18 | 0 | none | none | none | 12h | yes |
| V19 | 0 | none | none | none | 24h | yes |
| V20 | 15 min | +100% | -50% | none | 24h | yes |
| V21 | 30 min | +100% | -50% | none | 24h | yes |
| V22 | 60 min | +100% | -50% | none | 24h | yes |
| V23 | 120 min | +100% | -50% | none | 24h | yes |
| V24 | 240 min | +100% | -50% | none | 24h | yes |
| V25 | 480 min | +100% | -50% | none | 24h | yes |
| V26 | 0 | none | -20% | 20% | 24h | no |
| V27 | 0 | none | -20% | 30% | 24h | no |
| V28 | 0 | +50% | -20% | 20% | 24h | no |
| V29 | 0 | +50% | -20% | none | 4h | no |

"None" for a stop means only the rug rule (-90%) closes early. A delayed entry takes the open of
the first candle at or after the delay, at the same costs, and its 24 hours run from that entry.
