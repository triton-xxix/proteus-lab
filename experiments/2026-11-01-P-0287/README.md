# P-0287 reanimate: does its recorder extract animations and positions from a public page, keyless?

Source: github.com/NiazMorshed2007/reanimate (Claude Code skill, 731 stars), codeload tarball into
`sandbox/reanimate/`, 1 Nov 2026. Script deps by `npm install --ignore-scripts` (24 packages); its
Playwright 1.64.1 wants Chromium 1248, the user cache has 1234, so the headless shell (104 MiB) went
into `sandbox/ms-playwright/` with `PLAYWRIGHT_BROWSERS_PATH`. `run.py` runs everything from the
scripts folder because the hook allows no `cd`. `ffmpeg-static`'s binary is a postinstall download
that `--ignore-scripts` skipped, so both runs used `--no-video` (inspection and tracking only).

Measured:
- turborepo.com, load trigger, 3 s, tracking `h1, nav`: exit 0, no key, no login. 25 keyframe rules
  read out of the stylesheets, 0 animations running at load, library detected "css scroll-driven
  animations", 3 fonts, 56 per-frame position samples for the two selectors, renderer SwiftShader.
  Files here: `inspect.json` (34 KB), `track.json` (22 KB), `capture.json`, `final.png`.
- The repo's own turborepo-gauge example from file://: exit 0, 1 keyframe rule, 0 running
  animations, 0 samples (no selector given). Its motion is JS-driven, which the getAnimations()
  inspection does not see; that is what the `--clock virtual` and `--gl` modes are for, not run.

Verdict: works, for the recorder's keyless slice. Not run: video and frames (ffmpeg), the compare
loop and the virtual clock. A turborepo hero that animates on scroll explains 0 at load.
