# Channel digest

A YouTube channel's recent uploads, keyless, with the sentences worth checking flagged and linked to
the second they were said.

```
pip install youtube-transcript-api
python3 digest.py @Unabated eFd_LWmH2bQ --days 7 --max 5
```

- A channel can be a handle (`@Unabated`), a channel id (`UC...`), a channel URL, or any video id
  or URL from that channel (the channel is read from the watch page).
- Uploads come from the channel's public RSS feed, which holds only the last 15. If every one of
  the 15 is inside the window the digest says so, because there may be more.
- Transcripts come from YouTube's captions through `youtube-transcript-api`.
- Output: `digest.json` and `digest.md` in `--out` (default: next to the script).

## What a flag means

A flag is not a check. Each sentence scores 3 for a percentage, up to 2 for other numbers, 1 for a
year, 2 for a comparison ("more than", "beats", "on average", "edge") and 1 for an absolute
("always", "never", "guaranteed"). Sentences scoring 3 or more are candidates; the top five per
video are kept. Captions rarely carry full stops, so a "sentence" is cut at punctuation or every
30 words. Caption noise (`[music]`, `>>`) is stripped.

## Known limits (29 Oct 2026, first run)

- YouTube's IP block: the second run of the day, about 25 caption fetches in ten minutes from one
  Mac, had 2 of 13 refused with `IpBlocked`. They are reported per video, never retried.
- The heuristic has not been scored. Next step: hand-mark a sample of flagged and unflagged lines
  and see whether the flags are the checkable ones.
- Shorts and clips are read like anything else and usually flag nothing.

Built by Proteus, Big Expedition step one (channel digest, 26 Oct to 8 Nov 2026).
