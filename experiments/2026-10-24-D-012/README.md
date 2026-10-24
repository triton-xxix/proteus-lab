# D-012: called shots, first verdict at 40 scored

Smith, 24 Oct 2026 20:15. The row said "first verdict at 40 scored shots"; duecheck read only the
backstop date and showed waiting at 55 (F-0049, fixed tonight), so this read lands at 65 rather
than 40. Numbers straight from `python3 /Users/triton/PROTEUS/bin/probe.py shots`, nothing
recomputed here.

**Measured.** 65 scored, 0 waiting. Hit rate 0.91. Mean stated p 0.63. Brier 0.163.

**Lines (PASS-MARKS.md "Called shots", written 9 Oct before any shot existed).** KEEP at Brier
0.160 or below at 40 or more. KILL above 0.200. Anything between is INCONCLUSIVE until 80 scored,
then KILL unless KEEP.

**Verdict: INCONCLUSIVE.** 0.163 sits three thousandths above the KEEP line and well under KILL.
The habit continues; the next read is at 80 scored shots (D-018 in DUE.md, backstop 2026-11-30 as
D-012 had).

**Said plainly.** The Brier is held up by low stated p's on shots that hit: hit rate 0.91 against a
mean p of 0.63. P-0198 (23 Oct) decomposed an earlier 52 into reliability 0.085, resolution 0.021,
uncertainty 0.102, and found that saying "works" at the base rate every time would score better. So
the number that matters at 80 is whether the stated p's moved up toward the hit rate, which the
Trials prompt has asked for since 23 Oct. Two of today's shots were made after looking at the data
and scored at p 0.5, said so in their notes; they count here as the rule counts them.

The number in each shot is still not scored (PASS-MARKS.md: "not scored until a rule for it is
written here"). BACKLOG.md carries the hit field idea from 21 Oct.
