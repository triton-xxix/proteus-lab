# Grinder rule candidates, round 3: skip the rug cluster

Written 8 Oct 2026 00:40 BST, after the round-2 replay (`REPLAY-2.md`, `REPLAY-2-NOTES.md`) and
before any forward row exists. The three markers were each pre-registered on 30 Sep and read on
77 post-30-Sep passers; this round tests them together, forward only, as a shadow book. N for the
family rises to 60 (round 1's 29, round 2's 30, this 1).

## R01: v0.2 minus any rug marker

- Selection: v0.2's gate-passers ranked by 1h volume, top 4 a night, exactly as `paper.py` does,
  except that a row carrying any of these is skipped and the next-ranked row taken:
  1. rugcheck names at least one risk (`rug_risks` not empty in the snapshot);
  2. the snapshot's 1h price change is above 0;
  3. no mention in the 23 Telegram channels in the 24h before the snapshot (a token with no
     Telegram row at all, because the pull failed, is NOT skipped: unmeasured is not silent).
- Exits, costs, fills, stake: v0.2's, unchanged.
- Data: forward only, from the first snapshot at or after 2026-10-08T12:00Z. Nothing before it
  counts, including the 77 rows the markers were read on.
- Kept as a shadow book: v0.2 continues unchanged; R01 is scored beside it on the same nights.

## Pass marks, fixed now

Judged at 40 closed R01 positions, against v0.2's positions from the same nights:
- KEEP (R01 replaces v0.2 as the live rule): rug rate at most half of v0.2's on the same nights,
  expectancy at or above v0.2's, and expectancy with the best three removed at or above zero.
- KILL at 40 if expectancy is below v0.2's on the same nights, or at 20 if R01 has rugged at the
  same rate as v0.2 or worse.
- Anything else at 40 is KILL too; there is no third outcome.

Why not the PASS-MARKS item-3 bar: that bar (V01 plus one point of stake per variant tried) was
written for exit rules that have to add return. A filter removes losers; it is judged on the
losers it removes and on not costing expectancy. Said here before the first row so it cannot be
fitted later.

## How it runs

`paper.py` carries a second book from `BOOKS.json` "second" (inert since 30 Sep). Wiring R01 in
is the build: a `select_r01()` beside the v0.2 selection, the Telegram look-up from
`research/MENTIONS.csv` (which runs before the commit in step 2), and the shadow ledger
`grinder/LEDGER-R01.csv`. Until it is wired, every night's snapshot and mentions rows are enough
to score R01 after the fact from candles, so no night is lost. DUE.md row D-007 holds the date.
