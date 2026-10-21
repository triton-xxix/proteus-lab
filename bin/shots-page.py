#!/usr/bin/env python3
"""Build docs/probes/shots/data.json from the called-shot book in state/probes.json (Workshop, 21 Oct 2026).

A shot is scored on the verdict word only (probe.py cmd_shots): hit when the verdict equals the
expected one. The number written beside it is not scored, so this page says so. Same totals as
`probe.py shots`; exits non-zero if they ever disagree.
"""
import json
import os
import subprocess
import sys

ROOT = "/Users/triton/PROTEUS"
STATE = os.path.join(ROOT, "state", "probes.json")
OUT = os.path.join(ROOT, "docs", "probes", "shots", "data.json")
BINS = [(0.0, 0.55, "under 55%"), (0.55, 0.6, "55%"), (0.6, 0.7, "60 to 65%"), (0.7, 0.8, "70 to 75%"), (0.8, 1.01, "80% and up")]


def brier(ps, hits):
    return sum((p - h) ** 2 for p, h in zip(ps, hits)) / len(ps)


def main():
    st = json.load(open(STATE))
    rows = []
    for i in st["items"]:
        s = i.get("shot")
        if not s or i.get("status") != "done" or not i.get("verdict"):
            continue
        rows.append({
            "id": i["id"],
            "title": (i.get("title") or "")[:140],
            "expect": s["expect"],
            "verdict": i["verdict"],
            "p": s["p"],
            "hit": 1 if i["verdict"] == s["expect"] else 0,
            "number": s.get("number", ""),
            "at": s["at"],
        })
    rows.sort(key=lambda r: r["at"])
    waiting = sum(1 for i in st["items"] if i.get("shot") and i.get("status") != "done")
    n = len(rows)
    ps = [r["p"] for r in rows]
    hits = [r["hit"] for r in rows]
    hit_rate = sum(hits) / n
    works = [r for r in rows if r["expect"] == "works"]
    other = [r for r in rows if r["expect"] != "works"]
    verdict_works = sum(1 for r in rows if r["verdict"] == "works")
    bins = []
    for lo, hi, label in BINS:
        b = [r for r in rows if lo <= r["p"] < hi]
        if b:
            bins.append({"label": label, "n": len(b), "mean_p": round(sum(r["p"] for r in b) / len(b), 3),
                         "hit_rate": round(sum(r["hit"] for r in b) / len(b), 3)})
    summary = {
        "n": n, "waiting": waiting, "hits": sum(hits), "hit_rate": round(hit_rate, 3),
        "mean_p": round(sum(ps) / n, 3), "brier": round(brier(ps, hits), 3),
        "brier_at_hit_rate": round(brier([hit_rate] * n, hits), 3),
        "called_works": len(works), "called_works_hits": sum(r["hit"] for r in works),
        "called_other": len(other), "called_other_hits": sum(r["hit"] for r in other),
        "verdict_works": verdict_works,
        "first": rows[0]["at"][:10], "last": rows[-1]["at"][:10],
    }
    # agreement with probe.py's own tally
    out = subprocess.run([sys.executable, os.path.join(ROOT, "bin", "probe.py"), "shots"], capture_output=True, text=True).stdout
    want = "%d scored, %d waiting; hit rate %.2f; mean stated p %.2f; Brier %.3f" % (n, waiting, hit_rate, summary["mean_p"], summary["brier"])
    if want not in out:
        sys.exit("shots-page: disagrees with probe.py shots\n  mine: %s\n  probe.py: %s" % (want, out.strip()))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"summary": summary, "bins": bins, "rows": rows}, f, indent=1)
    print("shots-page: %d shots, hit rate %.2f against stated %.2f, Brier %.3f; agrees with probe.py; wrote %s"
          % (n, hit_rate, summary["mean_p"], summary["brier"], OUT))


if __name__ == "__main__":
    main()
