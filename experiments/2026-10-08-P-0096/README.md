# P-0096: the Grinder's round-2 entry-rule replay, run eight days late

Run 8 Oct 2026, 00:05 to 00:45 BST, interactively, after Luke asked what makes a good meme coin
and found this replay had been pre-registered on 30 Sep and never run.

- Script: `grinder/harness/replay2.py` (new; wires E01-E06 and M01-M09 from `VARIANTS-2.md` into
  the round-1 harness, with the mentions join). Candles fetched keyless from GeckoTerminal for
  189 rows, 0 missing.
- Table: `grinder/harness/REPLAY-2.md`. Reading: `grinder/harness/REPLAY-2-NOTES.md`.
- Overlap of the three rug markers: `rugmarks.py` here (output in the notes).
- Next: `grinder/harness/VARIANTS-3.md`, R01 as a forward shadow book, DUE.md row D-007.

One bug on the way: the first run joined mentions on the full night timestamp and matched
nothing; fixed to the date and rerun from cache.

Verdict: **works**. Nothing clears the pre-registered bar, and the bar is the wrong shape for a
filter. The finding is that eighteen of the field's twenty rugs since 30 Sep carried at least one
of three markers readable before entry (rugcheck risk, rising into the snapshot, no Telegram
mention), and that the X-silence lead from 30 Sep reversed.
