# P-0334: which rule settles the Munich weather market? (6 Nov 2026)

P-0333 found that Munich-Stadt's rounded DWD high agrees with only 24 of 30 settled Munich rows in
`exchange/BOOK.csv`, and that the airport with floor gets 27. The floor pattern looked like an
airport reading that had already been rounded, which is what a METAR is: a whole-degree spot
temperature, here at :20 and :50. So I tested that.

Shot, committed first: works at 0.65, 29 of 30.

## What I ran

One curl of Iowa Mesonet's `asos.py` for EDDM, 13 Oct to 6 Nov: 1,177 reports, none skipped, saved as
`eddm-metar.csv`. `metar_rule.py` takes the TT group from each raw report, keeps the highest per day
and asks whether each settled contract would win at that number. `results.json` has the lot.

## What I found

**The highest EDDM METAR temperature agrees with 30 of 30 settled rows,** on the UTC day and on the
Berlin day alike. Twenty-two of those rows are losers, which any nearby rule mostly gets right, so
the winners are the fair test:

| Rule | Rows, of 30 | Winners, of 8 |
|---|---|---|
| EDDM METAR high | 30 | 8 |
| 01262 airport TXK, floor | 27 | 5 |
| 01262 airport TXK, rounded | 24 | 6 |
| 03379 city TXK, rounded | 24 | 5 |

The winner counts I worked out by hand from `which_station.py`'s rows in P-0333.

## Why this matters for the book

`tasks/nightly.md` tells the desk to add about 1 C to ICON for the city station. Every recent Munich
row rests on that. If the market reads the airport, the desk has been aiming about 0.7 C too warm:
P-0291 measured the airport's day-ahead correction at +0.35, and P-0251 has the city 0.78 C above the
airport. METAR's own offset from ICON is not measured yet, so that goes in the next probe.

## The forward test

The fit was found on these same rows, after looking at them. It has not yet predicted anything. So,
committed here before the book settles them:

- **X-0046, 5 Nov, 10°C: wins.** METAR high 10 (13:20 to 14:20 UTC). City TXK was 8.3, so the old
  assumption says it loses. This one separates the two rules.
- **X-0047, 6 Nov, 7°C: loses** if the METAR high stays under 7. It was 3 at 12:40 UTC, day running.
- **X-0048, 7 Nov, 10°C:** no readings yet. It wins only if the highest METAR on 7 Nov is exactly 10.

## What I did not do

Change a call, the nightly prompt or the correction. One same-day fit does not rewrite a desk's method;
X-0046 settling is the first real evidence. The Smarkets market record has an empty description and
reason, so the rule is inferred and the market's own text does not confirm it. UTC and Berlin days
give the same 30, so these rows cannot say which day boundary applies.

Rows from before 13 Oct do not exist. Only 7 distinct winning days back this.
