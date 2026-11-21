# P-0524: Zpup and the small box on the big floor

Question: does Zpup (Show HN, 21 Nov 2026) keep a small object visible on a big floor at four angles,
with no script in the SVG? The README's claim is that Zdog sorts by one point per shape, so a big
floor covers small things once they sit farther away than its centre; Zpup compares overlapping pairs.

## What I ran

`npm install @zpup/core` (0.4.1, no install scripts) in `sandbox/p0524/inst/`, then `test.mjs`:
a 300x300 flat floor and a 20 px box near each of its four corners, each viewed at four turns
(y = 0, 90, 180, 270, tilt -30), 16 renders. A box is visible if every one of its pieces is painted
after the floor in the SVG. Also one `renderSpinSvg` turning file. Output `results.json`,
`c120_120_y*.svg`, `spin.svg`.

## Result

- 16 of 16 renders paint the box after the floor, including the 8 where the box sits on the far
  half, which is the case one-point sorting gets wrong.
- 0 of 17 SVGs contain a script. The turning file is 14,955 bytes and animates with SMIL alone.
- I did not run Zdog beside it (its comparison lives in the repo's bench and needs a DOM shim), so
  the "Zdog fails here" half is the author's, not mine.

## Verdict

Works, on the case it was built for. Small next step if wanted: a cluttered scene (many small
solids touching) where pairwise sorting can meet a cycle.
