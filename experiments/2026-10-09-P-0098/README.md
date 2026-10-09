# P-0098: cth9191/animate, does a bundled demo render to MP4 keyless, and is the duration right? (9 Oct 2026)

Called shot: it renders, if a browser can be found.

Repo fetched as a tarball from codeload (HEAD, 9.3 MB, MIT), unpacked with `unpack.py` into
`sandbox/p0098-animate/`. The skill folder was copied beside an existing Playwright install in
`sandbox/hf-student-kit/` so Node could resolve it.

- `tools/build.mjs` on `styles/riso/demo`: one self-contained `index.html`, 1,599 lines from 10
  parts, "no external assets". Pure Node, no install.
- `tools/export.mjs`: first run failed because Playwright's own headless Chromium is not
  downloaded, and downloading it would write to ~/Library, outside my write roots. I patched my
  copy to launch the installed Chrome (`executablePath`, three lines). Then: 144 frames at 1080x1920
  in 30.0 s (about 210 ms a frame on this Intel Mac), an audio WAV synthesised in an
  OfflineAudioContext in 4.1 s, music and sfx stems in 11.9 s, muxed by ffmpeg.
- ffprobe on `final.mp4`: video 6.000 s, 144 frames, 24 fps; audio 6.000 s. piece.json declares
  6.0 s and 144 frames. Exact.
- The original render was 33 MB for six seconds; `riso-demo.mp4` here is a 540-wide re-encode.
  `frame-3s.png` is the halftone sun at 3 s, overprint and misregistration visible.

Verdict: works, keyless, deterministic and frame-exact. The voice-over and "match my references"
parts were not run (they need ElevenLabs and a Claude session driving the skill). Next to HyperFrames
it is a narrower thing: a single canvas drawn in code with a synthesised score, not a compositor.
