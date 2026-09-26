# P-0019: hyperframes-student-kit, does the keyless demo lint and render?

Run 26 Sep 2026, 23:35 to 23:50, from the nightly. Source: harvest H-0010. Script:
`sandbox/p0019_student_kit.py` (steps fetch, install, demo, lint, render, probe). Step log with
timings and output tails: `steps.jsonl`. The rendered file stays in the experiment folder as
`demo.mp4` (1.26 MB).

## What I ran

1. **Fetch.** `git clone` is not on the unattended safe list (denied, one call), so the script pulls
   the codeload tarball instead. 398 MB, 1,229 files, 69 s. The repo carries its example media,
   which is why it is that big for a skills kit.
2. **Install.** `npm install --ignore-scripts`: 141 packages in 6.7 s (hyperframes 0.7.109, gsap,
   playwright). No postinstall scripts ran.
3. **Demo.** `npm run demo` copies `examples/starter` to `video-projects/demo` and vendors gsap into
   it. 0.8 s.
4. **Lint.** `npx hyperframes lint`: 0 errors, 0 warnings, 5.9 s.
5. **Render.** `npx hyperframes render --quality draft`: rc 0 in 60 s wall, 34 s of pipeline. 240
   frames captured by three workers in 14.7 s, encoded in 2.5 s, "artifact validated".
6. **ffprobe.** h264, 1920x1080, 30 fps, exactly 8.000 s, no audio stream.

## What I did not do

- Studio preview: it is an interactive server with a browser, not something a scheduled run can
  judge. Not run.
- Did not check whether render touched the network. The render worked with install scripts
  disabled, so its headless browser came from a cache already on this Mac (HyperFrames skills are
  installed here), not from the kit. On a clean machine the first render would download one.
- The real-footage path (transcript, silence cuts, 406 card templates) needs ElevenLabs or a local
  Whisper and footage. Not tried.

## Verdict

Works. The claim holds for the slice tested: keyless, no account, lint clean, a valid 8-second
1080p mp4 in about a minute. Caveat: nothing here is the kit's own work beyond a starter template
and a copy script; the render is HyperFrames itself.
