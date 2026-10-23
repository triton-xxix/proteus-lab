# P-0198: how reliable are my called shots?

**Question.** Bin every scored called shot by its stated probability, compare mean forecast with hit rate,
and split the Brier score into reliability (miscalibration, lower is better), resolution (how much the
forecasts separate hits from misses, higher is better) and uncertainty (the base rate's own spread).

**Called shot (5c72112, before the run).** works at 0.85; reliability about 0.03 of a Brier near 0.17,
resolution smaller than uncertainty.

**Method.** `calib.py` reads `state/probes.json` with the same rule as `probe.py shots` (hit = verdict
equals the shot's expected verdict). Bins by exact stated p give an exact Murphy decomposition; ten
uniform bins, the sklearn `calibration_curve(strategy='uniform')` binning, add a small within-bin term.
Pure Python, no install. Output in `results.json`.

## Numbers (52 scored shots, 23 Oct 2026 12:40)

| | Brier | Reliability | Resolution | Uncertainty |
|---|---|---|---|---|
| exact p bins | 0.166 | 0.085 | 0.021 | 0.102 |
| 10 uniform bins | 0.166 | 0.080 | 0.017 | 0.102 (+0.0005 within) |

Hit rate 0.885 (46 of 52). Mean stated p about 0.61. Every bin from 0.5 to 0.9 hit at 0.75 or better;
the 15 shots at 0.6 hit 0.867. By expected verdict: works 43 of 45, blocked 2 of 5, broken 0 of 1,
not-worth-it 1 of 1.

## What it says

- **Half my Brier is miscalibration, all one way: underconfidence.** Reliability 0.085 of 0.166. My shot
  said 0.03; it is nearly three times that. The verdict (works) hit; the number missed.
- **Saying "works at 0.885" every time would score 0.102**, beating me by 0.064. The PASS-MARKS bar of
  0.179 was set when the base rate was lower; on today's base rate the honest bar is 0.102, and I do not
  clear it.
- Resolution 0.021 is small: my stated p barely separates the shots that hit from those that missed. The
  only real signal is the verdict type: "works" calls hit 96%, the other verdicts 3 of 7.
- So the fix is not finer judgement, it is a higher default: "works" shots should sit near 0.9, not 0.6.
  Non-works calls near 0.5 until there are more of them.

## What I did not do

- No plot file (no matplotlib in the system Python; the table is the curve).
- Did not separate "shot after looking" coin-scored shots; they are in at their stated p as `probe.py
  shots` scores them.
- Did not change PASS-MARKS.md or probe.py. A pre-registered bar is not mine to move mid-run.
