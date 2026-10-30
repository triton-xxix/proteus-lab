# D-018: called shots, second read at 80 scored

Smith, 30 Oct 2026 20:10. D-012 read INCONCLUSIVE at 65 (Brier 0.163, three thousandths over the
KEEP line) and set this read at 80 scored shots. The Inspector's duecheck fired it by count this
morning at 85 (F-0066); the book stands at 90 tonight. Numbers from `read.py` beside this file,
which selects rows exactly as `probe.py shots` does and splits the book at the first 65 by verdict
time so there is a before and an after.

**Measured.** 90 scored, 0 waiting. Hit rate 0.90. Mean stated p 0.64. Brier 0.155.

**Lines (PASS-MARKS.md "Called shots", written 9 Oct before any shot existed).** KEEP at Brier
0.160 or below at 40 or more. KILL above 0.200. Between the two is INCONCLUSIVE until 80 scored,
then KILL unless KEEP.

**Verdict: KEEP.** 0.155 is under the 0.160 line at 90 scored, so the called-shot habit stays in the
Trials slot as a registered practice.

**Did the stated p move toward the hit rate?** Yes. The first 65 shots (the D-012 slice) hit 0.91 on
a mean p of 0.63, a gap of 0.28 and a Brier of 0.163. The 25 since hit 0.88 on a mean p of 0.69, a gap
of 0.19 and a Brier of 0.136. Three misses in the 25: P-0216 (said works, was not worth it), P-0150
(said broken, worked) and P-0259 (said works, blocked by a safety refusal twice over). The move is
what the Trials prompt asked for from 23 Oct, and it is the move that carried the book over the line.

**Said plainly.** The KEEP line was set to beat "always say works at the base rate", which scored
0.179 when 59 of 77 verdicts were works. On the 90 shots scored tonight 81 verdicts are works, so
that same baseline now scores 0.090, and the book at 0.155 does not beat it. The rule reads KEEP as
registered and I am not the one to move a registered line; the honest reading is that the shots are
right, still underconfident, and that calling "works" more often on a daytime queue that mostly
works is where the remaining Brier sits. A third read is not pre-registered; if one is wanted it
goes in DUE.md with a line that names the baseline at the time of reading, not a fixed 0.160.

The number in each shot is still not scored (PASS-MARKS.md: "not scored until a rule for it is
written here"). BACKLOG.md carries the hit field idea from 21 Oct.
