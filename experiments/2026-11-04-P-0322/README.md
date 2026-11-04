# P-0322: mcp-video-analyzer with no third-party upload

**Question.** P-0312 saw mcp-video-analyzer 0.11.0 send audio to OpenAI when captions failed. Can it
transcribe a captionless local file with nothing leaving the Mac?

**What the code says** (`dist/processors/audio-transcriber.js`). Three strategies in order: transformers.js
only if `WHISPER_HF_MODEL` is set; then `WHISPER_BIN` or `whisper` on PATH, called with openai-whisper flags
(`<audio> --output_format json --model M --output_dir D`), reading `<D>/<base>.json` `segments`; then OpenAI
`whisper-1`, only if `OPENAI_API_KEY` is set. So there is no switch to find: an unset key is the switch. The gap
is that whisper.cpp's `whisper-cli` takes different flags and writes a different JSON.

**Method.** `whisper_shim.py` takes the openai-whisper flags, runs `/usr/local/bin/whisper-cli` with
`ggml-base.en.bin`, and rewrites its JSON into `segments`. `run.mjs` deletes `OPENAI_API_KEY` and
`WHISPER_HF_MODEL`, sets `WHISPER_BIN` to the shim, and wraps `fetch` to count every host contacted. `probe.py`
makes a 44-word clip with `say`, wraps it as a captionless mp4 with ffmpeg, runs the tool (`--detail brief
--fields transcript,metadata --force-refresh`) and scores word match with difflib.

**Numbers.** Exit 0 in 5.9 s, 3 transcript entries, word match **0.909** (40 of 44; shot 0.90). Misses: "14"
for "fourteen", "Matteo" for "Meteo", "Hakka" for "Hacker", one dropped "at". Fetches: **0**, to any host. The tool
itself flags it: "Transcript generated via Whisper fallback".

**Caveats.** A synthetic voice is easy audio; P-0068 found whisper-cli base.en dropped half the words on a real
66 s clip. The fetch counter sees `globalThis.fetch` only, which is what the OpenAI path uses; ffmpeg and
whisper-cli are local binaries. `--model` from the tool is ignored by the shim (whisper.cpp needs a ggml path;
`P0322_GGML` overrides).

**Two denials on the way.** `say` and a bare `/usr/local/bin/ffmpeg` are off the unattended safe list; both
ran from `probe.py` instead.
