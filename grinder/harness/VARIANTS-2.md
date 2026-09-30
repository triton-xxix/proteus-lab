# Grinder rule candidates, round 2: what gets bought

Written 30 Sep 2026 before `grinder/research/MENTIONS.csv` has a single row, and after the round-1
replay (`REPLAY.md`) showed that no exit rule rescues the v0.2 selection. Same procedure as
`VARIANTS.md` and PASS-MARKS item 3; N for round 2 counts round 1's 29 as well, because they were
tried on the same weeks.

## Two kinds of variant, judged on different data

**Seen (E01 to E05).** I looked at these splits on the 58 round-1 tokens on 30 Sep before writing
this (`winlose` in the session of that day): rising 1h price at entry went with dying, rugcheck
warnings went with dying, older tokens and lower volume-to-liquidity went with surviving. Because
they were seen, their replay counts **only snapshots taken after 2026-09-30T12:00Z**. The 58 cannot
vote for them.

**Unseen (M01 to M06).** Mention and paid-promotion signals from `grinder/research/mentions.py`.
Nobody has looked at these numbers against outcomes. They may be replayed on the 58 (backfill) and
on every later night.

## Exits

Every round-2 variant is run at two exits: V01 (the current v0.2 exits) and V17 (hold 4h, the
round-1 exit with the best trimmed-free showing). The pair counts as two variants each.

## Variants

| ID | Entry rule on top of the v0.2 gates | Data it may use |
|---|---|---|
| E01 | 1h price change at the snapshot at or below 0 | after 30 Sep 12:00Z only |
| E02 | no rugcheck risk named (`rug_risks` empty) | after 30 Sep 12:00Z only |
| E03 | E01 and E02 | after 30 Sep 12:00Z only |
| E04 | age at least 12h, 1h volume at most 1x liquidity, no rugcheck risk | after 30 Sep 12:00Z only |
| E05 | E01 and E04 | after 30 Sep 12:00Z only |
| M01 | X: at least 10 distinct authors in the 24h before the snapshot | backfill and later |
| M02 | X: at most 3 distinct authors (the quiet ones) | backfill and later |
| M03 | X: shill or call share at or below 0.5 | backfill and later |
| M04 | Reddit: at least one mention in the six subreddits | backfill and later |
| M05 | DexScreener: no paid profile, boost or ad before the snapshot (tonight onward; backfill cannot date boosts) | after 30 Sep 12:00Z only |
| M06 | M03 and E01 | after 30 Sep 12:00Z only |

11 entry rules x 2 exits = 22. **N = 29 + 22 = 51.** Bar for a second book: expectancy at least
+10% of stake, at least 40 closed positions, best three removed at or above zero, and at least
10 + 41 = 51 points of stake above V01 on the same rows. That is a high bar, on purpose: most of
these will fail it and the ones that clear it will have earned the book.

## Added 30 Sep 2026, after seeing the backfill and the gate replay (forward-only, N rises)

Written after `MENTIONS-REPLAY.txt` and `GATES.md` were read, so these are seen and count only
snapshots after 2026-09-30T12:00Z. Each at V01 and V17: 4 more variants, **N = 55**.

| ID | Entry rule | Why it is here |
|---|---|---|
| M07 | X: at least one post by anyone in the 24h before the snapshot | on the 58, the 37 silent tokens were up at 24h 5 times (V01 -£36.9); the 21 talked-about 8 times (about -£2.4) |
| E06 | the v0.2 gates except age, with age above 48h instead of at most 48h (needs the scanner to surface older pools) | the 20 age-rejected tokens older than 48h averaged about -£2.9 at V01 against -£24 for the passers; the 5 under 1h all died |

M01 to M04 on the 58 (unseen, pre-registered): none clears the bar. M01 and M03 have 1 and 4
rows; M02 (quiet, 41 rows) is -£26.5 at V01; Reddit has 2 hits in 58 and Telegram 0.
