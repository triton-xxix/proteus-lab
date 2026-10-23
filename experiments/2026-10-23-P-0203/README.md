# P-0203: track_edges.py on a known 2 percent sway

Nightly probe, 23 Oct 2026, from harvest H-0374 (rossark0/rossark-motion-skill: animation rules for
agents plus three small tools). `tools/track_edges.py` claims to measure motion too small to see on a
contact sheet ("a 2% squash, a 5-pixel sway") by printing a subject's edges frame by frame. Standard
library plus ffmpeg, 4 KB, read before running; copied to `sandbox/rossark-motion/`.

## Called shot

works at 0.60; measured sway 2.0 plus or minus 0.5 points. Commit e19dc22.

## Method

`sway_test.py` renders 120 frames at 60 fps, 500 by 400: an orange rectangle (160 by 240) whose centre
sways sideways by exactly 2.0 percent of frame width peak to peak (10 px) at 1 Hz and bobs by 1.0
percent of frame height (4 px) at 0.5 Hz, drawn with area-coverage anti-aliasing so edges land between
pixels. Encoded twice: lossless (libx264 qp 0, yuv444p) and ordinary (crf 18, yuv420p, which halves
chroma resolution and is what a downloaded reference clip looks like). The tool was run as its docstring
says, `python3 -I`, colour EB781E, tolerance 60, one column for the top edge and one row for left and
right. Its table was parsed and compared with the known positions.

## Numbers

| encode | sway measured | bob measured | widths seen | centre error mean / max | tool time |
|---|---|---|---|---|---|
| lossless | 10 px = 2.00% (true 2.00) | 4 px = 1.00% (true 1.00) | 158, 159 | 0.50 / 0.75 px | 0.48 s |
| crf 18 yuv420p | 10 px = 2.00% | 4 px = 1.00% | 157, 158, 159 | 0.48 / 0.83 px | 0.45 s |

## Reading

The shot's number was hit with no margin needed: 0.0 points off on both encodes. The tool is integer
pixels, so its floor is the half-pixel error you see in the centre column, and the width wobble of one
or two pixels is anti-aliasing plus chroma subsampling, not motion. For the job it is written for
(telling whether a reference is holding still or breathing by 2 percent) that is plenty. Compression
did not hurt it at crf 18.

## Not done

No real footage, no textured subject, no colour close to the background (tolerance 60 on a flat orange
against near-black is the easy case). A subject whose colour varies across its body, or a camera
move, would need the colour list and the run length tuned, and the tool has no help for choosing them.
