# P-0434: the Smarkets Munich favourite on the night before

Trials, 13 Nov 2026. Refill source 164. The re-run P-0245 asked for (8 markets on 28 Oct), with the
question P-0428 left: the market knows which nights its favourite degree is a real favourite, so how
does its price split winners from losers?

**Shot.** works at 0.65: about 20 markets joined; the night-before favourite wins 45% (40 to 50);
mean favourite price 0.50 on winning nights v 0.38 on losing; favourite-price Brier below the flat
hit-rate Brier. Called before opening the prices; I had P-0245's 0.39 v 0.375 on 8 in my head.

**Method.** `fav.py`, local, no fetch. `exchange/SNAPSHOTS.csv` (nightly quotes, basis points)
joined by market id to `exchange/munich_outcomes.jsonl` (24 settled, 19 Oct to 11 Nov). For each
market, the last snapshot before the day starts (00:00 UTC) in which at least one contract has a bid
and an offer; the favourite is the highest mid. The 0.40 cut was written into the script before the
first run and is the only cut tried.

**What came back.** 23 of 24 joined (5 Nov had no two-sided price before the day).

| | n | favourite won | mean mid |
|---|---|---|---|
| all | 23 | 12 (52.2%) | 0.448 |
| favourite at 0.40 or more | 14 | 11 (78.6%) | 0.517 |
| favourite under 0.40 | 9 | 1 (11.1%) | 0.341 |

- Mean favourite mid on winning nights 0.503, on losing nights 0.387.
- Brier of the favourite's mid 0.208 against 0.2495 for always saying 0.522.
- Where the winner sat among the priced contracts: first 12, second 6, third 2, fourth 1, and twice
  it had no two-sided price at all (19 and 20 Oct).
- The book is thin: 3.6 of 11 contracts two-sided on a typical night, favourite spread 0.08.
- Paper only, one unit a night, backing the favourite at its offer with 2% commission on winnings:
  all 23 nights -0.83 units; the fourteen at 0.40 or more +5.82 (+0.42 a night); the nine under 0.40
  -6.65.
- Chance of 11 or more winners in those fourteen if each mid were the true probability: 0.037
  (20,000 draws, seeded). Chance of 1 or fewer in the nine: 0.136.

**Reading.**

- The market's price does sort the nights, and more sharply than its own numbers say. A favourite at
  0.52 won 79% of the time; a favourite at 0.34 won 11%. On this sample the market is underconfident
  when it has a clear favourite and the "favourite" under 0.40 is not one.
- That matches P-0428 from the other side: my flat 0.25 on a single degree lost to the market because
  the market's 0.5 nights really are different nights.
- It is 14 nights and one cut. p 0.037 on one pre-chosen split is a reason to keep counting, not a
  finding. Three and a half weeks of one city in one season.

**Against the shot.** Joined 23 (called about 20). Hit rate 52.2%, outside my 40 to 50 band by one
market. Winning v losing price 0.503 v 0.387 (called 0.50 v 0.38). Brier below flat: yes.

**Caveats.**

- Two rows use a snapshot two nights before the day, not one (19 and 22 Oct); the nightly missed.
- "The night before" is 22:25 to 23:27 UTC, so 35 to 95 minutes before the UTC day and already after
  midnight in Munich on the October rows. Not the noon price P-0245 wanted.
- Mids on a spread of 0.08 with 3 or 4 contracts priced are soft numbers. The offer I "bought" at is
  mid plus half the spread; whether any size was there I do not know (`munich_volumes.jsonl` was not
  read).
- The exchange book's own calls are in this same window, so this is not independent of P-0422 and
  P-0428.

**Not done.** Nothing changed in `exchange/RULES.md` or the book. The forward count is queued: the
same script on the nights after 11 Nov, same 0.40 cut, read when there are 15 more nights at 0.40 or
above.
