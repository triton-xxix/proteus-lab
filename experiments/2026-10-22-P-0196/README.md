# P-0196: HyperFrames variables, three ads from one composition

From the harvest (vault thread "tweak knobs on every composition", H-0364). Question: can one
composition render three distinct per-business ads from a variables file with no edit to its HTML?

Setup: hyperframes 0.7.109 (the pinned copy in `sandbox/p0192/hf`). A 3-second 1280x720 card in
`sandbox/p0196/ad/index.html` declares three variables on `<html data-composition-variables>`
(business, offer, accent colour) with defaults; its script merges the defaults with
`window.__hfVariables`, which the renderer injects. `batch.json` here holds three made-up trade
businesses. `run.py` lints, renders the default, then `render --batch batch.json --output row-{index}.mp4
--strict-variables`, then samples each output at 2.5 s.

Result (`results.json`, frames `*.png`):

- Batch render rc 0, 30.7 s for three draft renders (about 10 s each, 90 frames); default 13.1 s.
- Four outputs, four distinct frame hashes. The accent stripe measured 252,121,56 / 59,175,251 /
  176,106,254 against requested #ff7a3d / #3dafff / #b46bff; row-1's frame shows "Brook Street
  Plumbing" and its offer line. index.html sha identical before and after.
- Lint failed with 3 errors: each variable entry needs a `label` field. The render did not care,
  even with `--strict-variables`. So lint is stricter than render here; add labels.

Verdict: works. The batch flag takes a JSON array of rows and an `{index}` placeholder in the
output path; no per-row HTML, no wrapper script. Not tested: fonts or images as variables, a
row with a missing value, and anything above draft quality.
