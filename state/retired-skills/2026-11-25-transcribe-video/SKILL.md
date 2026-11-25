---
name: transcribe-video
description: Get a usable transcript for a YouTube, Loom, Skool (Mux) or local video, keyless, with a completeness check so a half-empty whisper output is never treated as the talk. Use whenever a probe, the harvester, the research desk or a Skool reading needs what a video says.
---

# Transcribe a video

Routes proven by 9 Oct 2026, cheapest first. Nothing here needs a key or a login except the Skool
lesson page itself (an interactive browser session).

## Routes

1. **YouTube captions:** `youtube_transcript_api` in the project venv
   (`/Users/triton/PROTEUS/.venv/bin/python3`). Fast and exact when it works. YouTube blocks this IP
   after a burst (IpBlocked, then 429 on yt-dlp subtitles; 29 Sep and 7 Oct). On a block: stop asking,
   note it in the run log, try again next day. Never hammer it.
2. **Any host by script:** `sandbox/skool_transcript.py <url> [--out file] [--force-whisper]`
   (YouTube captions, then yt-dlp bestaudio to whisper-cli; Loom through its transcript endpoint).
3. **Skool lessons (Mux):** the lesson page carries a signed Mux playlist with an English caption
   track; fetch the caption track, not the audio (7 Oct: 2 h 59 min of video in minutes, no whisper).
4. **Local audio:** ffmpeg to 16 kHz mono wav, then `/usr/local/bin/whisper-cli` with ggml-base.en
   (about a third of real time on this Intel Mac). faster-whisper 1.2.1 needs PyAV 16 or older; pin it
   in `sandbox/py312-venv` (P-0068).

## Completeness check (always, for any whisper output)

P-0068 found whisper-cli dropped half the words on a 66 s clip (word error 0.537) while faster-whisper
got 0.109. So before using a whisper transcript:

- words per minute of audio should be roughly 120 to 180 for speech; under 80 means words were lost;
- the last timestamp should reach within a minute of the media duration (`ffprobe`);
- if either fails, re-run with faster-whisper or say in the artefact that the transcript is partial.

## Keep it legal and small

Raw course text and transcripts stay local (`field-notes/skool/`, `sandbox/`, both gitignored; the repo
is public). Commit what you learned, with the source and timestamp, not the transcript.
