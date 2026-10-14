# P-0148: switch the Pitch's Dixon-Coles fit to the analytic gradient

Question: P-0136 wrote an analytic gradient for the desk's objective (refit 21 s to 0.4 s, same
objective, parameters up to 0.02 apart on a flat ridge). Does the backtest agree to 0.001 Brier?

Method: `compare.py` calls `pitch/backtest.py`'s own `run_group` (weekly walk-forward) for the dc model,
season 2025-26, all eight groups, once as the desk was and once with `model.fit` swapped for
`dc_grad.fit_grad`. Nothing written in `pitch/backtest/`. `predictions.csv` here holds both runs.

Result (`result.json`): 3,134 matches, all with a closing price.
- 1X2 Brier: finite-difference 0.60528, analytic 0.60528. Market close 0.5853.
- p_home moves: largest 0.0031, mean 0.00003.
- In-sample log-pool weight on the model against the close: 0.00 for both (the model adds nothing to
  the closing line in 2025-26, same as the desk's backtest report).
- Wall time: 685 s against 30 s, about 23x.

Shot: works at 0.75, Brier under 0.0005 apart: hit (0.00000).

Done tonight: `pitch/model.py` fit now uses the gradient (4e21eb6), checked on ENG after the edit: 0.11 s,
converged, objective within 2e-6 of P-0136's fit. Dated implementation note in `pitch/RULES.md` (same
commit). Tonight's predictions were committed before the switch; from 15 Oct the nightly uses it.
Next: close. The full three-season backtest can now be rerun in under two minutes when it matters.
