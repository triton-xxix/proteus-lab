# P-0296: the bootgpt teardown page, with controls, checked at two widths

**Question.** P-0295's page ran 400 steps (6 short of the v86 screen), had logit labels under the bars and
no controls. With a seed box, a step slider and 420 steps, does it match the whole boot screen, and does
it hold at phone width?

**Method.** This folder is the machine (`main.js`, `net.js`, `weights.js` from P-0295, `main.js`
rewritten): 420 steps, labels below the lowest bar, a bottom bar with a seed box (hex, forced odd like the
disk's `or dx, 1`), a step slider that takes over from the clock and a play button that hands it back.
`build.mjs` builds with the kit into `out/dist/2026-11-02-P-0296.html`. `check.mjs` opens it in the
bundled Playwright Chromium at 1600x900 and 375x812.

**Numbers.** 187 KB. At both widths: all 10 rows of P-0294's v86 screen compared, 0 full rows differing and
the last row a prefix match (397 printed chars); horizontal overflow 0 px; the slider still at 161 after
300 ms; seed 0x1235 regenerates a different stream; 0 page errors. Frames: `desktop-step161.png`,
`phone-step161.png`.

**Caveat.** At 375 px the 1600x900 drawing scales to fit, so nothing overflows, but the text is too small to
read. It needs a portrait layout before it goes on a phone.

**Not done.** Not published under docs/ (the Workshop's publish skill does that); no portrait layout.
