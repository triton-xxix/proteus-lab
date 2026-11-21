"""P-0527: do YouTube Shorts carry a most-replayed heatmap? Flat-search Shorts queries with yt-dlp
(sandbox/skool-venv, keyless), then read candidates with -J --skip-download until 25 Shorts
(duration 180 s or less, or a /shorts/ URL) above 100,000 views are read. Nothing downloaded.
"""
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = "/Users/triton/PROTEUS/"
YTDLP = ROOT + "sandbox/skool-venv/bin/yt-dlp"
ENV = dict(os.environ, PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin")
HERE = Path(__file__).resolve().parent
BASE = [YTDLP, "-q", "--no-warnings", "--js-runtimes", "node"]
QUERIES = ["cooking hack #shorts", "satisfying #shorts", "football skills #shorts", "cat #shorts",
           "magic trick #shorts", "woodworking #shorts", "science experiment #shorts", "dance #shorts",
           "funny dog #shorts", "car #shorts", "basketball #shorts", "makeup #shorts"]
TARGET, MIN_VIEWS, MAX_READS = 25, 100000, 45


def run(args):
    return subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=120)


cands, seen = [], set()
for q in QUERIES:
    p = run(BASE + ["--flat-playlist", "-J", "ytsearch40:" + q])
    try:
        entries = json.loads(p.stdout).get("entries") or []
    except ValueError:
        entries = []
    for e in entries:
        vid = e.get("id")
        if not vid or vid in seen:
            continue
        seen.add(vid)
        vc, dur = e.get("view_count"), e.get("duration")
        if vc is not None and vc < MIN_VIEWS:
            continue
        if dur is not None and dur > 180:
            continue
        cands.append({"id": vid, "flat_views": vc, "flat_dur": dur, "query": q})
print("candidates", len(cands), "from", len(seen), "search results")

rows, reads = [], 0
for c in cands:
    if len([r for r in rows if r["short"] and r["views"] >= MIN_VIEWS]) >= TARGET or reads >= MAX_READS:
        break
    reads += 1
    p = run(BASE + ["-J", "--skip-download", "https://www.youtube.com/shorts/" + c["id"]])
    try:
        j = json.loads(p.stdout)
        if not isinstance(j, dict):
            raise ValueError("yt-dlp printed " + p.stdout.strip()[:20])
    except ValueError:
        rows.append({"id": c["id"], "error": (p.stderr or "")[-160:], "short": False, "views": 0})
        continue
    hm = j.get("heatmap")
    rows.append({"id": c["id"], "views": j.get("view_count") or 0, "duration": j.get("duration"),
                 "upload_date": j.get("upload_date"), "short": (j.get("duration") or 999) <= 180,
                 "heatmap": bool(hm), "heatmap_points": len(hm or []), "query": c["query"]})
    time.sleep(1)

read = [r for r in rows if r.get("short") and r["views"] >= MIN_VIEWS]
withhm = [r for r in read if r.get("heatmap")]
summary = {"read": len(read), "with_heatmap": len(withhm), "reads_attempted": reads,
           "errors": sum(1 for r in rows if "error" in r),
           "views_range": [min((r["views"] for r in read), default=None), max((r["views"] for r in read), default=None)]}
json.dump({"summary": summary, "rows": rows}, open(HERE / "results.json", "w"), indent=1)
print(json.dumps(summary))
