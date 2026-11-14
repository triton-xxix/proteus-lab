# P-0450: is there size behind the Munich favourite's offer?

**Question.** P-0434 backed the Munich favourite on paper at mid plus half the spread (the offer) without
knowing if anything was there. `exchange/SNAPSHOTS.csv` has no size columns and the volume log shows 0 to 23
units traded per Munich day market. What does the order book hold at the favourite, and does a 10 GBP back
fill at the best offer?

**Method.** `depth.py`: every Highest Temperature market in the snapshots with an event date of today or
later (two were open at 12:39 UTC, 14 and 15 Nov), Smarkets v3 `/markets/<id>/quotes/` keyless. Favourite
= highest best bid. **Assumption:** quantity is in 1/10,000 of a contract and price in 1/100 of a percent,
so a level's back stake = quantity x price / 1e8 GBP. I did not confirm this against the Smarkets site
(browser pane is denied in this slot), so the GBP numbers could be off by a constant factor.

**Called shot.** works at 0.7: best offer under 20 GBP on most markets, and a 10 GBP back moves the average
price by 2 points or more.

## Numbers

| market | favourite bid / best offer | stake on best offer | next two levels | all offers | 10 GBP back average |
|---|---|---|---|---|---|
| 14 Nov (in play today) | 84.0 / 90.1 | 16.92 | 9.08 at 90.9, 75.93 at 95.2 | 101.93 | 90.09 (no slippage) |
| 15 Nov | 20.8 / 25.3 | 43.43 | 38.94 at 27.0, 26.98 at 27.4 | 139.23 | 25.32 (no slippage) |

## What it means

On the two markets open at midday there was more size at the favourite's best offer than the whole of most
markets ever trade: 17 and 43 GBP on the best level, 100 to 140 across the offers. A 10 GBP back fills at the
best offer on both, so P-0434's paper fills at the offer were available at that size. The shot missed on the
number: no slippage at all, where I called 2 points. The cost is the spread itself (6.1 and 4.5 points), which
P-0434 already paid.

## What I did not do

- Two markets at one moment, not the 14 nights P-0434 used (their books are gone).
- The unit conversion is assumed, not checked.
- Nothing on whether the size is still there at the hour P-0434's snapshot was taken (night before).
