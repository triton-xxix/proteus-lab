# P-0370: does kubai-icons really hold 2,600+ icons under an MIT licence?

Question from the harvest (H-0573). Repo description says 2,600+, its README now says 2,800+ and "nearly 900 objects, plus badged and slashed off versions".

## Method

`count.py` reads the git tree and licence files from GitHub, keyless. `published.py` lists the npm tarball of `kubai-icons-static` 0.2.0 without extracting it or running anything from it. Saved: `results.json`, `published.json`, the licence texts.

## Numbers

| What | Count |
|---|---|
| Files in the repo tree | 1,181 |
| Files under `icons/` in the repo | 915 |
| `.svg` files in the repo | 1 (a site asset) |
| Distinct icon names in the npm package | 2,871 |
| SVG files in the npm package | 5,742 (two styles, `svg` and `svg-soft`, 2,871 each) |
| Names that are another name plus a suffix | 2,095 (73%) |
| Names with no parent name | 776 |
| Names ending `-off` | 69 |

Top suffixes: check 308, plus 252, x 217, clock 136, alert 119.

## Licence

- `LICENSE-ICONS` is the plain MIT text and covers the icons and the four packages. The npm package carries the same text and says MIT.
- `LICENSE` covers the agent skill and says source-available, not open source. `LICENSE-SITE` is all rights reserved.
- GitHub's API reports the repo's licence as `NOASSERTION`, because the root file is the custom one.

## Reading

The count holds in the published package, and the icons are MIT. The repo itself does not hold 2,600 icon files: it has 915 files under `icons/`, and I did not open them to see how the rest are produced. The 2,871 is a count of names, and about 73% are a base name plus a badge. The real drawing count is nearer the 776 to 900 range. The README says so itself, so that is disclosure and not a catch.

The headline repo, the skill, is not MIT. Anyone reading "MIT" and copying the skill is wrong about what they may do.

## Not done

Did not render any icon, did not check that the variants differ visually from their parents, did not install the skill. The suffix split is a name match, so a few real objects will be counted as variants (for example names ending in `up`, `down`, `right`).
