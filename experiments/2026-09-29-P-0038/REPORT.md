# P-0038: motion-broll, offline render and determinism

Source: github.com/Barty-Bart/motion-graphics (329 stars, created 25 Sep 2026), harvest H-0059. A
Claude Code skill that plans and renders motion-graphic B-roll from a transcript.

## What I ran (29 Sep, about 23:55 to 00:05 BST)

- `git clone` is denied in a nightly, so the engine (`build.py`, `motion.js`, `base.css`,
  `render.js`, two Geist fonts) and one example clip (`01-opus-drop.html`) came down by curl into
  `sandbox/motion-broll/`. I did not run their `setup.sh` (it pip-installs and npm-installs).
- `build.py` inlined engine, fonts and clip into one self-contained HTML file. No network needed.
- `render.js` drives headless Chromium through Playwright, seeks the page's timeline to four
  subframes per output frame across a 180 degree shutter, pipes PNGs to ffmpeg and blends them
  with `tmix`. I borrowed the Playwright already in `sandbox/hf-student-kit/`; its Chromium revision
  was not in the cache, so a wrapper (`sandbox/motion-broll/run-render.js`) launches installed
  Chrome headless instead. That is a deviation from their setup.
- `render_twice.py` rendered the clip twice and compared.

## Numbers (`result.json`)

- Both renders succeeded: 186 frames, 1920x1080, H.264, 29.97 fps, 6.2 s, 464,106 bytes.
- Wall time 100.9 s cold, 69.6 s warm. So about 11 to 16 seconds of render per second of clip on
  this Mac, with 744 screenshots behind 186 frames.
- The two MP4s have the same sha256 and every decoded frame matches. Byte-identical.
- Motion blur is real but coarse: `frame-5s.png` shows four distinct ghost copies of the cursor
  and the pill edge rather than a smooth smear. Four samples is visible on fast moves.

## Verdict

Works. It renders offline from one self-contained HTML file, and the same input gives the same
bytes, which is what HyperFrames also promises. What it adds is the single morphing shape with a
cursor driving it and a ready library of such clips. What it costs is time: at 11 to 16x real
time, a minute of B-roll is a quarter of an hour of rendering.
