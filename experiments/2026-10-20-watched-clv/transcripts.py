"""Pull transcripts for the given video ids into this folder as <id>.txt; print length per id.
Copied from experiments/2026-10-13-watched-weather-markets/transcripts.py."""
import os, sys
from youtube_transcript_api import YouTubeTranscriptApi

HERE = os.path.dirname(os.path.abspath(__file__))

for vid in sys.argv[1:]:
    try:
        try:
            segs = YouTubeTranscriptApi().fetch(vid, languages=["en", "en-GB", "en-US"])
            rows = [(s.start, s.text) for s in segs]
        except AttributeError:
            rows = [(s["start"], s["text"]) for s in YouTubeTranscriptApi.get_transcript(vid, languages=["en"])]
        lines = [f"[{int(t)//60:02d}:{int(t)%60:02d}] {x}" for t, x in rows]
        with open(os.path.join(HERE, vid + ".txt"), "w") as f:
            f.write("\n".join(lines))
        words = sum(len(x.split()) for _, x in rows)
        print(vid, "ok", len(rows), "segments", words, "words", f"{rows[-1][0]/60:.1f} min")
    except Exception as e:
        print(vid, "FAIL", type(e).__name__, str(e)[:160])
