# P-0543 skill-distill extract_session.py with both leak fixes, on five transcripts

Nightly 2026-11-22, refill 229, following P-0536 (two leaks in the unpatched script).

## What I ran

`patched.py` loads `sandbox/skill-distill/extract_session.py` twice: as shipped, and patched in memory
(`scheduled-task` added to the INJECTED regex; tool results passed through `INJECTED.sub`). Both ran on
the five newest Proteus transcripts other than tonight's. Only counts are written (`results.json`); the
extracted text was never saved, so nothing private lands in the repo.

## Result

| session | raw marker lines | shipped | patched | email-shaped strings (patched) | ~/.claude paths (patched) |
|---|---|---|---|---|---|
| 9aedcd25 | 22 | 2 | 0 | 0 | 0 |
| d03e4f04 | 40 | 6 | 0 | 0 | 1 |
| 1c91d4f8 | 20 | 2 | 0 | 0 | 0 |
| bc122616 | 20 | 2 | 0 | 0 | 0 |
| 44dd8d9b | 38 | 2 | 0 | 1 | 1 |
| total | 140 | 14 | **0** | 1 | 2 |

## Verdict: works, with a new edge

The two one-line fixes take marker lines from 14 to 0 across five sessions. But on a scheduled run
the first user message is the wrapper, so once it is stripped the "task" comes out empty (four of
five), and on d03e4f04 the next user message, a `<task-notification>` block, becomes the task. So a
third fix is needed for scheduled sessions: add `task-notification` to the list, and fall back to
the first tool-read prompt file as the task. Still in the output: one email-shaped string and two
`~/.claude` paths, all inside tool commands or results (not printed here); the script cannot know
which of those are private, which is why its README keeps raw logs out of git.
