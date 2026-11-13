# P-0441: does cinematic-skill's starter explainer render here, and how long does it take?

Harvest H-0643. Moh4696/cinematic-skill, main, fetched as a tarball 13 Nov 2026 (no installer run).
skia-python 144.1 installed into `sandbox/py312-venv`; the skill's `check_setup.py` said ready
(ffmpeg with libx264, macOS fonts, `say` as scratch voice, 8 workers on 16 GB).

Steps, the README's order: `new_project.py` (template "From Cherry to Cup"), `tts_say.py` (macOS
say, 3 takes), `split_takes.py` (6 lines, median 17.07 letters a second, 0 flagged),
`build_narration.py` (23.70 s narration), `render.py --size 1280x720` with the narration.

Results:
- First render hung. The README says the template "renders" once it has a scratch voice, but it
  also needs `prep_assets.py` (the studio texture). Without it each of the 8 workers printed
  `image 'studio.png' not found ... run prep_assets.py` and exited, and the parent sat on 8
  header-only chunks (262 bytes each) for 628.9 s until I ended it (`render-hung-before-prep.json`,
  `kill_hung.py`). A still render (`--probe`) fails cleanly with the same message; the parallel
  path does not exit.
- After `prep_assets.py` (9 textures, 0 photos): 710 frames, 1280x720, 30 fps, h264 plus AAC,
  23.67 s, 27.3 MB, in 47.6 s wall on this Intel Mac with 8 workers (1.9 to 3.0 frames a second per
  worker). About 2 s of render per second of film at 720p. `render-1280x720.json`, `still-12s.jpg`.

Verdict: works, with one bug worth reporting upstream: a missing prepared asset hangs the parallel
render instead of failing it, and the template's quick start skips the step that makes the asset.
Not tested: the documentary example (needs Wikimedia fetches), 1080p, sound effects and captions.
