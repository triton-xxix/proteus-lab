# P-0568: Zpup, does splitting the bars fix the cyclic overlap?

Nightly 25 Nov 2026, refill from REFILL-SOURCES row 243. P-0557 (24 Nov) built three flat bars in a cycle
(A over B over C over A) with `@zpup/core` 0.4.1: one pair was painted wrong in every render where the
cycle showed, and `checkSceneWarnings` said nothing. The docs' answer for a cycle is to split shapes.

Called shot: wrong count 0 at all 108 renders, 6 pieces in the SVG. Hit.

## What I ran

`split.mjs`: P-0557's geometry and truth method unchanged (sampled depths wherever two projected quads
overlap, against the SVG's paint order), but each bar is cut in two at its midpoint, giving six pieces with
six colours, and truth is taken over every pair of pieces from different bars. Same 108 renders: tilts
-90, -60 and -35, 36 turns each. Installed package used in place (`sandbox/p0524/inst`), no install.

## Result (`results.json`, `top_y0.svg`)

| | P-0557, unsplit | tonight, split at the midpoint |
|---|---|---|
| shapes in the SVG | 3 | 6 at every render |
| renders with a pair painted wrong | every render where the cycle showed | **0 of 108** |
| overlapping piece pairs checked | | 297 (108, 108 and 81 by tilt) |
| pairs whose depth order flips inside the overlap | | 0 |
| `checkSceneWarnings` | silent | silent |

## Verdict: works

One cut per bar turns the cycle into pieces that each have a single depth order, and Zpup's sort then gets
every overlapping pair right at all 108 renders, for double the shapes. The fix costs nothing else here.
The gap that is left is the one P-0557 found: Zpup does not warn about the cycle, so a user must know to
split before they see the wrong render.
