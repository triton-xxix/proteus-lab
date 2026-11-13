# P-0439: guizang-game-skill's single-HTML packager on a toy three.js game

Harvest H-0638. Question: does `scripts/build_single_html.mjs` (op7418/guizang-game-skill, main,
fetched as a tarball 13 Nov 2026) bundle a toy three.js scene with zero network requests, and at
what size?

What I ran (all in `sandbox/p0439/`, gitignored; the scripts are copied here):
- `extract.py` unpacks the tarball (tar is not on the unattended safe list).
- `prep.mjs` builds the folder layout the packager expects: one 2048px JPEG ground texture, two UI
  PNGs, one ink JPEG, a 3,362-vertex grid GLB as a prop, a 1 s sound effect and a 20 s 192k music
  file (ffmpeg), three 0.170.0 vendored, and a `src/game.js` that reaches each asset the usual way:
  GLTFLoader (fetch), TextureLoader (an `<img>`), `fetch()` for the sound and JSON, `new Audio()`
  for the music. Dependencies pinned: gltf-transform 4.1.1, meshoptimizer 0.22.0, sharp 0.33.5,
  esbuild 0.24.2, installed with `--ignore-scripts`.
- `run_build.mjs` runs the packager unchanged. 1.5 s.
- `check.mjs` runs the HTML's inline fetch shim against a recording fetch and replays each load.

Results (`results.json`):
- `dist/wusuo.html` 1,233,434 bytes for 0.49MB of shrunk assets (ground texture cut from 2048 to
  1024px, music re-encoded to 88k) plus 0.58MB of minified code; the static site and its 2048px HD
  set came to 3.31MB beside it.
- All 9 assets are inside the file. The 3 loads that go through `fetch` (GLB, sound, JSON) hit the
  shim's data URLs with 0 network calls. The HTML's own `<img src="assets/ui/...">` was rewritten
  to a data URL; no stray src or href remains.
- The shim wraps `window.fetch` only. three's TextureLoader in the bundle makes an `<img>` and sets
  its src to the path as written (found in the minified bundle: `let o=ls("img")` in the image
  loader), and `new Audio()` does the same, so those two loads are requested from disk or the
  network and fail when the file is opened alone. This part is read from the bundle and the shim's
  code, not observed in a browser (the browser pane is barred in a nightly run).

Verdict: works, with a hole. The packager inlines everything and the fetch path is airtight, but
"no network requests" holds only for a game that loads every asset through fetch; a texture via
TextureLoader or music via `new Audio()` slips past. Their own demo may well route everything
through fetch or GLB-embedded textures; I did not have its source. Next check, in an interactive
session: open the toy's `wusuo.html` from `file://` with the network off and count failed loads.
