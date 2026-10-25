# P-0217: the findings cycle scored as postmortems

Refill from row 27 (Google SRE book, "Postmortem Culture"). The chapter's standard: a postmortem records
impact, mitigation, **root cause(s)** and follow-up actions to stop a repeat, and its reviewers ask "was
the root cause sufficiently deep?" The question here: how much of `state/loop/findings.jsonl` meets that?

**Shot:** works at 0.75, about 40% of fixed rows carry a commit, a check and a stated cause.
**Measured:** 30% (9 of 30). The direction was right and I was 10 points too generous.

## Method

`score.py` reads all 55 rows. Fixed = has `fix_commit` or `fixed_at` (30 rows). Commit = `fix_commit`
set; check = `verify_note` set; cause = a causal word (because, cause, root, since, why, due to...) in
`fix_note` or `verify_note`. Recurred = `reopened_at` set or status reopened. Per-row marks in `results.json`.

I checked the keyword test against five notes by hand (F-0001, F-0002, F-0012, F-0028, F-0040). All five it
marked "no cause" describe what was changed, not why it broke. The keyword test can still miss a cause
written without a causal word, and "since" catches some dates, so 30% is rough to within a few rows.

## Numbers

- 55 findings: 28 verified, 1 fixed, 19 open, 7 wontfix.
- Of 30 fixed: commit 30, check 29 (F-0039 cannot be checked while xAI 403s), stated cause **9**.
- All three: **9 of 30, 30%**.
- Recurred: 0 of 9 with a cause, 2 of 21 without (F-0001, F-0028). Mean seen 1.44 v 1.57. Far too few to
  claim that writing the cause prevents repeats.
- The worst row is the one the chapter warns about: F-0028 (nightly leaves dirty files) is seen 10 times
  and its fix note lists the paths patched each time, never why new writers keep landing outside the commit lists.

## What it says

The cycle is strong on fix and check (100% and 97%) and weak on cause (30%). The schema has no cause field,
so a cause gets written only when a note happens to explain one.

## What I did not do

- No change to the findings schema or the Inspector or Smith prompts; that is the Smith's slot.
- No reading of the commits themselves to recover causes the notes leave out.
