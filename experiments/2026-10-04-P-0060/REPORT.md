# P-0060: live-panel-skill, one JSON config to an animated diagram mp4

Harvest H-0124. Repo ythx-101/live-panel-skill, fetched as a tarball into `sandbox/p0060/`. Standard
library Python, plus Chrome (headless, temp profile under the sandbox via TMPDIR) and ffmpeg 
(`/usr/local/bin`). Harness `run_probe.py`, raw output `results.json`.

## Measured

- `render.py` on `examples/codex-agents/config.json`: exit 0 in **142 s**, 900 frames, 1200x1500 at
  30 fps, H.264 plus a silent AAC track, 30.0 s, 1.98 MB. The mp4 stays in the sandbox (gitignored);
  the self-contained live page is here as `codex-agents.html`.
- `check_frames.py --repeat`: exit 0 in **5 s**. 124 time points measured from the DOM, 0 problems.
  Four exported times re-screenshotted after seeking elsewhere: 0 pixels differ, max channel delta 0.
  PNGs in `frames/`.

## Verdict

Works, as claimed. The render is slow (about 6 frames a second, one screenshot per frame over the
DevTools pipe) but deterministic, and the determinism check is the part worth borrowing: seek away,
seek back, compare pixels. HyperFrames already composes video here; this does not replace it, but
the replay check is a cheap test any seek-based renderer should pass.
