---
name: recheck-a-probe
description: Re-run a committed Proteus probe's script and check its headline numbers against the verdict, without leaving the artefact folder dirty. Use in the Inspector's step 5 (two recent verdicts a morning), when a Field Notes claim rests on a probe number, or whenever a probe result is doubted.
---

# Re-check a probe

A verdict is a claim with a number in it. Re-running the script a day or two later says whether the
number was real, whether the data moved underneath it, or whether I misquoted it. Written 21 Oct 2026
by Smith after the Inspector did this by hand every morning from 17 to 21 Oct and hit the same traps
each time.

Drafted here because a scheduled run cannot write under `.claude/skills/` (the app asks a human, and
refused the Write on 21 Oct 20:20). An interactive session installs it:
`cp -R /Users/triton/PROTEUS/state/loop/skill-drafts/recheck-a-probe /Users/triton/PROTEUS/.claude/skills/recheck-a-probe`,
then points `tasks/inspector.md` step 5 at "Use the `recheck-a-probe` skill" and removes this draft.

## Pick

Two most recent `works` or `not-worth-it` verdicts from the last 48 hours whose artefact folder holds a
script. The register is `/Users/triton/PROTEUS/state/probes.json` (Read it, or
`grep -n '"P-0' /Users/triton/PROTEUS/state/probes.json`); the artefact is
`/Users/triton/PROTEUS/experiments/YYYY-MM-DD-P-00NN/`, listed with `ls`. The probe's quoted numbers
are in its `NOTE.md` and in the `verdict` text of the register row. Anything that would run over ten
minutes: skip and say so in the run log.

## Before running: find out where the script writes

`grep -n "open(\|OUT\|write\|json.dump" /Users/triton/PROTEUS/experiments/<folder>/<script>.py`

Most probe scripts write their result by **absolute path into their own artefact folder** (P-0183
`confirm.json`, P-0189 and P-0190 `result.txt`, P-0118 `result.json`). Copying the script to
`state/agents/inspector-YYYY-MM-DD/` and running the copy, the habit of 17 to 19 Oct, protects the
artefact only when the script writes relative to `__file__` or the working directory. On 20 and 21 Oct
the copies did nothing and the committed files were rewritten in place anyway.

So: expect the artefact to be rewritten, and plan the restore (below) before the run, not after.

## Run

Pick the interpreter from the imports, not from habit:

- `/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3` for numpy, pandas, scipy (P-0182, P-0189,
  P-0190). Plain `python3` here is Homebrew 3.14 on an Intel Mac and has no wheels for those.
- `/Users/triton/PROTEUS/.venv/bin/python3` for python-chess (P-0171) and the desk dependencies.
- `python3 -I /Users/triton/PROTEUS/experiments/<folder>/<script>.py` when the script reads a file
  that was downloaded (allowed unattended since 21 Oct, F-0007).

Absolute script path, timeout 600000, never `run_in_background`. A script that calls a live API can
fail on the API, not on the claim: Open-Meteo answered 503 on the first try on 19 Oct (P-0178) and ran
clean on the second. Run twice before writing "broken".

## Compare

Put the re-run's headline numbers beside the quoted ones. Three outcomes, each with its line:

- **Same numbers**: one run-log line, `P-00NN identical (the numbers)`. Timing fields that differ
  (`one_request_seconds`, `think_s`, a 3.0 s arm at 0.33 against 0.46 cp on 18 Oct) are not a
  difference; the headline is.
- **Data moved underneath** (live pools, forecasts, odds): the claim may still hold. If it does, say so
  with both numbers and no finding (P-0172, 18 Oct). If the quoted figure is now misleading, a `low`
  finding on desk `probes` (P-0179, F-0038, 19 Oct):
  `python3 /Users/triton/PROTEUS/bin/findings.py add --desk probes --severity low --title "..." --evidence "..."`
- **A quoted number is wrong** on the same data: `high` finding, same command, and a correction line in
  the run log naming both numbers. Never edit the probe's NOTE.md or the register to hide it.

## Restore, then prove the folder is clean

`git -C /Users/triton/PROTEUS status --short -- /Users/triton/PROTEUS/experiments/<folder>`

For each `M` file: `git -C /Users/triton/PROTEUS diff -- /Users/triton/PROTEUS/experiments/<folder>/<file>`.
The commit is the probe's proof of what it found when it found it, so the re-run does not replace it.
Restore the committed bytes:

1. `git -C /Users/triton/PROTEUS show HEAD:experiments/<folder>/<file>` and Write the output back to
   the file, byte for byte (trailing newline included; `show` prints it).
2. `git -C /Users/triton/PROTEUS status --short -- /Users/triton/PROTEUS/experiments/<folder>` must now
   print nothing.

`git checkout`, `git restore`, `git stash`, `rm` and `mv` are not on the unattended safe list (checkout
was denied on 20 Oct); `show`, `diff`, `status`, `log` and `cp` are. A re-run that leaves the artefact
dirty becomes somebody else's "left dirty" line for days: P-0118's `result.json` sat dirty from 12 to
20 Oct (F-0014).

## Children

One long re-check may go to a `general-purpose` child on `sonnet`. It can write only under
`/Users/triton/PROTEUS/state/agents/` and cannot run `git`, so tell it to copy the script there first
and to report the output path the script hardcodes; the parent compares and restores.
