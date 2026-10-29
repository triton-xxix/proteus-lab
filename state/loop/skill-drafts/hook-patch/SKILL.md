---
name: hook-patch
description: Write, prove and re-check a fix to the unattended hook (.claude/hooks/unattended-decide.py) from a scheduled Proteus run, which cannot edit anything under .claude/. Use in the Smith slot when a finding's cause is in the hook, and every night a hook patch is waiting, to confirm it still applies.
---

# Hook patch

A scheduled run may not write under `.claude/`: the app asks a human before any edit there, whatever
the PreToolUse hook answers, and since 21 Oct 2026 a scheduled prompt is refused outright. On 15 Oct
an Edit to the hook sat unanswered for six days and no Smith ran from 16 to 20 Oct (one session per
task). So the fix is written as a diff beside a proof, checked nightly, and an interactive session
applies it. Done by hand four times (F-0044 on 24 Oct, F-0056 on 26 Oct, re-checks 27 and 29 Oct).

## Write the patch (Smith, once)

1. Find the cause in `/Users/triton/PROTEUS/.claude/hooks/unattended-decide.py` by reading it. Read
   `/Users/triton/PROTEUS/BACKLOG.md` first; the hook section there lists gaps already known.
2. Write a unified diff to `/Users/triton/PROTEUS/state/loop/hook-patches/F-00NN.diff` with the Write
   tool: `--- a/.claude/hooks/unattended-decide.py` and `+++ b/...` headers, paths relative to the
   folder root, correct `@@ -start,count +start,count @@` headers (the checker counts the lines).
   Put the test cases in the same diff as a hunk against `bin/test-hook.py`, so one `git apply` brings
   both. A short "Why" paragraph above the first `---` line is fine; the checker skips it.
3. Prove the logic outside the hook: `/Users/triton/PROTEUS/state/loop/hook-patches/F-00NN-check.py`,
   pure Python that reads no logs and imports nothing from `.claude/`, exit 0 when the old way shows
   the bug and the new way does not. `F-0056-check.py` (date arithmetic across the clock change) is
   the model.
4. Check the diff fits the tree:
   `python3 /Users/triton/PROTEUS/state/loop/hook-patches/check-diff.py /Users/triton/PROTEUS/state/loop/hook-patches/F-00NN.diff`
   One line per hunk, `OK ... (offset 0)` or `MISMATCH` with the first differing line; exit 1 on any
   mismatch. It applies nothing (`git apply --check` is off the unattended list).
5. Leave the finding open. `findings.py fix` is wrong here: nothing has changed in the hook. One run-log
   line names the diff path and the check result, and one line under `## I changed myself` in
   `field-notes/drafts/YYYY-Www.md` says "not applied" with the path.
6. Commit the patch folder with the night's close: `state/loop` is in Smith's final commit.

## Re-check (every Smith while a patch waits)

Run `check-diff.py` on every `.diff` in the folder. All hunks `OK` means the patch still applies; a
`MISMATCH` means something else changed that part of the hook, so rewrite the hunk from the current
tree (the offset tells you how far it drifted). One run-log line: "F-00NN patch re-checked, N hunks OK".

## Apply (interactive session only)

`git apply /Users/triton/PROTEUS/state/loop/hook-patches/F-00NN.diff`, then
`python3 /Users/triton/PROTEUS/bin/test-hook.py` (expect 0 failed), then any action the "Why" paragraph
names (F-0044: `launchctl load` of the E-001 plist), then `findings.py fix F-00NN --commit <hash>`,
and delete the `.diff` and `-check.py`. The hook is live code: do not apply two patches without running
the tests between them.

## Traps

- The checker's hunk header counts are strict: a diff written by hand with a wrong `,count` reads as
  MISMATCH before any line is compared (24 Oct, first F-0044 draft).
- `$` inside double quotes in a Bash call is denied; keep `check-diff.py` arguments bare paths.
- Never test the hook by calling it: `bin/test-hook.py` uses a temp state folder; a stray call against
  the live state folder writes into today's decisions log (memory: decisions log mixes test lines).
