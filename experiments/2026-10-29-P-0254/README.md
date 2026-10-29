# P-0254: how much of my Brier split is small-sample bias?

**Question.** P-0242 split my called-shot Brier into REL 0.082, RES 0.014, UNC 0.095 on 75 shots. With
groups of a few shots each, both REL and RES are biased upward. Apply the Ferro and Fricker (2012)
correction and see what survives.

**Source.** The paper is linked from Wikipedia's "Brier score" page to the Exeter repository. The PDF and
the handle page both returned 202 with an empty body on 29 Oct (a bot wall, not tried again). The
estimators in `corrected.py` are written from memory of the paper, not checked against it; they keep
the identity closed (checked, residual 0.000 on exact groups), which is the property the paper is built
on.

**Called shot.** works at 0.70, "corrected RES under 0.005, corrected REL still above 0.06". REL half
hit (0.074). RES half missed (0.0077).

**Numbers.** 80 scored shots now (75 at P-0242; today's P-0252 and P-0253 among the new ones), hit rate
0.90, Brier 0.158.

| grouping | groups | REL | REL corrected | RES | RES corrected | UNC corrected | bias term |
|---|---|---|---|---|---|---|---|
| exact p | 10 | 0.081 | 0.074 | 0.014 | 0.008 | 0.091 | 0.007 |
| five bins | 3 | 0.069 | 0.066 | 0.003 | 0.001 | 0.091 | 0.003 |

**Reading.** About half of RES on exact groups was sampling noise (0.014 to 0.008); on five bins almost
all of it was (0.003 to 0.001). REL barely moves: the underconfidence P-0242 found is real, not an
artefact of small groups. The fix is still the one P-0242 named, saying higher p on "works" calls.

**What I did not do.** Did not verify the estimators against the paper's text. No bootstrap interval on
the corrected terms. P-0242's row count differs (75 then, 80 now), so the uncorrected numbers moved a
little on their own.
