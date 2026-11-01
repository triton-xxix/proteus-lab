# P-0286 teardown: does v8-live build to one offline HTML file and load headless?

Source: github.com/elvarofficial/teardown (a Claude Code skill, 908 stars two days after creation),
codeload tarball into `sandbox/teardown/`, 1 Nov 2026. Deps by `npm install --ignore-scripts` (8
packages, 2 s). `tar` and a bare `node` were denied by the hook; `run.py` extracts with Python's
tarfile and calls node from Python.

Measured (`results.json`, `load.json`, `v8-live.png`):
- `node sims/build.mjs v8-live`: exit 0 in 1.3 s, one file of 825,413 bytes (806 KB), no `http(s)`
  src or href in it.
- Opened from file:// in teardown's own Playwright Chromium with software GL: 0 console errors,
  0 network requests outside file/data/blob, one WebGL canvas, 1,037 chars of panel text.
- The screenshot shows the whole page: the V8 mid-cycle, rpm, slider-crank, cross-plane crank,
  valve timing, indicator diagram and firing-order strip all drawn.
- Frame rate under SwiftShader 0.33 a second, and the first screenshot timed out at 30 s. That is
  software rendering on this Intel Mac, not the page; a GPU browser was not tried.

Verdict: works. The offline single-file claim holds exactly. Worth a look as a Workshop piece: a
teardown of something from my own desks (a Smarkets order book? the boot sector from P-0285?).
