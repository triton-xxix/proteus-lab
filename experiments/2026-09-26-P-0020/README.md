# P-0020: Reladraw, keyless install and a text diagram to an image

Run 26 Sep 2026, 23:52 to 00:00, from the nightly. Source: harvest H-0013 (Show HN). Script:
`sandbox/p0020_reladraw.py`; everything it measured is in `results.json`, the SVGs and their
`.reladraw` sources sit beside it.

## What I ran

- `npm install --ignore-scripts reladraw`: one package, 0.5.0, no dependencies at all, 1.7 s.
- A 3-node diagram (two children in a group, one database to the right, one labelled edge) from the
  README: rendered to a well-formed SVG, 1,842 bytes, 18 elements, 0.3 to 0.9 s.
- **Deterministic:** rendered twice, identical bytes (same SHA-256).
- **"A gap is a minimum, not an exact distance."** SYNTAX.md's own corridor example. Hub and Side
  alone: 56 px apart. Add a 230 px node wedged between them: 342 px apart, which is exactly
  230 + 2 x 56. The claim holds to the pixel. (Removing it closing them back up is the first
  render, so that half holds too.)
- One doc slip: the README cites `between cluster.desktop1 and cluster.laptop1` as a placement
  statement. On a node, `between` is an error ("is not a direction"); it is an edge clause. Nodes
  go between things with `right of X  left of Y  level with Y`.

## What I did not do

- No PNG: the CLI writes SVG, which is an image; I did not rasterise it.
- Did not test the agent skill (`npx skills add`) or the browser playground.
- Did not render the 44-statement `arch.reladraw` benchmark, which ships in the repo, not the npm
  package.

## Verdict

Works. Zero-dependency, keyless, deterministic, and the headline layout claim measures exactly.
Worth knowing for anyone who wants an agent to edit a diagram by changing sentences rather than
coordinates. Still v0.5 with an unstable syntax and no edge routing around nodes, both stated by
the author.
