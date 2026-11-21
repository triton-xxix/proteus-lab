# P-0521: mcp-server-youtube-transcript, keyless, against our pipeline

Question: does the MCP server return a full transcript keyless, within 10% of our pipeline's word count?

## What I ran

- `npm --prefix sandbox/p0521 install @kimtaeyoon83/mcp-server-youtube-transcript --ignore-scripts`:
  the registry's latest is **0.1.1, published Nov 2024**. The GitHub README describes `strip_ads`,
  chapter markers and more; none of that is in the published package, whose only tool is
  `get_transcript(url, lang)` built on `youtube-captions-scraper`. The README's `npx -y` install gets
  this 0.1.1.
- `run.py` drives the server over stdio (initialize, tools/list, tools/call) and compares word
  counts with `youtube_transcript_api`, our pipeline, on five videos. Output `results.json`.

## Result

| Video | MCP server | Ours |
|---|---|---|
| co33P6bb0eg | success, 0 words | 52 words |
| mdzIXanauYk | success, 0 words | 64 words |
| odRxggAh3G8 | error, no captions | error, TranscriptsDisabled |
| dQw4w9WgXcQ | success, 0 words | 487 words |
| jNQXAC9IVRw | success, 0 words | 39 words |

0 of 4 within 10%. Worse than an error: on every video with captions it reports success and hands
back an empty transcript, in under a second. An agent using it would conclude the video is silent.
The one honest answer was the video with captions turned off, where both agree.

Likely cause, not checked line by line: the scraper reads the old caption track format that YouTube
no longer serves to unauthenticated page fetches, and treats an empty parse as a transcript.

## Verdict

Broken, silently. Our own `youtube_transcript_api` pipeline (and the transcribe-video skill's
completeness check) stays; this is a good case for why that check exists.
