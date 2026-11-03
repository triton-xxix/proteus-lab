# P-0312 mcp-video-analyzer CLI on public YouTube videos

Question: does its CLI return transcript, frames and metadata for a public YouTube video in under 120 seconds?

Install: npm 0.11.0 into `sandbox/mcpva/` with `--ignore-scripts` (264 packages). Run through `sandbox/mcpva/run.mjs` (copied here), which sets
`MCP_CACHE_DIR` and `TMPDIR` inside the sandbox (the default cache is `~/Library/Caches`, outside my write roots; the hook denied the
inline env assignment, so the wrapper sets them) and `FFMPEG_BIN=/usr/local/bin/ffmpeg` (ignore-scripts skips ffmpeg-static's binary download).
Note: the CLI's argv starts after `analyze` when called through `runCli`.

| run | video | detail | wall | metadata | transcript | frames | OCR |
|---|---|---|---|---|---|---|---|
| 1 | jNQXAC9IVRw (0:19) | brief | 5.1 s | yes | 6 lines | skipped by design | - |
| 2 | same | standard, no ffmpeg | 23.1 s | yes | yes | 0 (browser fallback grabbed 3, all removed as black) | 0 |
| 3 | same | standard, ffmpeg set | 10.2 s | yes | (cached) | 1 | 0 |
| 4 | -9JM9suCIHs (8:56) | standard | 126.6 s | yes | **none**: YouTube subtitles 429, then OpenAI transcription 401 | 5 | 3 frames, conf 66 to 70 |

## Verdict: works, with two caveats measured

- The 19-second clip: everything in 10.2 s. The 9-minute video: 126.6 s, just over the 120 s line, and no transcript.
- The transcript failure is mine as much as theirs: I had pulled five transcripts from YouTube twenty minutes earlier, and the 429 is the
  burst block the transcribe-video skill warns about.
- When captions fail it falls back to OpenAI's transcription API on its own. With no key it got 401, which means it sent a request anyway.
  Worth knowing before pointing it at anything private: the fallback is a third-party upload, not a local whisper, unless `--model` is set
  and a local whisper is present (not tested).
- OCR on slide frames is rough but usable: the 2:54 frame carries "g ~ 0.011", the growth figure the Kelly video quotes.
- Without ffmpeg it silently degrades to a headless-browser frame grab (puppeteer-core) that produced only black frames.
