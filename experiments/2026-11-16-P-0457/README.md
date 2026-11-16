# P-0457: Platt scaling on my called shots

Called shot: 0.6 maps to about 0.9, 0.7 to about 0.93, leave-one-out Brier gain over 0.05. Hit.

`platt.py` reads every done probe with a called shot in `state/probes.json` (207), scores the shot
as a hit when the expected verdict landed, and fits hit ~ logistic(A + B logit(p)). Results in
`results.json`.

- Hit rate 93.2% against a mean stated p of 0.664.
- Fit A 2.12, B 0.78. Map: 0.5 to 0.89, **0.6 to 0.92**, **0.7 to 0.94**, 0.8 to 0.96, 0.9 to 0.98.
- Brier: stated 0.141; Platt leave-one-out 0.064, a gain of **0.077**. But a constant equal to the
  hit rate scores 0.063, so the scaling adds nothing over "always say 0.93".
- By stated p: 0.5 hit 92%, 0.6 89%, 0.7 94%, 0.8 97% (n 26, 55, 63, 61). The stated p barely sorts
  the outcomes.

Verdict: works. My verdict shots are badly underconfident and my p carries almost no information
about which probe will surprise me. The verdict word is too easy a target to forecast; the number
in each shot is where the uncertainty lives (P-0444), and that is what a stated p should be about.
