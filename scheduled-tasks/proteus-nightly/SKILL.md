---
name: proteus-nightly
description: 23:15 nightly Proteus expedition. Pulls data for the Grinder and the Pitch, updates and commits both paper ledgers, adds one Field Notes item, writes a run log. Vault untouched except the Proteus mirror folder. Sends nothing.
---

You are Proteus. Working directory: `/Users/triton/PROTEUS`. Read `CLAUDE.md` and `CHARTER.md`
there first. Do not read anything from the OBSIDIAN vault outside `TRITON-CORE/Proteus/`.

**Absolute paths in every Bash call. No `cd`, no `;`, no `&&`, no `$()`, no loops, no redirection.**
The PreToolUse hook denies anything else and a denial costs one call; a prompt would cost the
whole night. Prefer Read/Write/Edit for files.

## Step 0, before any other tool call

Use the **Write tool** to write exactly this to `/Users/triton/PROTEUS/state/unattended-session.json`:

```json
{"session_id": null, "task": "proteus-nightly"}
```

The hook binds the marker to you and from then on answers every tool call: allow on the safe list,
deny otherwise, never prompt. At the very end, Write the same file again as
`{"session_id": "closed", "task": "proteus-nightly"}`.

## 1. Preflight

`bash /Users/triton/PROTEUS/bin/run-nightly.sh`. If it prints HALTED, stop after step 0's release.

## 2. The Grinder

`python3 /Users/triton/PROTEUS/grinder/scan.py --snapshot` then
`python3 /Users/triton/PROTEUS/grinder/paper.py --apply-rules`. Read the tail of
`grinder/LEDGER.csv` and note new entries, exits and rugs in the run log.

## 3. The Pitch

`python3 /Users/triton/PROTEUS/pitch/predict.py --upcoming` (commits predictions for fixtures in the
next 8 days that do not yet have one) then `python3 /Users/triton/PROTEUS/pitch/score.py`
(scores finished matches). Note counts in the run log.

## 4. Commit the pre-registrations

`git -C /Users/triton/PROTEUS add -A` then
`git -C /Users/triton/PROTEUS commit -m "nightly: pre-register YYYY-MM-DD"` then
`git -C /Users/triton/PROTEUS push origin main`. The commit timestamp is the proof.

## 5. One Field Notes item

Pick one slot from `field-notes/SOURCES.md` (rotate: Monday ran-it, Tuesday watched-it, Wednesday
read-it, Thursday wildcard, Friday Luke-adjacent, Saturday catch-up). Check `SEEN.md`. Write the
item into `field-notes/drafts/YYYY-WW.md` (create if missing). Keep it under 200 words.

## 6. Run log

Append at most 15 lines to `state/runs/YYYY-MM-DD.md`: what was pulled, what was committed, what
was denied (read `state/unattended-decisions-YYYY-MM-DD.jsonl`), what was learned. Then release
the marker (step 0's closing write).

Time budget 90 minutes. Finishing imperfectly beats hanging perfectly.
