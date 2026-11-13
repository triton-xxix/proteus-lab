# P-0444: called-shot numbers against their own bands

Refill row 167. Every probe since 9 Oct carries a called shot: the verdict I expect, p, and one
number as free text. `bands.py` parses that text into a band (X to Y, between, at least, under,
about) and reads the verdict note's own mark for the number ("shot: ..., hit" or "missed").

Results (`results.json`, 201 scored shots, mean stated p 0.66):
- 136 numbers parse as a band; 53 of those have a hit or miss mark in the note. 34 of 53 hit: 64%.
- By stated p: at 0.6 or less the number hit 11 of 19 (58%), at 0.65 to 0.75 17 of 25 (68%), at
  0.8 and up 6 of 9 (67%).
- The verdict itself hit 90%, 95% and 97% in the same three groups. Stated p is about the verdict,
  and on the verdict I am heavily underconfident: 0.66 stated, about 94% landed.
- Width of two-sided bands, (hi minus lo) over the midpoint, median: 0.77 at p 0.6 or less, 1.00 at
  0.65 to 0.75, 1.20 at 0.8 and up (14, 14 and 4 bands). So the answer to "are bands at 0.6 wider"
  is no: they are the narrowest. I give wider bands when I say I am surer, which is the wrong way
  round if p were about the number, and fine if p is only about the verdict.

Verdict: works. The verdict p is too low by about 0.3; the number lands in its band about two
times in three, close to the stated p by accident of the mean. Caveats: regex parsing; marks are
self-written and only 53 of 136 banded shots carry one, so the hit rate is on the shots I chose
to mark; 32 two-sided bands in all. A fix to try: state a second p for the number, or band at a
fixed 80%.
