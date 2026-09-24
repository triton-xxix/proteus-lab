# P-0004: bookmaker disagreement as a feature

**Verdict: not worth it for the desk.** On the desk's own model the feature earns nothing: adjusted DC
takes 0.00 pool weight against the close in all three seasons across nine leagues, and pooled out-of-sample
log loss moves by 0.0006. The one faint signal is on the market itself: the pre-close price shaded away from
outcomes with an outlying Max price (every fitted coefficient negative on H and A, nine leagues) takes a pool
weight of 0.08 to 0.29 against the close where the raw pre-close takes 0.00 to 0.14. The gain is 0.0005 of log
loss against a 0.0021 gap to the close, and the pool weight is in-sample on the test season, so it is a lead,
not an edge. E0 alone is too small to say anything (2026-27 has 50 rows and the fit blows up there).
Correlation of disagreement with the move to close is within 0.07 of zero everywhere.

Disagreement d_k = Max_k / Avg_k - 1 on the pre-close prices, per outcome. Saved walk-forward DC probabilities
from `pitch/backtest/predictions.csv`, no refit. Coefficients fitted leave-one-season-out on log loss; every
number in the out-of-sample tables is on a season the coefficients never saw. Pool weight is `best_weight`
against the devigged average closing price, as in the harness.

## E0 (n=810)

Disagreement, median (90th pct): H 0.027 (0.061), D 0.042 (0.068), A 0.038 (0.103)
Correlation of d_k with the move to close (close minus pre-close prob): H +0.069, D -0.007, A +0.040

| base | season | log loss base | log loss adjusted | change | b_H, b_D, b_A (fitted elsewhere) | pool wt base v close | pool wt adjusted v close |
|---|---|---|---|---|---|---|---|
| pre-close | 2425 | 0.9706 | 0.9718 | +0.0013 | -1.05, +3.90, -0.59 | 0.00 | 0.11 |
| pre-close | 2526 | 1.0153 | 1.0139 | -0.0013 | -4.22, -0.41, -1.14 | 0.00 | 0.18 |
| pre-close | 2627 | 1.0522 | 1.0761 | +0.0239 | -5.92, +0.22, -1.60 | 1.00 | 0.29 |
| dc | 2425 | 0.9800 | 0.9776 | -0.0024 | -1.80, +1.88, -1.82 | 0.11 | 0.20 |
| dc | 2526 | 1.0411 | 1.0396 | -0.0015 | -4.21, +0.39, -0.63 | 0.00 | 0.00 |
| dc | 2627 | 1.0494 | 1.0754 | +0.0259 | -6.39, +0.02, -2.33 | 0.60 | 0.36 |

Out of sample, pre-close, all seasons pooled (n=810): log loss 0.9966 to 0.9980, change +0.0015.
Out of sample, dc, all seasons pooled (n=810): log loss 1.0129 to 1.0127, change -0.0002.
Closing price log loss on the same rows: 0.9933.

## all nine leagues (n=6766)

Disagreement, median (90th pct): H 0.031 (0.066), D 0.043 (0.075), A 0.043 (0.107)
Correlation of d_k with the move to close (close minus pre-close prob): H -0.004, D -0.022, A +0.006

| base | season | log loss base | log loss adjusted | change | b_H, b_D, b_A (fitted elsewhere) | pool wt base v close | pool wt adjusted v close |
|---|---|---|---|---|---|---|---|
| pre-close | 2425 | 0.9697 | 0.9685 | -0.0011 | -1.52, -0.14, -1.19 | 0.00 | 0.08 |
| pre-close | 2526 | 0.9830 | 0.9831 | +0.0001 | -3.48, -1.82, -2.48 | 0.14 | 0.29 |
| pre-close | 2627 | 0.9868 | 0.9860 | -0.0008 | -2.56, -1.25, -2.08 | 0.00 | 0.24 |
| dc | 2425 | 1.0044 | 1.0035 | -0.0009 | -1.25, +0.41, -1.50 | 0.00 | 0.00 |
| dc | 2526 | 1.0135 | 1.0132 | -0.0004 | -2.80, -1.40, -2.65 | 0.00 | 0.00 |
| dc | 2627 | 1.0395 | 1.0388 | -0.0007 | -1.71, -0.53, -2.25 | 0.00 | 0.00 |

Out of sample, pre-close, all seasons pooled (n=6766): log loss 0.9771 to 0.9766, change -0.0005.
Out of sample, dc, all seasons pooled (n=6766): log loss 1.0112 to 1.0106, change -0.0006.
Closing price log loss on the same rows: 0.9745.

Rows with Max and Avg pre-close prices, by league and season:

```
season  2425  2526  2627
div                     
D1       304   305    34
E0       380   380    50
E1       549   550    93
F1       305   305    44
I1       377   379    50
N1       304   305    62
P1       305   304    61
SC0      228   228    41
SP1      379   378    66
```
