# P-0340: claude-animation-skills /graph

Question: does `skills/graph/build.py` turn a JSON spec into an mp4 keyless, and is "about 10 seconds" true?

Method: fetched the repo tarball into `sandbox/animskills/` (no clone, no `install.sh`, nothing linked into
`~/.claude`), fetched GSAP by hand, ran `build.py` twice from `run.py` on my own called-shot counts
(48, 65, 90, 122). npx fetched HyperFrames 0.8.34 itself. Results in `results.json`, sheet beside it.

Measured on this Intel Mac: first run 33.1 s, second 15.6 s, both exit 0. Each mp4 is 1080x1920, 30 fps,
120 frames, 4.000 s, about 156 KB.

Read from the sheet: the count lands on 122 and stays on one line, and the last frame holds it. Two flaws
on a series that does not start near zero. The count opens at 0 while the dot already sits at 48's height,
so the number and the line disagree for the opening frames. The first and last axis labels straddle the
red safe-area edge, partly outside it.

Not done: `npm install` in the kit (three.js and Playwright are not needed by /graph), the other five
skills, and the Instagram safe-area claim beyond reading the sheet.
