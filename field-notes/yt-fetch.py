#!/usr/bin/env python3
"""
yt-batch fetch — pull metadata + transcript for a list of YouTube URLs.

No yt-dlp, no API keys, no OpenAI. Metadata comes from YouTube's keyless
oEmbed endpoint; transcripts from youtube-transcript-api (Hermes venv).

Usage:
    /Users/triton/.hermes/hermes-agent/venv/bin/python3 fetch.py urls.txt
    ... --only VIDEO_ID     fetch a single video
    ... --force             refetch even if staged output already exists

Writes, per video, into staging/:
    <id>.json   metadata + timestamped transcript segments
    <id>.txt    readable transcript, one line per ~30s block with [mm:ss]

Rerunnable: already-staged videos are skipped unless --force.
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STAGING = os.path.join(HERE, "staging")

ID_PATTERNS = [
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})",
    r"youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})",
]


def video_id(url):
    for pat in ID_PATTERNS:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    if re.fullmatch(r"[a-zA-Z0-9_-]{11}", url.strip()):
        return url.strip()
    return None


def read_urls(path):
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            vid = video_id(line)
            if vid:
                out.append((vid, line))
            else:
                print(f"  !! unparseable line: {line}")
    return out


def fetch_metadata(url):
    """Keyless title/channel via oEmbed. Returns {} on failure."""
    endpoint = "https://www.youtube.com/oembed?" + urllib.parse.urlencode(
        {"url": url, "format": "json"}
    )
    try:
        with urllib.request.urlopen(endpoint, timeout=20) as resp:
            data = json.load(resp)
        return {
            "title": data.get("title"),
            "channel": data.get("author_name"),
            "channel_url": data.get("author_url"),
            "thumbnail": data.get("thumbnail_url"),
        }
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


def fetch_transcript(vid):
    """Timestamped segments via youtube-transcript-api. Raises on failure."""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(vid, languages=["en", "en-GB", "en-US"])
    except Exception:
        # fall back to whatever language exists
        fetched = api.fetch(vid)
    return fetched.to_raw_data()


def blockify(segments, block_seconds=30):
    """Collapse segments into ~30s blocks so quotes stay locatable."""
    lines, buf, block_start = [], [], None
    for seg in segments:
        if block_start is None:
            block_start = seg["start"]
        buf.append(seg["text"].replace("\n", " ").strip())
        if seg["start"] - block_start >= block_seconds:
            mins, secs = divmod(int(block_start), 60)
            lines.append(f"[{mins:02d}:{secs:02d}] " + " ".join(buf))
            buf, block_start = [], None
    if buf:
        mins, secs = divmod(int(block_start or 0), 60)
        lines.append(f"[{mins:02d}:{secs:02d}] " + " ".join(buf))
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    only = None
    if "--only" in args:
        i = args.index("--only")
        only = args[i + 1]
        args = args[:i] + args[i + 2:]
    urls_path = args[0] if args else os.path.join(HERE, "urls.txt")

    os.makedirs(STAGING, exist_ok=True)
    targets = read_urls(urls_path)
    if only:
        targets = [t for t in targets if t[0] == only]

    print(f"yt-batch: {len(targets)} video(s) from {urls_path}\n")
    ok, skipped, failed = 0, 0, []

    for idx, (vid, url) in enumerate(targets, 1):
        out_json = os.path.join(STAGING, f"{vid}.json")
        if os.path.exists(out_json) and not force:
            print(f"[{idx}/{len(targets)}] {vid}  — already staged, skipping")
            skipped += 1
            continue

        print(f"[{idx}/{len(targets)}] {vid}", end="  ", flush=True)
        meta = fetch_metadata(url)
        title = meta.get("title") or "(title unavailable)"

        try:
            segments = fetch_transcript(vid)
        except Exception as exc:
            reason = f"{type(exc).__name__}"
            print(f"NO TRANSCRIPT ({reason}) — {title}")
            failed.append({"videoId": vid, "url": url, "title": title, "reason": reason})
            continue

        record = {
            "videoId": vid,
            "url": url,
            "fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            **meta,
            "segmentCount": len(segments),
            "durationSeconds": int(segments[-1]["start"] + segments[-1].get("duration", 0)),
            "transcript": segments,
        }
        with open(out_json, "w") as fh:
            json.dump(record, fh, indent=2)
        with open(os.path.join(STAGING, f"{vid}.txt"), "w") as fh:
            fh.write(f"# {title}\n# {meta.get('channel')}\n# {url}\n\n")
            fh.write(blockify(segments))

        mins = record["durationSeconds"] // 60
        print(f"ok — {len(segments)} segs / ~{mins}m — {title}")
        ok += 1

    print(f"\nstaged {ok}, skipped {skipped}, failed {len(failed)}")
    if failed:
        report = os.path.join(STAGING, "_failed.json")
        with open(report, "w") as fh:
            json.dump(failed, fh, indent=2)
        print(f"failures written to {report}:")
        for f in failed:
            print(f"  - {f['videoId']}  {f['reason']}  {f['title']}")


if __name__ == "__main__":
    main()
