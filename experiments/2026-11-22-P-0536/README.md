# P-0536 skill-distill extract_session.py on a real Claude Code session

Nightly 2026-11-22, harvest item gh:sybil-solutions/skill-distill (repo created 21 Nov 2026).

## What I ran

- Fetched `skills/skill-distill/scripts/extract_session.py` (main branch, 291 lines, stdlib only, no
  network calls; read in full before running) to `sandbox/skill-distill/`.
- Ran it with `python3 -I` on today's Trials session transcript (session d03e4f04, 124 tool calls).
  Output kept in `sandbox/skill-distill/trials-ref.md` (gitignored: it carries machine paths).
- Counted lines matching seven system-text markers (`system-reminder`, `Contents of /Users`,
  `userEmail`, `SCHEDULED TASK`, `scheduled-task`, `Attribution for git`, `gitStatus`) in the raw log
  and in the output.

## Result

| | raw transcript | extracted reference |
|---|---|---|
| marker lines | 40 | 6 |
| CLAUDE.md / memory / email / git status blocks | present | 0 |
| scheduled-task wrapper | present | 2 lines (kept as the "task") |
| system-reminder inside tool results | present | 4 lines |

It reported 124 tool calls, 7 tool errors, 3 user turns and 16 files written.

## Verdict: works, with two leaks

The injected context blocks (CLAUDE.md contents, auto-memory, user email, git status) are stripped
completely. Two kinds of harness text survive:

1. The `<scheduled-task ...>` wrapper is not in its INJECTED list, so on a scheduled run the "task"
   is the scheduler's boilerplate plus the pointer, including the local path of the task file.
2. `clean_user` is applied to user text only; `<system-reminder>` blocks inside tool results
   (four "file exists but the contents are empty" warnings here) pass through.

Both are one-line fixes (add `scheduled-task` to the regex; run results through `INJECTED.sub`).
Neither leaked anything private in this transcript, but a reminder carrying memory text inside a
tool result would. The "Final answer" section was empty because the session ended on a tool call.
