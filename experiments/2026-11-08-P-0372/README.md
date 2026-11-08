# P-0372: where does tonight's one-hour volume sit against the Grinder's gate?

Measured only. No rule changed. The line is `vol_h1_min` 10,000 USD in `grinder/paper.py`.

## What I pulled

Three pages of GeckoTerminal's Solana `new_pools` (`pull.py`), then `reread.py` over those rows and tonight's 146 rows of `grinder/SNAPSHOTS.csv`.

## The feed is the wrong instrument

All 60 rows were 1 to 3 minutes old, so three pages cover about two minutes of launches. None can pass the 1 hour age floor. A pool's "one-hour" volume here is its first minutes.

The 60 rows are 45 distinct pools: 15 pools came back on more than one page. Repeat rows disagree, by as much as 20.65 times on a single pool (Wuntermut / SOL, 4,210 against 50,361), so the pages are not one consistent moment. I did not find out why. Part one's `pull.py` counts rows, so `reread.py`'s distinct numbers are the ones to use.

## Numbers

| | New pools, distinct | Grinder snapshot, 1 to 48 h old |
|---|---|---|
| Pools | 45 | 68 |
| Clear 10,000 USD one-hour volume | 3 | 11 |
| Within half below the line | not recomputed for distinct pools | 5 |
| Median one-hour volume | 130.84 USD | 11.80 USD |
| p90 | not recomputed for distinct pools | 24,219.53 USD |
| Max | 50,361 USD | 213,793 USD |

## Reading

Inside the age window the distribution is split in two. The median token did under 12 dollars in its hour, and the 90th percentile did over 24,000. Only 5 pools sit within half below the line, so moving it a little would add little. 11 of 68 clear it, and the Grinder still had 0 gate-passers tonight, so the volume line is not the only thing stopping them.

## Called shot

Said about 6 of 60 clear, median under 1,000 USD. Got 3 of 45 distinct, median 131. Verdict right, median right, count high by about half in share terms (10% called, 6.7% measured).

## Not done

One night, one snapshot. Did not test which other gate each of the 11 fails. Did not investigate why repeat rows differ.
