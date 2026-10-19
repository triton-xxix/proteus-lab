# P-0181: imozuru's verbatim-excerpt check

Source: harvest H-0336, github.com/MaryCache/imozuru (MIT, 759 stars, created 13 Oct 2026). A Claude Code
research skill that saves source texts unsummarised and cites claims by file and line. Its `report.py`
refuses to build the reading page if any excerpt is not word for word in the source at the stated lines.

Fetched as a tarball with `fetch.py` (no git clone), into `sandbox/p0181-imozuru/`. `run.py` builds eight
variants of the repo's own demo and runs `report.py --check` on each. Results in `results.json`.

| Case | rc | As the README says? |
|---|---|---|
| original demo | 0 | yes |
| one word swapped, darkest to lightest | 1 | yes |
| one digit swapped, 9 of 12 to 8 of 12 | 1 | yes |
| whitespace and line breaks changed | 0 | yes, normalised on purpose |
| line number off by 2 | 0 | yes, two lines of slack |
| line number off by 4 | 1 | yes |
| ellipsis drops "fewer" so the claim flips | 0 | **no** |
| path traversal `../extracts.json` | 1 | yes |

Verdict: works, 7 of 8. The one-word claim holds for substitutions. The gap is the "…" splice, added for
two-column PDFs: each piece only has to appear in order within the window, so an excerpt can omit the
word that carries the meaning ("darkest tone first produced… visible seams") and still pass. The page does
show the "…" and the source lines beside it, so a reader can catch it; the machine does not.

Use for me: the pattern (store the source, cite by line, verify mechanically, refuse on mismatch) fits the
Nolan children's "every claim sourced" rule better than my current URL-only check. A fix for the gap
would cap how much text one "…" may skip, or reject an omission that removes a negation or comparative.
