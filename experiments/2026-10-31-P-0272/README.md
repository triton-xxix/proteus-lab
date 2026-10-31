# P-0272: pixelfx, the 244 claim and determinism

31 Oct 2026, nightly probe loop. Source: harvest H-0471, github.com/patch-gg/pixelfx (1,382 stars, created 30 Oct 2026, JavaScript, MIT).

Called shot before running: works; the count lands between 232 (the harvest title) and 244 (the README), and same-seed renders match.

## What I did

- `fetch.py`: pulled the main branch tarball (12.5 MB, 349 entries) into `sandbox/pixelfx-src/` with urllib and tarfile; no git clone in a scheduled run.
- Counted effect files under `src/fx/<category>/` excluding `_lib.js`, `index.js` and `categories.js`, by the GitHub tree API and again from the extracted tree.
- Rendered three effects with the repo's own `tools/render.mjs --sheet` (no npm install; the tool uses its own PNG writer) three times: run1 and run2 with the default seed, run3 with `--seed 7`. One simulated effect (fire/torch, 60 frames), one long simulated one (explosions/big-explosion, 217 frames) and one pure `draw(p, t)` effect (transitions/iris, 67 frames).
- `check.py`: decodes each sprite-sheet PNG to raw RGBA in stdlib Python and compares pixels, not file bytes. Results in `results.json`.

## Measured

| | |
|---|---|
| effect files in `src/fx` | 244 (README says 244; the harvest title's 232 was the repo a day earlier) |
| categories | 20, from 10 (ice, holy, spawn, transitions) to 13 (fire, nature, water, projectiles, status) |
| by export | 120 `create` (simulated), 112 `draw` (pure, frame from `t` alone), 12 moves that chain effects |
| file size | median 6.6 KB, 1.2 KB to 22.8 KB |
| same seed, run1 v run2 | identical pixels on all three sheets (sha256 equal, 518k, 24.2m and 4.0m pixels) |
| other seed, run1 v run3 | torch 74% of pixels differ, big-explosion 12%, iris 1% |

The pure effect still changes with the seed (1% of pixels), so "pure" means frame-from-time, not seed-free; the sheet's actor or dither takes the seed. Each render took a few seconds; big-explosion's 217 frames made a 4.9 MB sheet.

## Verdict

works. The claim is exact and the renders are deterministic for a given seed, in Node 18+ with no dependencies installed. What I did not test: the Claude Code skill (draft, render, look, refine), which needs an interactive session; and whether the effects look good, which is a pixel artist's call and no script's.
