# P-0067: 3d-asset-server, how many of its 19 sources answer "low poly tree" keyless?

Run 7 Oct 2026, about 00:28 to 00:36, unattended nightly. Harvest item H-0152.

## What I could not run
The server itself: TypeScript, 11 runtime dependencies including native `sharp` and `resvg`, built
with `tsc`. npm is off the unattended list, so it never started.

## What I ran
`sources.py` here: the search endpoints copied from its `src/providers/*.ts`, called directly with
Python, no keys. Seven of the 19 sources; the 3 "linked" ones (Fab, Poliigon, TurboSquid) are
link-only by design (the README's "honest about what's blocked"); 9 were left untested for time.
Output in `results.json`.

## Numbers
- 7 of 7 answered HTTP 200 keyless, 0.2 to 7.9 s.
- BlenderKit: 1,314 free results for the query, first three titled "Low poly tree", licence field
  `royalty_free` on each. The only source tested that gives a licence per result in the search reply.
- Poly Haven: 521 models, 33 tree hits by name or tag, CC0 site-wide.
- itch.io: 162 asset cells on the search page; licence only on each item page.
- ShareTextures: 1,665 tags including "tree" and "pine-tree"; the provider maps query words to tags.
- Kenney and Quaternius: catalogue pages mention trees 9 and 30 times (both CC0 sites).
- ambientCG: 0 results. It is materials and HDRIs, so a model query is the wrong question for it.

## Verdict
works, for the slice. The sources are real and open: 6 of 7 tested have tree assets, 2 with an
explicit licence (BlenderKit per item, Poly Haven site-wide CC0). The aggregator itself is untested
here; running it needs npm in an interactive session.
