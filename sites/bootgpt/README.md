# bootgpt teardown machine (published)

The P-0296 machine (`main.js`, `net.js`, `weights.js`) plus the Workshop's portrait layout of 2 Nov 2026:
when the window is taller than wide it draws a 600x1100 layout with labels only on the pick and the eight
highest logits, so a phone held upright can read it.

- Build: `node /Users/triton/PROTEUS/sites/bootgpt/build.mjs` (kit in `sandbox/teardown`), out to `out/dist/bootgpt.html`.
- Check: `node /Users/triton/PROTEUS/sites/bootgpt/check.mjs` (Playwright, 1600x900 and 375x812) writes
  `results.json` and the two step-161 frames.
- Publish: `python3 /Users/triton/PROTEUS/docs/bootgpt/build.py` copies the machine to `docs/bootgpt/machine.html`
  and writes `docs/bootgpt/index.html` from P-0294's results and screen and this folder's `results.json`,
  exiting if they disagree. Lint with `docs/bootgpt/lint.py`.

Live: https://triton-xxix.github.io/proteus-lab/bootgpt/
