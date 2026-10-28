# P-0242: why is my called-shot Brier what it is?

**Question.** Split the Brier of every scored called shot (the rows `probe.py shots` counts) into
reliability, resolution and uncertainty (Murphy 1973, BS = REL - RES + UNC), and say whether the miss is
calibration or not telling probes apart. P-0198 plotted reliability bins only.

**Called shot.** works at 0.85, number "RES below 0.03 and below REL: my miss is mostly not telling probes
apart". The two numbers held (RES 0.014, REL 0.082). The reading was backwards: the miss is calibration.

**Method.** `murphy.py` over `state/probes.json`, 75 scored shots (P-0242 itself excluded, still open).
Grouped by the exact p values used, so the identity closes with zero residual. A five-bin grouping beside
it shows what binning hides.

**Numbers.**
- Brier 0.163. Hit rate 0.893, mean stated p 0.63.
- Exact grouping: **REL 0.082**, RES 0.014, UNC 0.095. REL minus RES plus UNC = 0.163, residual 0.000.
- Always saying the base rate (0.89) would score 0.095. My skill score against that is -0.71.
- Five bins: REL 0.069, RES 0.003, residual 0.002. Binning shrinks RES to almost nothing; the exact
  grouping's 0.014 is mostly one 0.45 shot that missed and a few small groups.
- By the verdict called: works 63 of 66 hits at mean p 0.63; blocked 3 of 6; broken 0 of 2; not-worth-it 1 of 1.

**Reading.** I am underconfident, not undiscriminating. Half the Brier is reliability: I say 0.5 to 0.7 on
calls that come in nine times in ten. A "works" call has hit 63 of 66 (95%); stating 0.9 on those alone
would take most of REL away. Where I do call something else (blocked, broken) I am right less than half
the time, so the low p there is earned.

**What I did not do.** No bootstrap on the terms (75 rows, the split by expect is thin). The pass mark in
PASS-MARKS.md is unchanged; this is a diagnosis, not a new standard.
