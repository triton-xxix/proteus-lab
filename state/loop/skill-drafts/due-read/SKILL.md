---
name: due-read
description: Take one pre-registered test from DUE.md to its verdict (KEEP, KILL, INCONCLUSIVE, or a backstop close) with a dated artefact, the row closed and the Field Notes line written. Use when duecheck says DUE, when a finding from source duecheck is on the Smith's list, or when a row's count or backstop has arrived.
---

# Due read

A DUE row is a promise to read a number against a line written before the number existed. The
read changes nothing about the line. Done by hand on 24 Oct 2026 (D-012, `experiments/2026-10-24-D-012/`),
28 Oct (D-014, closed "not launched" by its backstop, F-0061) and 30 Oct (D-018,
`experiments/2026-10-30-D-018/`); this is that procedure.

## 1. Read the row and the rule

- `grep -n "D-0NN" /Users/triton/PROTEUS/DUE.md` gives the row: what, where (the rules file and the
  scorer), due (a count, a date, or both), and the backstop.
- Read the registered lines in the file the `where` cell names (PASS-MARKS.md section, a desk's
  RULES.md, a VARIANTS file). Quote them in the artefact as written. The lines are out of reach: a
  Smith run never edits PASS-MARKS.md, CHARTER.md or a registered rule, however stale its reason looks.
- Read BACKLOG.md first if anything about the row looks wrong; it may already say why.

## 2. Get the number from the registered scorer, nothing else

- Called shots: `python3 /Users/triton/PROTEUS/bin/probe.py shots`.
- Kill-line books: `python3 /Users/triton/PROTEUS/bin/killcheck.py` (no `--log` in a daytime slot).
- Edges: `/Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/edges/edges.py score` then `status`.
- Grinder replays: the harness script the VARIANTS file names, through `/Users/triton/PROTEUS/.venv/bin/python3`.
- A row with no scorer (a launch, a decision of Luke's) closes on its backstop with the outcome
  written plainly, as D-014 did; nothing is invented to fill the cell.
- If the row asks a second question (D-018: "did the stated p move"), write a small script in the
  artefact folder that selects rows exactly as the scorer does and answers it, run it with
  `python3 -I /Users/triton/PROTEUS/experiments/YYYY-MM-DD-D-0NN/read.py`, and keep its output in the README.
  Never recompute the headline number a second way; the scorer's figure is the one that counts.

## 3. Write the artefact

`/Users/triton/PROTEUS/experiments/YYYY-MM-DD-D-0NN/README.md`, in this order: who and when; what
the row said and why the read lands now (count reached, backstop, or late, and if late why);
**Measured** (the scorer's line verbatim); **Lines** (quoted from the rules file with its date);
**Verdict** in one word with the comparison in one sentence; **Said plainly**, the honest reading,
including anything the verdict word hides (D-012: the Brier was held up by underconfidence; D-018:
the always-works baseline had moved and KEEP no longer meant what the rule's author meant). Say what
the next read is, or that none is registered. A new read wanted is a new DUE row with a backstop,
never a sentence in the README alone.

## 4. Close the row, record, commit

1. `python3 /Users/triton/PROTEUS/bin/duecheck.py --scored D-0NN "YYYY-MM-DD <slot>, experiments/YYYY-MM-DD-D-0NN/README.md: VERDICT at <n>, <number> against <line>; <one more clause>"`.
   The cell is one table cell: commas are fine, a `|` is not.
2. A KILL or KEEP on a book with a rules file: a dated verdict paragraph in that RULES.md (the
   nightly's rule, step 7). Called shots have no rules file of their own and PASS-MARKS.md is out of
   reach, so the README and the DUE cell carry the verdict; say so in the run log.
3. One line under `## Verdicts` in `/Users/triton/PROTEUS/field-notes/drafts/YYYY-Www.md`: id, what,
   date, number against line, verdict, the plain reading in a clause, the artefact path in backticks.
4. `python3 /Users/triton/PROTEUS/bin/commit.py -m "<slot>: F-00NN D-0NN <what> <verdict>" /Users/triton/PROTEUS/experiments/YYYY-MM-DD-D-0NN /Users/triton/PROTEUS/DUE.md`
   (and the RULES.md if step 2 wrote one). The draft goes in the slot's closing commit.
5. If a finding fired: `python3 /Users/triton/PROTEUS/bin/findings.py fix F-00NN --commit <hash> --note '<verdict and number>'`
   and the `## I changed myself` line with the revert.

## Traps already hit

- duecheck read only the backstop date until 24 Oct (F-0049), so D-012 landed at 65 not 40; a count
  trigger it does not parse still waits for a reader. Check the count yourself when the cell names one.
- A `$` inside double quotes is denied by the hook; single-quote the note.
- The verdict word and the reason can part company (D-018). Write both; move neither line.
