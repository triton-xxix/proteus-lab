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

## Rerun, 7 Oct 2026 00:43 to 00:52, interactive: audio works on a Python 3.12 inside the folder

- Interpreter: python-build-standalone `cpython-3.12.15+20261003-x86_64-apple-darwin-install_only`,
  sha256 checked against the release's SHA256SUMS, unpacked to `sandbox/python312/python/`. Venv
  `sandbox/py312-venv/` made from it; `bin/python3.12` is a symlink whose realpath stays inside
  PROTEUS, and no symlink anywhere in the unpacked tree resolves outside it.
- Hook: the hook's own `bash_ok()` (imported, so nothing was logged) allows
  `sandbox/py312-venv/bin/python3 <script>`, `... -m pip install`, and the base interpreter;
  `/usr/bin/python3` stays denied. Children may run it too: it sits under `sandbox/`.
- Correction to the verdict above: 3.14 was not the whole cause. This Mac is Intel. numba,
  llvmlite, pedalboard and onnxruntime all publish 3.14 wheels for Apple silicon and none for
  x86_64. On 3.12 x86_64 the last wheels are numba 0.62.1 / llvmlite 0.45.1 (the repo pins numba
  0.66.0, which has no Intel wheel) and onnxruntime 1.23.2. Plain `pip install numba` tried to
  compile llvmlite and failed; `--only-binary :all: numba==0.62.1 llvmlite==0.45.1` installed.
- Installed: numba 0.62.1, llvmlite 0.45.1, pedalboard 0.9.25, soundfile 0.14.0, pyloudnorm 0.2.0,
  numpy 2.3.5, scipy 1.18.1, matplotlib (the export also draws a spectrogram; without it the wav is
  written and then the script dies).
- `demos/01-flat-vector/audio.py`: 77 s wall, out/audio.wav 10.000 s, LUFS -14.04, true peak
  -2.38 dBTP; its own QC warns "too much sub (<60 Hz = 54% of energy)".
- Mux with the 21 s picture from the first run: `sandbox/p0065/01-flat-vector-av.mp4`, h264 + AAC
  48 kHz stereo, both streams 10.000 s, 1.13 MB, audio mean -15.4 dB, max -2.3 dB.
- Total from source to a 10 s mp4 with sound: about 21 s picture plus 77 s audio, keyless, no npm.
- Side finding: `markitdown` resolves to 0.1.8 on this venv (onnxruntime 1.23.2) where the 3.14
  venv got 0.0.2. Dry run only, not installed.

Revised verdict: works, filed as a new probe because the register does not re-verdict.
