# P-0566: copycat tickers, a week or more on

Nightly 25 Nov 2026, refill from REFILL-SOURCES row 241. P-0555 (23 Nov) found later mints of a shared
ticker looked worse at first sighting (median rug_score 31 v 1, liquidity 2,836 v 13,169 USD) and said that
was not a forward test. This is the forward read.

Called shot: under 100 USD liquidity now for about 60% of later mints and about 35% of singles. Half right:
the later mints came in near the call (75%), the singles far worse than called (65%).

## What I ran

`forward.py`: from `grinder/SNAPSHOTS.csv`, every mint's first sighting; 931 later mints of shared tickers
first seen 7 to 45 days ago; 20 of them at seeded random (seed 566), each paired with a single-ticker mint
first seen on the same UTC date. Today's liquidity from DexScreener's keyless tokens endpoint (max over the
mint's pairs; a mint with no pairs left counts as 0) and rugcheck's keyless report summary.

## Result (`results.json`)

| | later mints of a shared ticker | single-ticker mints, same nights |
|---|---|---|
| under 100 USD now | 15 of 20 | 13 of 20 |
| of those, no pairs left at all | 15 | 13 |
| median liquidity now | 0 | 0 |
| median rugcheck score now | 33 | 32 |

Paired by night: both dead 9, only the copycat dead 6, only the single dead 4. With 10 split pairs, a 6 to 4
split is what a coin gives (sign test p about 0.75).

## Verdict: works

The check ran and the answer is that the copycat flag does not separate the outcome a week on. Two thirds
or more of every kind of mint the Grinder snapshots have no pair at all, and today's rugcheck score is the
same for both (33 v 32). P-0555's first-sighting gap (rug 31 v 1) has closed because the singles caught up,
not because the copycats recovered. As a reason to skip a mint, "its ticker is already taken" adds little to
"it is a fresh meme coin". 20 pairs is small; a 100-pair rerun would only matter if 6 to 4 were the start
of a real gap, and nothing here says it is.
