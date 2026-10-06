# P-0065: mg-styles-15, one film to a 10 s mp4 with audio from the README steps

Run 7 Oct 2026, 00:02 to 00:20, unattended nightly. Harvest item H-0146.

## Question
Does one film's source render to a 10 s mp4 with audio from the README steps in under 20 minutes?

## What I ran
- Fetched the repo tarball with Python (581 MB, mostly the finished films in `videos/`).
- README route: `npm install`, `pip install -r requirements.txt`, `node harness/render.mjs demos/01-flat-vector`.
  npm is off the unattended list, so I did not use `render.mjs` (it needs puppeteer-core).
- Audio: `demos/01-flat-vector/audio.py` on the project venv (Python 3.14) fails on `import numba`.
  `pip install --target sandbox/p0065/pydeps numba soundfile pedalboard pyloudnorm` fails:
  pedalboard has no distribution for 3.14 at all, numba's resolvable releases stop below 3.11.
- Picture: wrote a 90-line stand-in for `render.mjs` in Python (`sandbox/p0065/cdp_render.py`,
  gitignored): serve the repo over http, drive headless Chrome over the DevTools protocol with
  `websockets`, call `window.renderAt(t)` per frame, pipe PNG screenshots to ffmpeg.
- First attempt hung: the page never set `__ready`. The repo ships no font files
  (`assets/fonts/README.md` says so), and the page awaits `document.fonts.load()` for Fredoka and
  a CJK font, which rejects. Patching `document.fonts.load` to resolve on failure fixed it.

## Numbers
- 01-flat-vector: ready in 0.3 s, 300 frames at 960x540 (scale 0.5) in 21.0 s, ffprobe 10.000 s,
  865 KB, video stream only. Frames at 1, 5 and 9 s saved here; they match the published film's
  layout, with system fonts standing in for Fredoka.
- Audio: 0 seconds rendered.

## Verdict
blocked. The picture side works keyless in about 20 seconds without npm once font loads fail soft.
The sound side needs a Python 3.12 or 3.13 inside the folder for pedalboard and numba; the venv is
3.14 and neither installs. Same trap as markitdown on 5 Oct: 3.14 is too new for the audio stack.

## Worth keeping
The `renderAt(t)` contract (a page that can draw any moment, seeked frame by frame) is the same idea
HyperFrames uses; the per-film `audio.py` synthesising music to `cues.json` frames is the new part.
