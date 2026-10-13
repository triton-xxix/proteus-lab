# P-0136: analytic gradient for the Pitch desk's Dixon-Coles fit

The eight-group nightly refit drops from **21.1 s to 0.4 s** (about 50x) when the objective returns
its gradient and L-BFGS-B stops estimating one by finite differences. The objective value at the
optimum is the same to four decimals in every group. The parameters are not identical: up to 0.02
apart on ENG (54 teams), under 0.01 elsewhere, 0.0001 on SCO. Predictions on ENG differ by at
most 1.0 percentage point on p_home across all 2,862 ordered team pairs.

Called shot: works at 0.55, under 6 s with parameters matching to 1e-4. Time hit by a wide margin;
the parameter match missed: the fits stop on a flat ridge of the shrunken likelihood and the
finite-difference run stops at a slightly different point.

## Method

`dc_grad.py`: same likelihood as `pitch/model.py` (weighted Poisson terms, Dixon-Coles tau on the
four low scores, L2 0.02 on attack and defence, time decay XI), with the gradient:
d ll / d log lam = hg - lam + lam (dtau/dlam) / tau, likewise for mu, d ll / d rho = (dtau/drho) / tau,
summed into team slots with bincount; clipped tau rows get zero tau gradient. `gammaln` of the
goal counts computed once per fit instead of every call. Same x0, bounds and maxiter as the desk.
`predcheck.py`: both ENG fits pushed through `model.predict` for every ordered pair.

## Numbers (result.json, predcheck.json)

| Group | Matches | Teams | FD s | Grad s | max abs param diff | nll FD | nll grad |
|---|---|---|---|---|---|---|---|
| ENG | 3,895 | 54 | 10.36 | 0.11 | 0.020 | 889.8747 | 889.8747 |
| ESP | 1,598 | 29 | 1.95 | 0.07 | 0.0038 | 399.5591 | 399.5591 |
| GER | 1,269 | 25 | 1.40 | 0.05 | 0.0053 | 311.1885 | 311.1885 |
| ITA | 1,580 | 27 | 2.13 | 0.05 | 0.0063 | 343.3314 | 343.3314 |
| FRA | 1,352 | 25 | 1.62 | 0.04 | 0.0031 | 309.0484 | 309.0484 |
| NED | 1,296 | 25 | 1.50 | 0.04 | 0.0081 | 352.2756 | 352.2756 |
| POR | 1,295 | 26 | 1.81 | 0.05 | 0.0035 | 321.6979 | 321.6978 |
| SCO | 960 | 14 | 0.38 | 0.03 | 0.0001 | 238.6309 | 238.6309 |

ENG predictions, max abs difference over 2,862 pairs: p_home 0.0103, p_draw 0.0039, p_away 0.0101,
p_over25 0.0065. Home advantage 0.19903 v 0.19903, rho -0.10613 v -0.10611.

## What it says

- The gradient is right: identical objective values at the optimum in all eight groups is not
  something a wrong gradient produces.
- The desk's current fit is the less precise one. With 110 parameters and a finite-difference
  gradient, L-BFGS-B stops within its tolerance on a ridge; a one-point difference in p_home is
  the size of that imprecision, not of the model.
- The backtest refits hundreds of times, so this is minutes to seconds there. Not timed tonight.

## Not done, and what next

- Not switched into `pitch/model.py` tonight: it moves live predictions by up to a point, so it
  goes in through a daytime slot with the backtest re-run (pool weights, Brier) on both fits, then
  a dated note in `pitch/RULES.md`. Queued.
- No `scipy.optimize.check_grad` at random points; the matching optima stand in for it.
