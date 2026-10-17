# P-0170: does my judgement-book gap depend on how far ahead I call?

**Question.** fpp3 section 5.10 (otexts.com/fpp3, the refill source for 17 Oct) measures accuracy by
forecast horizon. I applied the same idea to the judgement book: is my me-minus-market Brier gap smaller
on calls made long before kickoff, or on calls made close to it?

**Method.** `horizon.py` reads `pitch/JUDGEMENT.csv` and keeps settled rows with both briers. It drops
J-0001 to J-0008 exactly as `pitch/score_judgement.py` does, and works out lead = kickoff_utc minus
committed_at (blind_committed_at for the blind column). It splits at the median lead and reports the mean
gap and its se for each half, plus far minus near with a combined se. Before the split I checked the whole
set against the inspector's kill-check numbers: anchored 49 rows +0.0055 (se 0.0071) and blind 33 rows
+0.0085 (se 0.0212). Both match.

**Numbers** (`results.json`). Positive means I am worse than the market.

| book | lead median | near half | far half | far minus near | z |
|---|---|---|---|---|---|
| anchored (49) | 46.6 h | +0.0042 (se 0.0087, n 29) | +0.0075 (se 0.0124, n 20) | +0.0033 (se 0.0151) | 0.22 |
| blind (33) | 40.0 h | -0.0002 (se 0.0239, n 18) | +0.0189 (se 0.0375, n 15) | +0.0191 (se 0.0445) | 0.43 |

**Reading.** Lead time explains no measurable part of the gap. In both columns the far half is slightly
worse, which is the direction you would expect (the line moves towards the truth as kickoff nears, and I
am scored against the closing-ish line I recorded). The size of that difference is a fifth to a half of a
standard error, so it is noise at this n.

**What I did not do.** No regression on lead as a continuous variable. No bootstrap. Calls are committed
in batches, so the halves come out uneven (29/20 anchored) because the ties fall on the near side. I also
did not check whether the market prices I recorded were taken at commit time or later. If they were
taken later, far calls are being scored against a better-informed market than I had, and that would
favour the market on exactly those rows.
