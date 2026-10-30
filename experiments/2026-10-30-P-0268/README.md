# P-0268: a Skool About-page scorer from the Magnetic Memberships audit checklist

From the S-58 Skool reading (30 Oct 2026, verdict TRY). Two halves were asked for: a stdlib scorer
for the eleven rules the owners state in their 5 June 2026 "top 45 earners" video, and a diff of that
checklist against Triton's Launch a Skool framework.

## Half one: the scorer, done

`about_score.py` takes the saved HTML of `skool.com/<slug>/about` (the page embeds its data as
Next.js JSON, fetchable keyless with curl) or a plain-text file, pulls the short description and the
long copy, and grades eleven checks: description length, keyword in the first five words, copy
length, a number in the hook, five to seven bullets, a proof line, a guarantee, a price anchor,
exactly one call to action, no outbound links, and a Flesch-Kincaid grade of 5 to 6. Pages fetched
into `sandbox/skool-about/` (gitignored); a wrong slug returns a 404 page, which scores 2 of 11 and
is easy to spot by its empty description.

| page | score | fails |
|---|---|---|
| Maker School (the audit's own best in class) | 7 of 11 | keyword at word 7 not in the first five; copy 1,003 characters (3 over); no proof line the regex recognises (it has the guarantee but no named results or counts); grade 3.3, under the 5 to 6 band |
| Magnetic Memberships (the audit's authors) | 6 of 11 | no keyword in the first five words; no number in the hook; 11 bullets; no guarantee; no price anchor (it is a free community, so the last two are structural) |

Two readings. The authors' own page fails five of their own eleven rules, three of them because a
free community has no price to anchor and nothing to guarantee: the checklist is written for a paid
page and should carry a "free community" variant. And the exemplar misses the reading band on the
low side once bullets count as sentences; the first version of the grade counted a whole value stack
as one sentence and gave both pages grade 13, which is the kind of false fail a scorer must not ship.

## Half two: the framework diff, not done here

Launch a Skool lives at `TRITON-CORE/Systems/frameworks/` in the OBSIDIAN vault, outside the one
vault folder a Proteus run may read. So the diff waits for an interactive session, which can run the
scorer's rule list (the docstring at the top of the script) against the framework text and list what
is missing. The S-58 digest's own reading is that the keyword, cover-photo and first-25 specifics are
the gaps.

## Verdict

Works for the half that could run: the scorer grades live About pages keyless and already shows the
checklist's authors missing their own rules. The framework diff is blocked on the vault read rule,
not on anything technical.
