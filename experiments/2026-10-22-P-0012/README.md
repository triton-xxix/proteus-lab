# P-0012: which of the W39 AI builder tools still run cleanly a month later?

Run 22 Oct 2026, 12:35, Trials slot. Called shot before running: works at 0.70, expecting 3 of 4
clean with the hyperframes render as the drift. Measured: **4 of 4 clean**. The shot's verdict hit,
its number missed by one.

## Question

The 26 Sep Field Notes (2026-W39) reported four tools as "works": hyperframes-student-kit,
reladraw, magpie and golive-skill. A month later, do the copies a reader would have installed
then still do what the notes said, with the same answer?

## Method

`rerun.py` re-runs each tool from its sandbox copy (no reinstall) and compares with the 26 Sep
experiment folder for that probe. "Clean" means every step the September run passed still passes
with the same answer.

| Tool | Sept probe | What was re-run | Sept | Now | Clean |
|---|---|---|---|---|---|
| reladraw 0.5.0 | P-0020 | same 3-node diagram rendered twice | sha c3640837d2a41250 | same sha both times, well-formed | yes |
| magpie (Go, local toolchain) | P-0022 | the 9 SetJSON/DelJSON cases on fresh copies | 9 results | 9 of 9 byte-identical outputs and error strings | yes |
| golive v0.1.0-alpha.4 | P-0023 | version, detect, doctor, plan, bare apply, fake HOME | rc 0,0,2,0,1 | rc 0,0,2,0,1; detect names next/supabase/stripe/resend; apply refuses without --plan | yes |
| hyperframes 0.7.109 (student kit) | P-0019 | lint and draft render of the demo, ffprobe | lint 5.9 s, render 60.1 s | lint 2.0 s, render 19.5 s, 240 frames, h264 1920x1080 8.0 s 1.26 MB | yes |

Whole run: 30 s wall. The hyperframes render is three times faster than in September on the same
machine and the same installed version; the September run was the first after install (cold
Chromium and worker cache), so the speed difference is a warm cache, not a tool change.

## What I got wrong on the first pass

My first run marked golive not clean because the "detect names the stack" check searched only the
last 300 characters of its output. The tool was fine; the check was narrow. Fixed and re-run; both
results.json files are the second run.

## What I did not do

- No fresh install from today's registries. This tests the pinned copies a September reader would
  hold, not whether `npm install reladraw` or `golive@alpha` today still gives the same answers.
  Queued as a deepen.
- The hyperframes mp4 was rendered, probed and deleted (1.26 MB does not belong in git).
- No network was used except whatever hyperframes does on its own with telemetry off.

## Files

- `rerun.py` the script, re-runnable.
- `results.json` the numbers.
- `reladraw-three-1.svg`, `reladraw-three-2.svg`, `three.reladraw` the reladraw renders.
- `magpie-cases/` the nine case files after the run plus their error strings.
