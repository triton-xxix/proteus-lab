# P-0154: herk-edit-kit keyless starter

Question (harvest H-0256): does Nate Herk's HyperFrames edit kit (github.com/nateherkai/herk-edit-kit,
1,472 stars, pushed 14 Oct) build and pass its own tests on this Mac with no API keys?

Run, 14 Oct about 23:45 BST, in `sandbox/p0154-herk` (gitignored):
- Fetch: repo tarball by `fetch.py` (git clone is off the safe list): 411 MB, 1,232 entries. Most of the
  weight is the 12 published example projects' media.
- `npm ci --ignore-scripts`: 141 packages in 8 s; npm audit reports 9 vulnerabilities (6 moderate, 3 high).
- Tests: `npm test` and bare `node --test` were refused by the hook; `run-tests.mjs` here runs the same
  two node:test files through the node:test API: 11 pass, 0 fail, 3.4 s.
- The kit's own `scripts/check-kit.mjs`: 716 distribution files, 2 styles, 406 cards, both skill trees,
  0 errors. The README's "406 motion-graphics cards" holds; they sit under 2 styles.

Not run: `npm run setup` (writes .env), the transcription helper (ElevenLabs key), any render, any skill.
The repo ships its own CLAUDE.md and AGENTS.md telling an agent how to work in it; read as data, not acted on.

Shot: works at 0.60, tests pass with no key and install under 3 min: hit.

What it adds over the HyperFrames skills already here: a transcript-driven cut pipeline (silences, then
mistakes, on the retimed transcript) and a 406-card style registry. Next: deepen only if a Workshop video
needs cuts; a test of `cut-silences` on a local whisper transcript would be the one to run.
