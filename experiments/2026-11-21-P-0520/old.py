"""P-0520: do old (pre-2015) YouTube videos far above the 52k line lack a most-replayed graph?

yt-dlp (sandbox/skool-venv) flat searches on queries that lean to old uploads, keeps ids with flat
view count 150,000 to 1,000,000, reads each with -J --skip-download, keeps those uploaded before
2015 until TARGET are kept or the 7-minute budget ends. Keyless, nothing downloaded.

    python3 old.py
"""
import json, os, subprocess, sys, time
from pathlib import Path

ROOT = "/Users/triton/PROTEUS/"
YTDLP = ROOT + "sandbox/skool-venv/bin/yt-dlp"
ENV = dict(os.environ, PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin")
HERE = Path(__file__).resolve().parent
BASE = [YTDLP, "-q", "--no-warnings", "--js-runtimes", "node"]
QUERIES = ["how to tie a tie 2011", "guitar lesson 2012", "minecraft tutorial 2012",
           "iphone 4 review", "windows 7 tips", "harlem shake 2013", "how to solve rubiks cube 2010",
           "khan academy algebra", "ipad 2 unboxing", "photoshop cs5 tutorial"]
PER = 25
TARGET = 25
LO, HI = 150000, 1000000
STOP_AT = time.time() + 7 * 60


def run(args):
    return subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=120)


def main():
    if Path(ROOT + "HALT").exists():
        print("HALT")
        return 1
    cands, seen = [], set()
    for q in QUERIES:
        r = run(BASE + ["--flat-playlist", "--print", "%(id)s %(view_count)s", "ytsearch%d:%s" % (PER, q)])
        for line in r.stdout.splitlines():
            p = line.split()
            if len(p) == 2 and len(p[0]) == 11 and p[1].isdigit() and LO <= int(p[1]) <= HI and p[0] not in seen:
                seen.add(p[0])
                cands.append((q, p[0]))
        time.sleep(0.5)
    print("candidates", len(cands), flush=True)
    rows = []
    for q, vid in cands:
        kept = [r for r in rows if r.get("old")]
        if len(kept) >= TARGET or time.time() > STOP_AT:
            break
        j = run(BASE + ["-J", "--skip-download", "https://www.youtube.com/watch?v=" + vid])
        try:
            info = json.loads(j.stdout)
        except ValueError:
            rows.append({"q": q, "id": vid, "error": j.stderr.strip()[-100:]})
            continue
        up = info.get("upload_date") or ""
        row = {"q": q, "id": vid, "old": bool(up) and up < "20150101", "heatmap": bool(info.get("heatmap")),
               "views": info.get("view_count"), "upload": up, "duration": info.get("duration"),
               "comments": info.get("comment_count"), "category": (info.get("categories") or [None])[0]}
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(1.2)
    old = [r for r in rows if r.get("old")]
    newer = [r for r in rows if "heatmap" in r and not r["old"]]
    summary = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "candidates": len(cands),
               "read": len([r for r in rows if "heatmap" in r]), "errors": len([r for r in rows if "error" in r]),
               "old_kept": len(old), "old_without": len([r for r in old if not r["heatmap"]]),
               "old_without_rows": [r for r in old if not r["heatmap"]],
               "newer_read": len(newer), "newer_without": len([r for r in newer if not r["heatmap"]])}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
