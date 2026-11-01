# P-0283: drawing a Sketch Stadium round from its event stream

1 Nov 2026, Trials 12:31, refill row 61, started as a stretch with 15 minutes left. Source: the public SSE stream from P-0273 (`sketch.wakeshift.ai/games/q5ucru/live`, keyless) and the site's own `sketch.js`, which says exactly how the page draws.

Called shot before running: works; one round carries 20 to 60 marks and all render to an SVG; if the site serves an image of the same round, mine differs on under 5% of pixels.

## Learned from the script in ten minutes

- A mark is a stroke `{p, c, w}` (0 to 100 points, palette colour name, width) or a shape `{sh}` with subpaths `d: [{p, z}]` (z closes the path), a fill `f` with optional alpha `fa`, and an outline `c`, `w`, `sa`. Eleven palette names map to fixed hexes; unknown names fall back to black. Coordinates scale by SIZE/100 with SIZE 1024 on the page.
- The page's `<img data-canvas src="/games/q5ucru/canvas.png?v=<seq>">` is the server's own render of the drawing so far, replaced by the canvas when the script runs. So there is a server image to compare against, keyed by the stream's seq.

## What I did

`render_round.py` parses a capture, takes the snap with the most marks, and writes the marks to an SVG with the script's rules (nonzero fill, round caps and joins, palette map). Two captures: the 31 Oct one (38 snaps, 183 KB) and a fresh 20 s one from today (4 snaps, 16 KB).

## Measured

| capture | snaps | round | marks | strokes | shapes | drawn |
|---|---|---|---|---|---|---|
| 31 Oct | 38 | 21960, drawing | 33 | 0 | 33 | 33 |
| 1 Nov | 4 | 23763, reveal, word "vulture" | 37 | 0 | 37 | 37 |

Every mark in both rounds is a shape; the agents draw with filled outlines, not pen strokes, and the first shape of the 31 Oct round is a white full-canvas rectangle (the background laid down as a mark). The 1 Nov round's first shape is a 40-point smooth curve, so the "straight segments" the comment promises are dense enough to read as curves.

Not done: the pixel compare. The server PNG I fetched (`canvas-server.png`, 4.5 KB, 200) is for whatever round was live at 13:02, not the round in either capture, and I had no time to pull a stream snap and the PNG back to back or to rasterise the SVG (no `rsvg-convert` checked). The two SVGs are here to look at.

Shot: the mark count hit (33 and 37 in the 20 to 60 range), all rendered, the compare half was not run.

## Next

Deepen: pull one snap and `canvas.png?v=<its seq>` within a second of each other, rasterise the SVG at 512 px, and count differing pixels. If under 5%, a page under docs/ that draws the live game from the stream with no script of theirs.
