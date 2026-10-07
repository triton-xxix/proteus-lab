# P-0092: does Mortiflix's free demo run to a playable video on macOS?

Run 8 Oct 2026 00:08 to 00:16 BST, keyless, no Claude session used. Repo GTKottman/mortiflix-oss
(AGPL-3.0, 371 stars, created 5 Oct 2026), fetched as a tarball with `sandbox/p0092/fetch.py`
(git clone is off the unattended list), installed with the one npm form the hook allows
(`npm ci --ignore-scripts`, 7 packages, the only dependency is the Anthropic SDK).

## Yes

- `mortiflix demo --studio <sandbox folder>` made the studio, found the Claude Code login on this
  Mac as a backend (it was not used: the demo backend is scripted), queued a "logo sting" project
  from the bundled SVG, ran one session and stopped at the first gate, as the README promises.
- The gates are real: the CLI's `review` is interactive, so I approved through the same
  `gates.respond` call it uses, from a 20-line driver (`sandbox/p0092/approve.mjs`). The
  logo-sting pipeline in the demo has two steps: Directions (three placeholder SVG style frames,
  one question answered with the default) and Final.
- Final v1 arrived as `preview.mp4`: 4.0 s, 1280x720, h264 at 24 fps with a mono AAC track,
  1.4 MB, made by ffmpeg (the demo backend's test pattern). Copied here as evidence. The project
  state went queued, waiting, queued, waiting, delivered across two `mortiflix run` calls.
- Nothing was written outside the sandbox: `--studio` (or `MORTIFLIX_STUDIO`) moves the whole
  studio, which defaults to `~/Mortiflix`.

## What it is, from the run

A harness, not a model: pipelines are folders of `pipeline.json`, a craft document and skills; a
session (Claude Code, the API, or this scripted demo) works until it has something to review,
submits it through an `mfx` bridge that refuses submissions missing their error checks, then stops.
The reviewed files are copied under `state/<project>/reviews/` out of the session's reach. The web
studio (`mortiflix serve`) and the real backends were not run tonight: a real video needs the
Claude Code login, which is Luke's plan, so that is a probe for an interactive session.

## Verdict

**works**: the free demo runs end to end on macOS with the gates walked by script, and leaves a
real mp4. The README's "macOS untested" warning did not bite.
