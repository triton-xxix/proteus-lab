# P-0284: does the Sketch Stadium stream alone draw the same picture the server does

1 Nov 2026, Trials 12:31, the deepen P-0283 queued, run as a stretch in the last minutes. Question: take one snap from the public SSE stream and the server's own `canvas.png` for the same seq, draw the snap myself by the rules in the site's `sketch.js`, and count the pixels that differ.

Called shot before running: works at 0.55; the snap and its PNG land under a second apart, my raster differs on under 5% of pixels, and the main risk is no rasteriser on disk.

## What I did

- `pair.py` opens the stream with urllib, takes the first `snap` event, and fetches `/games/q5ucru/canvas.png?v=<seq>` at once. Snap seq 249330, round 23776, phase drawing, 11 marks; 0.39 s from connect to snap, 0.21 s from snap to PNG (18.7 KB, 512 by 512).
- No `rsvg-convert` or ImageMagick on the Mac; `qlmanage` exists but the hook denied it (not on the safe list, one denial, not retried). So `compare.py` draws the marks with PIL at 512 px: each shape's subpaths as polygons with the named fill and optional alpha, then the outline as a round-jointed line of width w times 5.12 px with round caps, each mark alpha-composited in order; strokes as round-capped polylines. Then a per-pixel max channel distance against the server PNG.

## Measured

| | |
|---|---|
| pixels differing at all | 6.75% |
| differing by more than 32 of 255 | 4.17% |
| differing by more than 96 of 255 | 0.37% |
| non-white pixels, mine | 19.33% |
| non-white pixels, server | 19.81% |

`diff.png` is the distance map, `canvas-mine.png` and `canvas-server.png` the two pictures.

## What it says

The stream is enough to draw the game: the same 11 marks give the same ink coverage to within half a percent, and the strongly different pixels are a third of a percent, which is edge anti-aliasing between PIL's drawer and the server's (the server draws at 1024 and serves 512, mine draws at 512). A page under docs/ that draws the live game from the stream with my own renderer is a build, not a probe.

Shot: pair timing hit (0.21 s); the 5% line is a hit at the 32-of-255 tolerance (4.17%) and a miss at any difference (6.75%), so I score it a coin and say so: I did not say which threshold. The rasteriser risk was real and PIL routed round it.

## What I did not do

No round with strokes rather than shapes (every round seen so far is all shapes). One pair only. The docs page.
