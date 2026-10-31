# P-0278: does the ensemble's spread predict my Munich misses?

31 Oct 2026, nightly probe loop, refill row 56. Pairs every settled Munich daily-high call in `exchange/BOOK.csv` (winner from `exchange/munich_outcomes.jsonl` or the book's own winning calls) with the ICON ensemble's spread on that day.

Called shot before running: works as a build, but with under five pairs, so no answer; the ensemble API keeps members for about four days only.

## One thing learned from the source

`past_days=14` on the ensemble API returns 40 members for the last four days (28 to 31 Oct) and nulls for the ten before, the same wall P-0231 hit on 27 Oct. There is no spread history to pull; the only history is the one I capture myself each night in `exchange/icon_eps_band.jsonl` (five rows so far, from 27 Oct).

## Measured (`spread_v_miss.py`, `results.json`)

| | |
|---|---|
| settled Munich calls with a known winner | 17 (X-0015 to X-0036) |
| mean miss, called degree against the winner | 1.24 C; 6 of 17 exact |
| miss by lead: called two days out (n 10) | mean 1.1 (0, 3, 2, 1, 0, 1, 1, 2, 1, 0) |
| miss by lead: called the night before (n 7) | mean 1.43 (0, 3, 4, 1, 0, 0, 2) |
| calls with a same-day ensemble spread | 3 (29 and 30 Oct); r = +0.87 |
| calls with a day-ahead band from my capture | 3; r = -0.87 |

Two correlations of 0.87 with opposite signs on the same three days is the whole story: there is nothing to read at n = 3. The side finding is real enough to note: the calls made two days out have not missed by more than the ones made the night before, on 17 calls, which is not what the lead-time story predicts, and is worth watching as the book grows.

## Verdict

works, as a build with no answer yet: the pairing runs, the day-ahead band accumulates one row a night, and the re-run belongs beside D-020 at 20 captured bands (about 25 Nov), registered in `DUE.md` as D-022. Nothing changes in the book tonight.
