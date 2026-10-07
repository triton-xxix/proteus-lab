# P-0069: my Dixon-Coles against penaltyblog's, and what the free courses add

Run 7 Oct 2026, interactive probe loop. `compare.py` refits penaltyblog 1.6.2's
`DixonColesGoalModel` every test week on every English match before it (Premier League and
Championship together, the same data my model sees), weighted exp(-0.0065 x days), and sets its
probabilities beside mine from `pitch/backtest/predictions.csv`.

## Same model, independently built

Season 2025-26, 930 matches over 38 weeks (penaltyblog: 17 s for all 38 fits):

| | Mine | penaltyblog | Closing market |
|---|---|---|---|
| Brier (lower is better) | 0.6373 | 0.6372 | 0.6201 |
| Log loss | 1.0568 | 1.0556 | 1.0295 |
| Mean draw probability | 0.2641 | 0.2633 | 0.2590 (actual 0.2688) |

- Mean absolute difference per outcome: 0.18 points. Only 0.5% of matches differ by more than two
  points anywhere; the largest gap is 8.7 points. The small differences are my L2 shrinkage (0.02),
  which penaltyblog does not apply.
- So my implementation is right, and the gap to the market is not a bug. It is what the model
  does not know.

## What the free courses would add

- **Soccermatics, "Calculating match outcomes"** (soccermatics.readthedocs.io/en/latest/lesson5/PoiBin.html):
  build each side's goal distribution from per-shot expected goals with a Poisson-binomial, not from
  final scores. I skip this: football-data has shots and shots on target (my `sot` model) but no
  per-shot xG.
- **Betfair data scientists, EPL machine learning** (betfair-datascientists.github.io/modelling/EPLmlPython/):
  exponentially weighted shots, corners and cards, Elo, squad market value by position, and moving
  averages of Asian handicap and over/under odds, validated on a held-out season. I skip squad value
  and odds-as-input. Their own reported result: log loss 0.9577 for the model against 0.9464 for
  the odds on 2017-18. Even with the market fed in, it did not beat the market.

## Verdict

Works. My Dixon-Coles matches an independent library to 0.18 points, so the Pitch's losses are the
model's information, not its code. The next step the courses point to is per-shot xG; the honest
expectation from Betfair's own numbers is that richer inputs narrow the gap rather than close it.
