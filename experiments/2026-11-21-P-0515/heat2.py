"""P-0515: where does YouTube's most-replayed line fall inside P-0506's 38,676 to 58,618 bracket,
and do old videos need more views than new ones?

yt-dlp (sandbox/skool-venv) flat searches many queries (30 results each), keeps ids whose flat
view_count is 30,000 to 80,000 and not already read in P-0506, then reads each with -J
--skip-download until TARGET are read. Keyless, nothing downloaded.

    python3 heat2.py
"""
import json, os, subprocess, sys, time
from pathlib import Path

ROOT = "/Users/triton/PROTEUS/"
YTDLP = ROOT + "sandbox/skool-venv/bin/yt-dlp"
ENV = dict(os.environ, PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin")
HERE = Path(__file__).resolve().parent
PREV = Path(ROOT + "experiments/2026-11-20-P-0506/results.json")
BASE = [YTDLP, "-q", "--no-warnings", "--js-runtimes", "node"]
QUERIES = ["how to sharpen a chisel", "pottery wheel centering", "fly tying tutorial",
           "harmonica blues lesson", "bonsai repotting", "knitting cable stitch",
           "ukulele strumming pattern", "watercolor sky tutorial", "leather wallet making",
           "spoon carving"]
PER = 30
TARGET = 25
LO, HI = 30000, 80000


def run(args):
    return subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=120)


def main():
    if Path(ROOT + "HALT").exists():
        print("HALT")
        return 1
    seen = set()
    if PREV.exists():
        seen = {r["id"] for r in json.loads(PREV.read_text())["rows"]}
    cands = []
    for q in QUERIES:
        r = run(BASE + ["--flat-playlist", "--print", "%(id)s %(view_count)s", "ytsearch%d:%s" % (PER, q)])
        for line in r.stdout.splitlines():
            parts = line.split()
            if len(parts) != 2 or len(parts[0]) != 11 or not parts[1].isdigit():
                continue
            v = int(parts[1])
            if LO <= v <= HI and parts[0] not in seen:
                seen.add(parts[0])
                cands.append((q, parts[0], v))
        print("search", q, "candidates so far", len(cands), flush=True)
        time.sleep(1)
    rows = []
    for q, vid, flat_v in cands:
        if sum(1 for r in rows if "heatmap" in r) >= TARGET:
            break
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
               "duration": info.get("duration"), "live": info.get("was_live")}
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(1.5)
    ok = [r for r in rows if "heatmap" in r and r["views"] is not None]
    old = [r for r in ok if (r["upload"] or "9") < "20211121"]
    new = [r for r in ok if r not in old]

    def side(rs):
        yes = sorted(r["views"] for r in rs if r["heatmap"])
        no = sorted(r["views"] for r in rs if not r["heatmap"])
        return {"n": len(rs), "with": len(yes), "without": len(no),
                "lowest_with": yes[0] if yes else None, "highest_without": no[-1] if no else None,
                "views_with": yes, "views_without": no}

    summary = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "candidates": len(cands), "read": len(ok), "errors": len(rows) - len(ok),
               "all": side(ok), "over_5y": side(old), "under_5y": side(new)}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
