# P-0192: fresh install today of the four W39 tools, same checks as P-0012

Run 22 Oct 2026, 12:55, Trials slot. Called shot before running: works at 0.65, expecting 4 of 4
to give the September answers with at least one version bump, hyperframes the likeliest to
differ. Measured: **3 of 4**. The verdict hit; the number missed, and the one that drifted was
the one I called safest.

## Question

P-0012 showed the pinned September copies still run. This is the other half: a reader who
follows the 26 Sep Field Notes today and installs fresh. Do today's registry versions give the
same answers?

## Method

`fresh.py` installs each tool into a new `sandbox/p0192/` directory (npm with `--ignore-scripts`
and the sandbox cache; GitHub tarballs for magpie HEAD and the student kit; the Go toolchain
from P-0022 is reused, it is not the tool under test) and re-runs the September checks against
the September experiment folders.

| Tool | Sept version | Today | Same answers | Clean |
|---|---|---|---|---|
| reladraw | 0.5.0 | 0.18.0 | no: CLI wants `reladraw render FILE`, syntax `level with` is now `even with`; migrated diagram renders deterministically (sha 1f373c2d4524e8be, 1632 bytes v 1842 in Sept) | **no** |
| golive | v0.1.0-alpha.4 | v0.1.0-alpha.9 | yes: version, detect, init, doctor, plan, bare apply rc 0,0,0,2,0,1, 6 of 6 as Sept; detect names next, supabase, stripe, resend; apply refuses without --plan | yes |
| magpie | HEAD 26 Sep | HEAD today (go 1.26.8) | yes: 9 of 9 cases byte-identical, go test ok 6.0 s | yes |
| hyperframes-student-kit | 0.7.109 | 0.7.109 (the kit pins it) | yes: lint 0 errors, draft render 19.5 s, 240 frames, h264 1920x1080 8.0 s 1.26 MB | yes |

Timings: student kit tarball 411 MB in 32 s, npm install 141 packages 5.3 s; magpie tarball
73 MB in 11 s. Whole run about 100 s of tool time.

## Reading

- Thirteen minor versions in 26 days took reladraw past the September notes twice over. Both
  breaks fail loudly with the exact fix in the error, so a reader is stuck for one minute, not
  an afternoon. The migrated diagram is still deterministic (two renders, one sha), which was the
  claim that mattered; the bytes differ from September (1632 v 1842) so the layout changed too,
  and I did not measure how.
- hyperframes did not move because the student kit pins 0.7.109 in its lockfile; the hyperframes
  package itself is past that (0.8 was in use elsewhere in this folder on 7 Oct). The kit, not
  the engine, is what the notes reviewed, so this is the right measurement for the notes.
- golive moved five alpha tags and kept every exit code and refusal. magpie HEAD kept all nine
  config-edit cases byte-identical.

## What I got wrong on the first pass

The first pass marked golive not clean because my step list skipped `init`, which September ran
between detect and plan (P-0012's re-run never noticed because the old scratch app already had
its golive.yaml). Added and re-run, 6 of 6. The script's second pass only re-runs the tools
named on the command line and keeps the rest of results.json.

## What I did not do

- No measurement of how reladraw's layout changed between 0.5.0 and 0.18.0 beyond the byte
  count. The gap-is-a-minimum claim from P-0020 was not re-tested on 0.18.0.
- hyperframes 0.8 was not installed; the kit's pin is the reader's experience.
- No network beyond npm, codeload.github.com and whatever hyperframes does with telemetry off.

## Files

- `fresh.py` the script; `python3 fresh.py` runs all four, `python3 fresh.py reladraw golive`
  re-runs a subset.
- `results.json` the numbers, both passes merged.
- `three-migrated.reladraw`, `reladraw-migrated-1.svg`, `reladraw-migrated-2.svg` the 0.18.0
  renders; `magpie-cases/` the nine case files after the run.
