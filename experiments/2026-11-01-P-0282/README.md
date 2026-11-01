# P-0282: pixelfx's own checker on all 244 effects

1 Nov 2026, Trials 12:31, refill row 60. The repo (pulled as a tarball for P-0272 on 31 Oct) ships `tools/check.mjs`, which the README says catches "spills, seams, unseeded randomness, slow frames". It takes a category name or `category/effect` ids and runs on node with no dependencies. The README gives no pass count and no run time for the whole library.

Called shot before running: works; 244 checked, 0 fail, about 10 with warnings (seams and slow frames), the whole library in about 75 seconds.

## What I did

`run_check.py` runs the checker once per category (21 categories), times each, and parses the summary line and the warning lines into `results.json`. One pass on this Intel Mac, nothing else running.

## Measured

| | |
|---|---|
| effects checked | 244 |
| pass | 244 |
| fail | 0 |
| with warnings | 19 |
| whole library | 445.7 s |
| per effect, median category | about 1.1 s |
| slowest category | weather, 121 s for 12 effects (10 s each) |
| next slowest | explosions 59.5 s (5.0 s each), moves 34.7 s (2.9 s each) |
| fastest | pickups 5.0 s for 11 (0.45 s each) |

Every one of the 19 warnings is the same kind: `slow: N ms a frame`, from 4.0 (lightning/storm-cloud) to 7.7 ms (weather/storm). Eleven of the twelve weather effects warn (all but one), two explosions, two transitions, and one each in ice, lightning, scifi and water. No spills, no loop seams, no unseeded randomness, no missing meta: the author's checker finds nothing structural in the author's effects, which is what a checker run before every commit would show.

## What it says

The library is clean by its own test, and the test is slow: seven and a half minutes for one pass, dominated by the particle-heavy weather and explosion categories, which are also the ones that warn. A 5 ms frame is 150 ms of a 30 fps second on this machine; whether that matters depends on how many weather effects a game layers.

Shot: the verdict and 0 fail hit; 19 warnings against my 10 and 446 s against my 75. I timed nothing before calling the time, and the fire category I had just run took 18 s, which I read as "a few seconds". The warning kind I called (seams and slow frames) was half right: slow frames only.

## What I did not do

No second pass to see how much of the 446 s is node start-up per category (21 launches) against effect work. No render of the warned effects to see whether 7 ms a frame is visible. The Claude Code skill in the repo is still untested (interactive only).
