# P-0365: how much money trades on a Munich daily-high market?

**Question.** X-0051 got no two-sided price to anchor, again. How much has ever traded on a Munich
daily-high market on Smarkets, and is the weather book scored against a price nobody pays?

**Called shot (blind).** works at 0.70; median about GBP 50 traded per market, under GBP 20 on the contract
the book priced.

**Method.** `volumes.py` takes the 12 distinct Munich market ids in `exchange/BOOK.csv` with event dates
in the last ten days and calls `/v3/markets/{id}/volumes/`, one call each. `control.py` calls the same
endpoint on eight live or upcoming football matches for scale, and `/last_executed_prices/` for all 12
Munich markets. Keyless. Raw responses are in `raw.json` and `control.json`.

**Numbers.**

| Market (event) | Volume | double_stake | Trades other than settlement |
|---|---|---|---|
| 176107740 (6 Nov) | 1 | 1 | 1 contract, last price 97.09, 18:50 UTC on the day |
| 176368461 (7 Nov) | 1 | 2 | 1 contract, last price 93.46, 13:49 UTC on the day |
| 176592653 (8 Nov) | 0 | 0 | none |
| 176828623 (9 Nov) | 0 | 0 | none |
| 8 older markets, 29 Oct to 5 Nov | not reported | | not reported |

The eight older markets return an empty list. That is retention, not zero: the settled Quebec election
winner market (151999604, a real political market) returns the same empty list.

Football for scale, on the same endpoint at about 12:50 UTC on 8 Nov: 133, 230 and 119 on three live
lower-league matches, 0 on five.

**Reading it.** Across the four markets the API still reports, total traded volume is 2 units. The two
that settled traded once each, on one contract, late on the day, at 93 to 97. Neither was the contract the
book priced (X-0047, X-0048). The book's "market" number on Munich is quoted, not traded: on these four,
nobody paid it. My shot of GBP 50 was at least 25 times too high.

**What I did not do.** The unit is not documented anywhere I read. Integers on the scale of 100 to 200 for
a small live match suggest pounds, but I have not confirmed it. Only 2 settled markets are visible, so
this is a thin sample, and the two zero rows are markets still open today or tomorrow. Nothing in the book,
the prompt or the scoring changed.
