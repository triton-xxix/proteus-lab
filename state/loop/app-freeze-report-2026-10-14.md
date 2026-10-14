# Bug report: scheduled Claude Code session freezes for 4h42m between hook approval and tool execution

Written by Proteus on 14 Oct 2026 for Luke Boyd to send to Anthropic.

## Environment

- Claude desktop app 2.31226.1 (macOS), Claude Code 2.1.296
- macOS 26.7.1 (25G241), Intel Mac, user "triton"
- Sessions started by the desktop app's scheduled tasks (routines) in working directory /Users/triton/PROTEUS
- Auto mode on; a PreToolUse hook (.claude/hooks/unattended-decide.py) answers allow or deny for every tool call

## What happened

Two scheduled sessions, on consecutive days, each froze for 4 hours 42 minutes and then carried on as if nothing
had happened. In both cases the freeze sits between the PreToolUse hook returning "allow" and the tool actually
running. Both runs are marked "succeeded" in the routine's Runs pane.

### Session 1: proteus-workshop, 12 Oct 2026

- Session id e5f407e6-96cf-4bca-b885-9f1696a2c699 (transcript 85b52cf9 in ~/.claude/projects/-Users-triton-PROTEUS/)
- Model claude-opus-5-5
- 15:38:18.720Z assistant issues `mcp__Claude_Browser__navigate` to https://triton-xxix.github.io/proteus-lab/probes/P-0128/
- 15:38:18.810Z hook_success attachment: PreToolUse allowed it
- 20:20:35.103Z the tool_result arrives ("navigated to ..."), 4h42m17s later. The navigation itself had succeeded.
- 20:20:36Z onward the session runs normally and finishes at 20:21:47Z

### Session 2: proteus-smith, 13 Oct 2026

- Session id b8c2db9e-82b0-4bd8-99f7-e0a90e297243 (transcript 296dea3a)
- Model claude-fable-5-1
- 19:07:39.163Z assistant issues an `Edit` on .claude/skills/probe-to-verdict/SKILL.md and 19:07:40.326Z a `Bash` `cat` of a CSV, in one message
- 19:07:39.253Z hook_success attachment: PreToolUse allowed the Edit. No hook record exists for the Bash call.
- 19:09:08.281Z a queue-operation "enqueue" for a background-task notification (a Bash command started earlier with run_in_background had completed)
- 23:51:48.089Z file-history-delta for the Edit, 23:51:48.122Z the Edit tool_result, 23:51:48.516Z the Bash tool_result, 23:51:48.764Z the queued notification is removed. All 4h42m40s after the calls.
- The session then ran normally to 23:53:56Z

## What it was not

- Not sleep. `pmset -g log` shows no sleep or dark wake on either evening; a screen-sharing session held a PreventSystemSleep assertion throughout.
- Not a slow tool. The Edit is a local file write; the Bash was `cat` on a small file; the browser navigate had completed.
- Not the hook. It had already answered allow (the attachment is timestamped before the gap). The hook is a short Python script with no network.
- Not the machine being busy. The app's other scheduled sessions ran normally during the gap (proteus-smith at 19:04Z on 12 Oct ran while the workshop session was frozen).
- Not a one-off. Two sessions, two days, two different tools, two models, the same 4h42m to within 30 seconds, which looks like a fixed internal timeout rather than an external event.

## What never froze

The same routine runner starts a nightly session at 23:23 local every night (proteus-nightly, 22 runs since 22 Sep). It uses the same hook, the same tools and longer runs (up to 80 minutes), and has never shown a gap. The four daytime routines (09:00, 12:30, 16:30, 20:00) are new since 12 Oct; two of their first eight runs froze.

## Files that show it

- ~/.claude/projects/-Users-triton-PROTEUS/85b52cf9*.jsonl (session 1) and 296dea3a*.jsonl (session 2): the timestamps above are in these transcripts
- /Users/triton/PROTEUS/state/unattended-decisions-2026-10-13.jsonl: the hook's own log; its last entry for session 2 is the Edit at 20:07:39 local, nothing for the Bash call that followed
- ~/Library/Logs/Claude/: nothing in remote-control.log, swift.log or ssh.log at the freeze or resume minutes

## Questions

1. Is there a 4h42m (about 16,920 s) timeout anywhere in the tool-execution or permission path of a routine-started session?
2. What runs between a PreToolUse hook returning allow and the tool starting, in auto mode, that could block?
3. Why would the Bash call in session 2 never reach the hook, yet return a result after the gap?
