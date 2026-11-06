# Scoring the number in a called shot

Fixed and committed before any shot was scored under it (Workshop, 6 Nov 2026). Every called shot carries
a number written before the probe ran. The verdict word has been scored since 9 Oct; this scores the number.

Each shot gets one score:

- **hit**: every claim in the number holds.
- **partial**: the number makes two or more claims, at least one holds and at least one misses.
- **miss**: no claim holds.
- **unscored**: the probe never measured it (blocked, or a different quantity was measured), or neither the
  verdict note nor the artefact folder settles it. An unscored shot leaves the denominator; the count of them
  is printed beside the rate.

What "holds" means:

- A threshold or a range ("at least 10 points", "under half", "between 2 and 5") is read literally, no tolerance.
- A point value, with or without "about", holds if the measured value is within 25% of it, relative.
- A percentage or share stated as a point value holds within 5 percentage points instead. A wider allowance of
  the two is never taken.
- A wrong sign is a miss whatever the size.
- A count ("3 of 4") is a point value: within 25% of the stated count.
- A word claim ("the render is the likely drift") holds only if the note or the artefact says so plainly.
- If the probe measured a variant of the quantity (a different window, a subset), score it on what was measured
  and say so in the reason. If the variant is too far off to compare, it is unscored.

A shot's own wording of what happened does not bind the score. If a note says "hit" and the rule says miss, it
is a miss.

For the chart: where the first claim is a point value with a number on both sides, record `said` and `got` as
plain numbers in the same unit.
