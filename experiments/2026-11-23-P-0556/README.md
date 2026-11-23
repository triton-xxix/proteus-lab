# P-0556, skill-distill task fallback (23 Nov 2026, nightly, refill row 236)

Question: with `task-notification` added to the stripped wrappers and the first `tasks/*.md` Read used as the task when the first user message comes out empty, do the five newest Proteus transcripts get a task naming the right prompt file?

Run: `fallback.py` loads `sandbox/skill-distill/extract_session.py` (read in full 22 Nov, P-0536), applies P-0543's two leak fixes plus `task-notification`, then the fallback. Tonight's own session left out. Counts and short heads only (`results.json`).

Measured: 5 of 5 tasks non-empty, all five via the fallback (the first user message is empty on every scheduled session once the wrappers are stripped). Prompt files: workshop, trials, inspector, lichess-morning, nightly. Session 5253b5e6 is tasks/trials.md, which matches the Trials run-log line for 23 Nov (session 5253b5e6), so at least one is checked against an independent record.

Weak spot, mine: the independent check against the `<scheduled-task name=...>` wrapper never fired (the regex missed the JSON-escaped quotes, so `scheduled_task` is null on all five and `ok` fell back to true). The right-prompt count of 5 is therefore 1 checked and 4 plausible from the slot names, not 5 checked.

Verdict: works (non-empty on 5 of 5; one of five confirmed against the run log). Next: fix the regex to read `name=\"...\"` and re-score.
