# P-0557: Zpup and a three-way cyclic overlap

## Question

P-0524 showed `@zpup/core` 0.4.1 sorts a small box on a big floor right, 16 of 16. Its docs say shapes
are compared where they overlap on screen, that truly intersecting shapes cannot be drawn, and that
`checkSceneWarnings` flags shapes passing through each other. They say nothing about three shapes that
never touch but overlap in a cycle (A over B over C over A), which no single back-to-front order can paint.

## Method

`cycle.mjs`, node, the copy already installed in `sandbox/p0524/inst/` (no new install).

- Three flat filled bars (closed 4-point `path`s) along the sides of a triangle, each rising 30 units
  from start to end and extended 30% past each corner. At every corner the arriving bar is 30 units
  above the leaving one. Nothing touches.
- Truth: my own copy of Zpup's rotation (z, then y, then x). Checked against the SVG: the red bar's
  first corner is (177.09, 69) in both. For each pair, 369 sample points on one bar, depth compared with
  the other bar's plane wherever the point lands inside its projected quad.
- Paint order read from the SVG. A pair is wrong if the nearer bar is not painted after the farther one.
- 36 turns (every 10 degrees) at three tilts: straight down (x -90), x -60, x -35.
- Clutter: 30 separated boxes on a 6 by 5 grid, random sizes, 36 turns at x -30, `checkScene` and
  `checkSceneWarnings` on each.

## Numbers

| tilt | renders | all three pairs overlap | renders with a wrong pair | wrong pairs |
| --- | --- | --- | --- | --- |
| -90 | 36 | 36 | 36 | 36 |
| -60 | 36 | 36 | 36 | 36 |
| -35 | 36 | 9 | 9 | 9 |

- Every render where the cycle is on screen paints exactly one pair wrong: the minimum any single order
  can do. Every render where it is not (27 at -35) is right. No bar is ever split (1 SVG piece per bar).
- `checkSceneWarnings` on the cycle: 0 issues. On the clutter scene: 0 warnings, 0 invalid, 36 of 36.
- Clutter paint order was not scored against truth (box faces need per-face geometry; not done).

## Called shot

broken at p 0.7: "at least one wrong pair in 36 of 36 top-down renders, 0 warnings for the cycle".
Measured 36 of 36 and 0 warnings. Hit.

## Reading

Not a bug in the sense of a mistake: no linear painter can do this without splitting a shape, and the
docs' advice ("split them into smaller shapes") is the fix. The gap is that the warning check is silent
on it, so a user finds out by looking. Splitting each bar in two at its midpoint should fix it; that is
the obvious deepen, not run here.

## What I did not do

No split-bar fix, no score of the clutter scene's face order, no issue filed upstream. No browser.
