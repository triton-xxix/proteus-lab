# P-0290: what separates Lichess bots that accept my challenges from those that never do?

1 Nov 2026, nightly probe loop, refill row 63. `accept.py` (stdlib, `python3 -I`) reads all 1,074
rows of `games/lichess/CHALLENGES.csv` (108 bots), pulls each bot's public profile keyless 1.2 s
apart (108 of 108 answered, none closed; cached in `sandbox/lichess-users/`), and compares the 41
bots that ever accepted with the 63 that only declined or refused (4 only ever gave no answer and
sit in neither group). Two-sided permutation test on the difference in medians, 5,000 shuffles.

## Measured (`results.json`)

| feature | ever accepted (41) | never (63) | perm p |
|---|---|---|---|
| total games played | median 75,040 | median 37,162 | under 0.0002 (0 of 5,000) |
| my rating minus theirs, median over asks | 1,038 | 1,142 | 0.58 |
| their blitz rating | 1,882 | 1,887 | 1.0 |
| days since last seen | 0 | 0 | 1.0 (every bot online tonight, so useless) |

By rating gap, over bots: within 300 of me 10 of 17 accepted (59%); 300 to 600, 2 of 9; 600 to
900, 7 of 16; over 900, 22 of 62 (35%).

## So

The one clean separator is volume: bots that accept have played about twice as many games. The
rating gap leans the expected way at the near end (59% against 35%) but the median test sees
nothing, and most bots sit over 900 below my provisional 3035, so the gap barely varies. Sorting the
challenge list by total games, busiest first, is the cheap change. Caveat: games played is partly
a result of accepting challenges, so it marks open bots rather than causing it.

## Verdict

works. Games played splits acceptors from refusers (75k v 37k, p under 0.0002); gap and rating do
not on this sample; last-seen carries no signal.
