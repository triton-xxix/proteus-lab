#!/usr/bin/env python3
"""P-0494: do loudness peaks land within 15 s of YouTube's most-replayed peaks?

Keyless. yt-dlp (sandbox/skool-venv) finds videos by search, reads each one's heatmap (the
most-replayed graph, 100 segments) and downloads the audio; ffmpeg decodes to 8 kHz mono PCM;
loudness is RMS per second, smoothed over 5 s. Top 5 peaks on each side, at least 30 s apart.
Usage: moments.py "search words" [n_videos]
"""
import json, math, os, struct, subprocess, sys, tempfile

ROOT = "/Users/triton/PROTEUS/"
YTDLP = ROOT + "sandbox/skool-venv/bin/yt-dlp"
ENV = dict(os.environ, PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin")
OUT = os.path.dirname(os.path.abspath(__file__))
BASE = [YTDLP, "-q", "--no-warnings", "--js-runtimes", "node"]
TOL, GAP, K = 15, 30, 5


def run(args):
    return subprocess.run(args, capture_output=True, text=True, env=ENV)


def peaks(series, k, gap, lo, hi):
    """series: list of (t, v). Greedy top-k by value, at least gap seconds apart, t in [lo, hi]."""
    out = []
    for t, v in sorted(series, key=lambda x: -x[1]):
        if t < lo or t > hi:
            continue
        if all(abs(t - p[0]) >= gap for p in out):
            out.append((t, v))
        if len(out) == k:
            break
    return sorted(out)


def loudness(path):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                       capture_output=True, env=ENV)
    raw = p.stdout
    n = len(raw) // 2
    per = []
    for s in range(0, n - 8000, 8000):
        chunk = struct.unpack("<8000h", raw[s * 2:(s + 8000) * 2])
        per.append(math.sqrt(sum(x * x for x in chunk[::8]) / 1000.0) + 1.0)
    db = [20 * math.log10(x) for x in per]
    sm = []
    for i in range(len(db)):
        w = db[max(0, i - 2):i + 3]
        sm.append((i + 0.5, sum(w) / len(w)))
    return sm


def main():
    query = sys.argv[1]
    want = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    r = run(BASE + ["--flat-playlist", "--print", "%(id)s", "ytsearch12:" + query])
    ids = [x for x in r.stdout.split() if len(x) == 11]
    results, tried = [], []
    for vid in ids:
        if len(results) >= want:
            break
        url = "https://www.youtube.com/watch?v=" + vid
        j = run(BASE + ["-J", "--skip-download", url])
        try:
            info = json.loads(j.stdout)
        except ValueError:
            tried.append({"id": vid, "skip": "no json: " + j.stderr.strip()[-120:]})
            continue
        dur, heat = info.get("duration") or 0, info.get("heatmap") or []
        if not heat or not (240 <= dur <= 1200):
            tried.append({"id": vid, "skip": "no heatmap" if not heat else "duration %d" % dur})
            continue
        tmp = tempfile.mkdtemp(prefix="p0494_", dir=ROOT + "sandbox")
        d = run(BASE + ["--retries", "5", "-f", "bestaudio", "-o", os.path.join(tmp, "a.%(ext)s"), url])
        files = os.listdir(tmp)
        if d.returncode != 0 or not files:
            tried.append({"id": vid, "skip": "audio failed: " + d.stderr.strip()[-120:]})
            continue
        loud = loudness(os.path.join(tmp, files[0]))
        for f in files:
            os.remove(os.path.join(tmp, f))
        os.rmdir(tmp)
        hs = [((h["start_time"] + h["end_time"]) / 2, h["value"]) for h in heat]
        lo, hi = 0.05 * dur, dur - 10
        hp = peaks(hs, K, GAP, lo, hi)
        lp = peaks(loud, K, GAP, lo, hi)
        hits = [t for t, _ in lp if any(abs(t - h) <= TOL for h, _ in hp)]
        covered = sum(1 for s in range(int(lo), int(hi)) if any(abs(s + 0.5 - h) <= TOL for h, _ in hp))
        chance = K * covered / max(1, int(hi) - int(lo))
        rev = [h for h, _ in hp if any(abs(t - h) <= TOL for t, _ in lp)]
        results.append({"id": vid, "title": info.get("title"), "duration": dur, "views": info.get("view_count"),
                        "heat_segments": len(heat), "heat_peaks_s": [round(t) for t, _ in hp],
                        "loud_peaks_s": [round(t) for t, _ in lp], "hits": len(hits), "of": len(lp),
                        "heat_peaks_with_a_loud_peak": len(rev), "chance_hits": round(chance, 2)})
        print(vid, dur, "s", "hits %d of %d" % (len(hits), len(lp)), "chance %.2f" % chance,
              "heat", [round(t) for t, _ in hp], "loud", [round(t) for t, _ in lp])
    out = {"query": query, "tolerance_s": TOL, "min_gap_s": GAP, "results": results, "skipped": tried}
    name = "results-" + "-".join(query.split()[:3]) + ".json"
    json.dump(out, open(os.path.join(OUT, name), "w"), indent=1)
    th, to, tc = sum(x["hits"] for x in results), sum(x["of"] for x in results), sum(x["chance_hits"] for x in results)
    print("TOTAL hits %d of %d, chance %.2f, videos %d, skipped %d" % (th, to, tc, len(results), len(tried)))


main()
