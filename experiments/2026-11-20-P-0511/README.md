# P-0511: P-0510's international model against my judgement book

Question: P-0510's Elo plus Poisson, frozen before each match day, on the judgement book's scored rows:
does it beat my anchored column, my blind column, or the market?

No called shot: I went straight from queuing this to running it and did not stop to call it. Logged as
unshot.

## Method

`judge.py`, standard library. Same Elo and Poisson as `experiments/2026-11-20-P-0510/model.py`; Elo
snapshot taken before each judgement match day from martj42 `results.csv` (last row 17 Nov 2026, so the
Sep to Nov 2026 matches are in it); Poisson fitted on 2010 to 25 Sep 2026, no friendlies. Home side gets
+100 (every row is a home game in the Nations League or qualifiers; not checked one by one). Market
prices normalised to sum to 1. Brier is the book's own 3-way sum.

## Numbers

57 scored rows, 55 used (J-0013 and J-0041 missed on the name "Bosnia & Herzegovina"; my alias table had
the wrong spelling).

| column | 3-way Brier, 55 rows |
|---|---|
| market | 0.538 |
| me, anchored | 0.546 |
| Elo plus Poisson | 0.581 |

On the 32 rows with a blind call: market 0.552, my blind 0.561, model 0.586.

So the model is 0.043 behind the market and 0.025 behind my own blind calls. It beat uniform on the
2022 World Cup (P-0510), but as a blind column here it is worse than what I already write by hand.

## Not done

No draw inflation, no tuning of K or home advantage, two rows lost to a name. None of that is likely to
find 0.04.
