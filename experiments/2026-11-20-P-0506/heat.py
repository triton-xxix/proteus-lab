"""P-0506: what decides whether a YouTube video has a most-replayed heatmap?

yt-dlp (sandbox/skool-venv) searches three unrelated queries, 10 results each, and reads each video's
JSON with --skip-download. Records heatmap present or not, view count, upload date, duration.
Keyless, nothing downloaded.

    python3 heat.py
"""
import json, os, subprocess, sys, time
from pathlib import Path

ROOT = "/Users/triton/PROTEUS/"
YTDLP = ROOT + "sandbox/skool-venv/bin/yt-dlp"
ENV = dict(os.environ, PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin")
HERE = Path(__file__).resolve().parent
BASE = [YTDLP, "-q", "--no-warnings", "--js-runtimes", "node"]
QUERIES = ["sourdough starter beginner", "bicycle chain repair", "banjo lesson clawhammer"]
PER = 10


def run(args):
    return subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=120)


def main():
    if Path(ROOT + "HALT").exists():
        print("HALT")
        return 1
    rows = []
    for q in QUERIES:
        r = run(BASE + ["--flat-playlist", "--print", "%(id)s", "ytsearch%d:%s" % (PER, q)])
        ids = [x for x in r.stdout.split() if len(x) == 11]
        for vid in ids:
            j = run(BASE + ["-J", "--skip-download", "https://www.youtube.com/watch?v=" + vid])
            try:
                info = json.loads(j.stdout)
            except ValueError:
                rows.append({"q": q, "id": vid, "error": j.stderr.strip()[-120:]})
                print(json.dumps(rows[-1]), flush=True)
                time.sleep(2)
                continue
            row = {"q": q, "id": vid, "heatmap": bool(info.get("heatmap")),
                   "views": info.get("view_count"), "upload": info.get("upload_date"),
                   "duration": info.get("duration"), "likes": info.get("like_count"),
                   "live": info.get("was_live")}
            rows.append(row)
            print(json.dumps(row), flush=True)
            time.sleep(1.5)
    ok = [r for r in rows if "heatmap" in r and r["views"] is not None]
    yes = [r for r in ok if r["heatmap"]]
    no = [r for r in ok if not r["heatmap"]]
    summary = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "videos": len(rows), "read": len(ok), "errors": len(rows) - len(ok),
        "with_heatmap": len(yes), "without": len(no),
        "lowest_views_with": min((r["views"] for r in yes), default=None),
        "highest_views_without": max((r["views"] for r in no), default=None),
        "views_with_sorted": sorted(r["views"] for r in yes),
        "views_without_sorted": sorted(r["views"] for r in no),
        "durations_without": sorted(r["duration"] or 0 for r in no),
        "uploads_without": sorted(r["upload"] or "" for r in no),
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
