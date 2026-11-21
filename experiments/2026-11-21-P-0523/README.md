# P-0523: sprite-stacking's slicer on a synthetic four-view sheet

Question: does `views_to_slices.py` (danielwh2/sprite-stacking, created 20 Nov 2026) turn a four-view
sheet into a 36-layer strip and a viewer?

## What I ran

- `fetch.py` pulled the repo tarball keyless into `sandbox/p0523/` (3.3 MB).
- `gen.py` draws a 108x12 px sheet of a small car in one row: top 24x12, side 24x10, front and back
  12x10 (yellow headlamps, red tail lamps, a glass cabin, black wheels).
- Run 1 failed: "Found 1 drawings, expected 4". The slicer grows the mask before finding views, so
  my 2 px gaps merged them. The error said so plainly. 12 px gaps fixed it.
- Run 2, `--order reading --slices 36 --html`: 36 slices of 172x86 px, `check.png`, a 110 KB
  standalone `viewer.html`. But the car came out wrong: reading order is TOP, SIDE, FRONT, BACK
  in the tool's sense, where SIDE is the short end, so my long profile was squeezed onto the end
  and the headlamps landed on the flanks.
- Run 3, default (views matched by proportion), `slices-auto.png`, `check-auto.png`: a recognisable
  car with the cabin set on the body, wheels on the flanks, at four angles and exploded. Still one
  mix-up: with two same-sized end views it cannot tell my front from my side, so headlamps show on
  both ends and the tail lamps on a flank.

## Verdict

Works: 36 layers and a viewer from four small drawings in under a second, NumPy and Pillow only.
Two things a user should know: leave about 10 px between views, and do not trust `--order reading`
to mean your own naming; the proportion matcher got the geometry right and only the paint on the
two end views wrong. The viewer's play modes were not opened (no browser in an unattended run).
