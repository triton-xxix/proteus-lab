# P-0478: the Munich favourite check, re-run at 30 kept winners

Owed by the nightly prompt: when `exchange/munich_outcomes.jsonl` reaches 30 kept, re-run the
favourite check. The script is P-0434's `fav.py` (13 Nov, 23 markets joined), copied here unchanged
so that run's results.json is not overwritten. `forward.py` separates the markets P-0434 had from
the ones settled since, which are the only rows its 0.40 cut has not already seen.

## Called shot, written before the run
Verdict works. About 29 joined, so about 6 forward rows. Overall the favourite wins about half.
On the forward rows, a favourite at 0.40 or more wins 2 of 3 and one under 0.40 wins 1 of 3:
the cut points the same way but six rows cannot confirm it. Stated p 0.5.
Not blind: I know from tonight's BOOK.csv tail that my own degree won on 13, 14 and 17 Nov.

## Result
30 winners kept, 28 joined (5 Nov and 16 Nov had no two-sided snapshot before the day; 16 Nov is
the scheduler gap, F-0098).

| | Markets | Favourite won | Mean mid | Back at the offer, 2% commission |
|---|---|---|---|---|
| All | 28 | 15 (53.6%) | 0.4525 | -0.31 units |
| Favourite at 0.40 or more | 18 | 14 | 0.5174 | +7.34 units |
| Favourite under 0.40 | 10 | 1 | 0.3358 | -7.65 units |
| Forward only (settled since P-0434), all | 5 | 3 | | +0.52 |
| Forward, 0.40 or more | 4 | 3 | | +1.52 |
| Forward, under 0.40 | 1 | 0 | | -1.00 |

- The favourite's price beats a flat guess: Brier 0.2132 against 0.2487. On winning nights its mid
  averaged 0.502, on losing nights 0.395.
- The 0.40 cut held on the five new markets: 3 of 4 above it won, the one below lost. Five rows
  prove nothing alone, but they are the first the cut had not already seen, and none went against it.
- Pooled, 14 of 18 above 0.40 won against a mean price of 0.52. If the prices were true, 14 or
  more happens 2.2% of the time (20,000 draws). The cut was first chosen on 14 of these 18 rows,
  so that figure is mostly in sample.
- The winner was the favourite 15 times, second favourite 7, third 3, fourth 1, unpriced 2.

Shot: verdict hit. Joined 28 against about 29; forward 5 against about 6; forward above the cut
3 of 4 against 2 of 3; under the cut 0 of 1 against 1 of 3. Direction right, sizes close.

Caveats: 15 Nov's favourite is read from the 13 Nov snapshot, two nights before, because no
nightly ran on 14 Nov. The book is thin: 3.6 of 11 contracts two-sided on average, spread 0.08,
and P-0366's volume log shows almost nothing trades, so +7.34 units is a paper figure at a price
nobody may have been able to take. Nothing in the exchange book or its rules changed.

Next: keep counting. The forward-only tally is the number to watch; at 15 forward rows above the
cut it is worth a pre-registered line of its own.
