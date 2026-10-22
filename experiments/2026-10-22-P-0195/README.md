# P-0195: molanim (AmadeusBio-ai/Molecular_Animation), the numpy layer without Blender

From tonight's harvest (H-0357). Question: do its numpy-only tests pass on a fresh venv, and does its
motion code move a public structure it was not tested on?

Fetched the main-branch tarball (`fetch.py`, 3.1 MB, 145 files; no git clone) into
`sandbox/p0195/repo`, made a fresh Python 3.12 venv with numpy, Pillow and pytest only.

- `pytest tests`: **60 passed, 1 skipped in 39.9 s.** Slowest: the channelrhodopsin activation
  path 18.2 s, retinal lobes 10.5 s. No Blender on this Mac and none needed.
- `move.py`: `protein_motion` (elastic-network modes plus side-chain turns, 30 modes, 0.8 Å target
  RMSF, 96 frames at 24 fps) on haemoglobin 2HHB chain A (1,112 atoms, from the repo's website
  folder, not used by any test) took 0.14 s; mean RMS displacement 0.92 Å; bond-length error p99
  0.194 Å, max 0.617 Å. Its own test's bar on 9GO1 is p99 under 0.25 and max under 1.2, so 2HHB
  clears it. The 9GO1 rerun: 0.31 s, p99 0.138, max 0.899. Numbers in `move.json`.

Verdict: works, for the pure layer. The physics is cheap (well under a second for a whole shot's
motion on one chain) and keeps bonds to the stated tolerance on a new structure. The films need
Blender 5.2 and its MCP bridge, which I did not install. The idea worth lifting is the evidence tag
per beat (experimental, simulation-derived, illustrative), which would fit the Nolan site and any
HyperFrames explainer.
