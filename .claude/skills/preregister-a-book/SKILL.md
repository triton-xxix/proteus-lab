---
name: preregister-a-book
description: Start a new Proteus paper book or pre-registered test properly - rules, KEEP and KILL lines and a due date written and committed before the first data point - so the result cannot be bent later. Use whenever a probe earns a book, a new prediction habit starts, or any test is written down to be scored later.
---

# Pre-register a book

The charter's first must: every prediction and paper trade committed before the outcome is knowable,
and every book given pass marks before its first scored row. Patterns: `systems/RULES.md` (P-0083),
`exchange/RULES.md`, `grinder/graduates/RULES.md` (G1 killed on its own line, 3 Oct), the judgement
book's blind column in PASS-MARKS.md.

## Order (all in one commit, before any row exists)

1. **RULES.md in the desk folder:** what is traded or predicted, the universe fixed in advance, entry
   and exit or the call format, fills and costs, what counts and what is excluded, and the scorer.
2. **The lines:** sample floor, KEEP, KILL, INCONCLUSIVE, and a horizon at which anything not KEEP is
   KILL. Write them in RULES.md or as a section of `PASS-MARKS.md`, and add a row to PASS-MARKS.md's
   "Log of changes to this file" (date, change, tightened or loosened, rows it would have judged: none).
3. **A DUE.md row** with a backstop date (a data condition alone never fires):
   `| D-0NN | YYYY-MM-DD | what | where the rule is | condition, backstop YYYY-MM-DD | | |`
4. **Wire the check:** if the book has a nightly kill line, add it to `bin/killcheck.py`; if it is a
   one-off test, `bin/duecheck.py` already reads DUE.md.
5. Commit by named path: `python3 /Users/triton/PROTEUS/bin/commit.py -m "pre-register <book>: rules and lines before the first row" <paths>`.
   The commit hash is the proof; quote it in the probe note.

## Rules that do not bend

- Lines are never changed after the first row except to tighten, and every change is logged.
- Rows seen before registration are excluded and named (the judgement book's J-0001 to J-0008).
- No unattended run edits a kill line, a pass mark or a registered rule (charter v3 draft,
  Self-improvement). Fixing the scorer is allowed; moving the target is not.
- A losing book is published in the same place and format as a winning one.
