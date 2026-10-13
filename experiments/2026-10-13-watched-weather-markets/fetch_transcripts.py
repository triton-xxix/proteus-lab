#!/usr/bin/env python3
"""Fetch YouTube caption transcripts for a list of video ids, politely, one at a time.

Usage: fetch_transcripts.py OUTDIR id1 id2 ...
Writes OUTDIR/<id>.txt (plain text, one line per caption segment with a start time)
and prints one status line per id. Pauses 8 s between videos so the IP is not blocked.
"""
import sys
import time
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi


def main():
    outdir = Path(sys.argv[1])
    outdir.mkdir(parents=True, exist_ok=True)
    ids = sys.argv[2:]
    api = YouTubeTranscriptApi()
    for i, vid in enumerate(ids):
        if i:
            time.sleep(8)
        try:
            t = api.fetch(vid, languages=["en", "en-GB", "en-US"])
            lines = [f"[{s.start:7.1f}] {s.text}" for s in t]
            words = sum(len(s.text.split()) for s in t)
            last = t[-1].start + (t[-1].duration or 0) if len(t) else 0
            (outdir / f"{vid}.txt").write_text("\n".join(lines) + "\n")
            print(f"{vid}\tok\tsegments {len(t)}\twords {words}\tlast {last:.0f}s")
        except Exception as e:  # noqa: BLE001
            print(f"{vid}\tFAIL\t{type(e).__name__}: {str(e)[:120]}")


if __name__ == "__main__":
    main()
