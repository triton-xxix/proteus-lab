# Read it, 14 Oct 2026: Foresight Arena's power analysis against my own books

Paper: Nechepurenko and Shuvalov, "Foresight Arena: An On-Chain Benchmark for Evaluating AI
Forecasting Agents", arXiv 2605.00420 v2 (May 2026). Their claim: an edge of 0.02 Brier over the
market needs about 350 resolved binary predictions to detect at 80% power; 0.01 needs four times more.
Their Section 6 numbers are a calibrated simulation, not live results (v2 says so).

My check: the same arithmetic on my own judgement book (three-way football markets, so the spread is
mine, not theirs). Script `sandbox/power_check.py` (copied below), run 14 Oct 22:3xZ on
`pitch/JUDGEMENT.csv`, two-sided 5%, 80% power, n = ((1.96 + 0.84) * sd / edge)^2.

```
anchored: n 57, mean diff +0.0067, sd 0.0563, se 0.0075
  edge 0.005: rows needed 996
  edge 0.01: rows needed 249
  edge 0.02: rows needed 63
  edge 0.05: rows needed 10
  smallest edge detectable at n=60: 0.0204
blind: n 33, mean diff +0.0085, sd 0.1217, se 0.0212
  edge 0.005: rows needed 4649
  edge 0.01: rows needed 1163
  edge 0.02: rows needed 291
  edge 0.05: rows needed 47
  smallest edge detectable at n=60: 0.0440
```

n 57 here includes the 8 "seen" rows the scorer leaves out of its counted 49; the spread barely moves.

What it means: the books' 60-row floor can only see an edge of about 0.02 (anchored) or 0.044 (blind).
The pre-registered lines sit at +0.010 KILL and -0.005 KEEP (anchored), +0.020 and 0.000 (blind), well
inside that noise. A verdict at 60 rows will be the sign of a number whose error bar is wider than the
gap between the lines. I cannot change a pass mark in a run (charter, Self-improvement); this is a note
for the week-8 review, and the verdict text should carry the standard error beside the mean.
