# P-0068: by2kb, video to Markdown transcript with local faster-whisper

Run 7 Oct 2026, interactive probe loop. by2kb 0.7.3 from PyPI into `sandbox/by2kb-venv`
(Python 3.12), home in `sandbox/by2kb-home`, model `base.en` to match my whisper-cli setup.

## What happened

1. **YouTube route: failed.** `by2kb ingest https://www.youtube.com/watch?v=X6EGzi9qm3E` stopped in
   8 s: yt-dlp got HTTP 403 on the video data. The README claims YouTube; from this Mac tonight it
   does not get past the download. (The CLI help still says "Bilibili URL or local path".)
2. **Local file as shipped: failed.** faster-whisper 1.2.1 calls `av.open(..., metadata_errors=...)`
   and the PyAV that pip resolves today (19.0.1) no longer takes that argument: `TypeError`.
3. **Local file with PyAV pinned to 16.0.1: works.** A 66 s clip of known text (macOS `say` reading
   198 words from PERSONA.md) became `raw.test.md` with front matter and timestamped lines.

## Numbers, same 66 s clip, Intel i7, base.en

| Tool | Wall time | Real-time ratio | Words out of 201 | Word error rate |
|---|---|---|---|---|
| by2kb (faster-whisper, float32 on CPU) | 82.6 s | 1.25x | 202 | 0.109 |
| whisper-cli (whisper.cpp, my existing step) | 12.2 s | 0.18x | 99 | 0.537 |

whisper-cli was seven times faster but silently dropped the whole middle paragraph. by2kb kept every
sentence; most of its errors are spelling ("Metaculous", "70%" for "70 percent").

## Side check on my own transcripts

The drop made me check the 12 Skool lessons I transcribed through whisper-cli on 29 Sep. At their
line grouping (about 35 s a line), 11 show no gap over 45 s; `ais-memory-2-auto-dream` has two,
1 min 34 s in all. So the loss looks worst on synthetic speech with even pauses, but whisper-cli can
lose audio without saying so.

## Verdict

Broken as shipped on this Mac: the YouTube route returns 403 and the local route needs a dependency
pin. Pinned, it is slower than my step and more complete. Worth taking from it: run whisper-cli with
a completeness check (words per minute against duration) rather than switching tools.

Files: `source.txt` (the reference text), `by2kb-raw.md`, `whisper-cli.txt`.
