# P-0028: anidoodle, byte-identical output across two runs?

Run 30 Sep 2026, scheduled nightly, attempt 1 of 3.

## What I did

- Pulled the codeload tarball with curl (git clone is not an unattended verb), extracted with the
  venv's tarfile into `sandbox/anidoodle/`: 957 entries, 595 `.ts`, 87 `.mjs`. Rendering is
  TypeScript on canvas, so a run needs node, which the unattended hook does not allow (npm was
  denied on P-0021 half an hour earlier; I did not spend a second denial proving node is the same).
- Static slice instead: grep for `Math.random`, `Date.now`, `performance.now`,
  `crypto.getRandomValues` across `.ts` and `.mjs`.

## What the grep found

- 15 distinct files per copy (the engine ships twice, under `skills/` and `plugins/`). None is in
  the drawing code under `src/canvas-core/` except `music/sfxCore.ts`, where the hit is a comment
  saying it reads no clock.
- `src/hosts/page.ts` uses `performance.now` only to time a frame, not to draw it.
- `tools/gate.mjs` is a lint that fails the build on `Math.random`, `new Date`, `Date.now`,
  `performance.now`, `ctx.filter`, network and image/font loads in art-core modules, and checks every
  rng call is seeded. There is a `test/fixtures/math-random.mjs` to prove the gate trips.

## Verdict

Blocked on node in a scheduled run. The source is built for determinism and polices it in code,
which is more than most repos claiming it. What the source cannot show is the claim that matters:
"identical on every machine". Canvas rasterisation (antialiasing, font hinting) can differ between
GPUs and Skia builds even with fixed inputs. Interactive test: render one still twice on this Mac
and hash both, then compare against a hash from a different machine if one is ever available.
