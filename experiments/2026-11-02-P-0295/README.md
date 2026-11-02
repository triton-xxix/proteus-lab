# P-0295: bootgpt's forward pass as a teardown page

**Question.** Can the teardown kit (fetched for P-0286) take apart something of mine rather than an
engine: bootgpt's boot-sector network, one character per step, every number on screen read from the same
integer forward pass that picks the character? And does the page print exactly what the real boot printed?

**Method.** `bootgpt-teardown/` is a kit machine: `net.js` is the integer forward pass from boot.asm (as
P-0294's `match.py` has it) over `weights.js` (weights.bin as base64, from `make_weights.py`); `main.js`
calls `runSim` with the step index as the one input and draws the 8-char context, the 96 hidden units, the
64 logits and the pick on a 2D canvas (HUD and director off). `build.mjs` sets `TEARDOWN_OUT` and imports
the kit's build so nothing lands in the repo root. `check.mjs` opens the page in the bundled Playwright
Chromium, reads `window.BOOTGPT.text` and lays it on an 80-column screen beside P-0294's v86 screen.

**Numbers.** One offline page, 186 KB (`out/dist/bootgpt-teardown.html`), built in 81 ms, loaded headless
in 216 ms with 0 page errors. At seed 0x9e75 (recovered from the v86 boot in P-0294) the page's text
matches all 9 full rows of the emulator's screen, 0 differing, about 378 printed characters. The last
row fails as a prefix only because the page stops at 400 steps and the emulator's screen holds about 406
characters with newlines. `frame-12s.png` is step 161.

**Seen in the frame.** Most of the 96 hidden units sit at the ±64 clip, so the layer works nearly as
binary features.

**Not done.** Not published; negative logit bars overlap the character labels; no live controls (seed,
step slider), no film. 400 steps, not the 406 the screen needs.
