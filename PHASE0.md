# Phase 0: Luke's one sitting

Steps 1 to 5 done 2026-09-22 (settings in place, repo public, Pages live at
https://triton-xxix.github.io/proteus-lab/, charter signed, card in 1Password tagged `proteus`,
five API items tagged). One step left.

## 6. Load the two scheduled runs, from a session opened IN this folder

A scheduled task inherits the working folder of the session that creates it. Created from a vault
session, the runs start in the vault, the Proteus hook never applies, and the first write raises a
prompt nobody answers (this happened on the first attempt tonight; both tasks were deleted). So:

1. In the Claude desktop app, start a **new session with the folder set to `/Users/triton/PROTEUS`**
   (not the vault).
2. Paste this, exactly:

```
Read scheduled-tasks/proteus-nightly/SKILL.md and scheduled-tasks/proteus-weekly/SKILL.md. Create two scheduled tasks with create_scheduled_task using each file's body (everything below the frontmatter) as the prompt and its description line as the description: taskId proteus-nightly, title "Proteus nightly expedition", cronExpression "15 23 * * *"; taskId proteus-weekly, title "Proteus Sunday Field Notes", cronExpression "0 18 * * 0". Then call run_scheduled_task on proteus-nightly once as the proof run, wait for it, and report whether state/unattended-session.json ended as "closed" and how many denials state/unattended-decisions-<today>.jsonl holds.
```

3. Confirm in the Scheduled section of the sidebar that both show, then check
   `/Users/triton/PROTEUS/state/runs/` for the proof run's log.

After that, nothing else needs you until Sunday's email.
