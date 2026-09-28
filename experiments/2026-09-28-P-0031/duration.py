"""P-0031 helper: duration and character count of each video's English transcript, straight from
youtube-transcript-api (the library the MCP server wraps), so the server's output can be checked
for truncation. Usage: duration.py ID [ID...]  (copy of sandbox/ytmcp/duration.py)"""
import sys
import time

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/ytmcp/lib")
from youtube_transcript_api import YouTubeTranscriptApi  # noqa: E402

api = YouTubeTranscriptApi()
for vid in sys.argv[1:]:
    t = time.time()
    try:
        tr = api.fetch(vid, languages=["en"])
        items = list(tr)
        last = items[-1]
        chars = sum(len(i.text) + 1 for i in items)
        print(vid, "ok", round(time.time() - t, 2), "s", len(items), "cues", chars, "chars", "ends", round((last.start + last.duration) / 60, 1), "min", "generated" if tr.is_generated else "manual")
    except Exception as e:
        print(vid, "fail", round(time.time() - t, 2), "s", type(e).__name__, str(e)[:120].replace("\n", " "))
