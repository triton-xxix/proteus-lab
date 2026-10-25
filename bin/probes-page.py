#!/usr/bin/env python3
"""Build docs/probes/data.json, the every-probe index, from state/probes.json (Workshop, 25 Oct 2026).

One row per finished probe (status done with a verdict), plus tallies by verdict, by source and by
ISO week. Exits non-zero if its verdict count differs from `probe.py status`, so the page can never
show a number the queue does not hold.
"""
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = "/Users/triton/PROTEUS"
STATE = os.path.join(ROOT, "state", "probes.json")
OUT = os.path.join(ROOT, "docs", "probes", "data.json")
VERDICTS = ["works", "not-worth-it", "blocked", "broken"]


def clip(s, n):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def main():
    st = json.load(open(STATE))
    rows = []
    for i in st["items"]:
        if i.get("status") != "done" or not i.get("verdict"):
            continue
        shot = i.get("shot") or {}
        page = os.path.isfile(os.path.join(ROOT, "docs", "probes", i["id"], "index.html"))
        rows.append({
            "id": i["id"],
            "title": clip(i.get("title"), 170),
            "source": i.get("source") or "unknown",
            "verdict": i["verdict"],
            "at": i.get("verdict_at") or "",
            "minutes": i.get("minutes"),
            "calls": i.get("calls"),
            "note": clip(i.get("note"), 320),
            "artefact": (i.get("artefacts") or [""])[0],
            "page": page,
            "shot": ({"expect": shot["expect"], "p": shot["p"], "hit": 1 if shot["expect"] == i["verdict"] else 0}
                     if shot.get("expect") else None),
        })
    rows.sort(key=lambda r: r["at"])
    n = len(rows)
    by_verdict = {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICTS}
    other = n - sum(by_verdict.values())
    if other:
        sys.exit("probes-page: %d verdicts outside %s" % (other, VERDICTS))
    sources = sorted({r["source"] for r in rows}, key=lambda s: -sum(1 for r in rows if r["source"] == s))
    by_source = [{"source": s, "n": sum(1 for r in rows if r["source"] == s),
                  **{v: sum(1 for r in rows if r["source"] == s and r["verdict"] == v) for v in VERDICTS}}
                 for s in sources]
    weeks = {}
    for r in rows:
        d = datetime.date.fromisoformat(r["at"][:10])
        monday = (d - datetime.timedelta(days=d.weekday())).isoformat()
        w = weeks.setdefault(monday, {"week": monday, **{v: 0 for v in VERDICTS}})
        w[r["verdict"]] += 1
    mins = sorted(r["minutes"] for r in rows if isinstance(r["minutes"], (int, float)))
    calls = [r["calls"] for r in rows if isinstance(r["calls"], (int, float))]
    summary = {
        "n": n, "by_verdict": by_verdict,
        "open": sum(1 for i in st["items"] if i.get("status") in ("open", "in_progress")),
        "killed": sum(1 for i in st["items"] if i.get("status") == "killed"),
        "minutes_total": int(sum(mins)), "minutes_median": mins[len(mins) // 2] if mins else None,
        "calls_total": int(sum(calls)), "pages": sum(1 for r in rows if r["page"]),
        "first": rows[0]["at"][:10], "last": rows[-1]["at"][:10],
    }
    out = subprocess.run([sys.executable, os.path.join(ROOT, "bin", "probe.py"), "status"], capture_output=True, text=True).stdout
    m = re.search(r"^verdicts: (\d+)$", out, re.M)
    if not m or int(m.group(1)) != n:
        sys.exit("probes-page: disagrees with probe.py status (mine %d, probe.py %s)" % (n, m.group(1) if m else "none"))
    with open(OUT, "w") as f:
        json.dump({"summary": summary, "by_source": by_source, "weeks": sorted(weeks.values(), key=lambda w: w["week"]),
                   "rows": rows}, f, indent=1, ensure_ascii=False)
    print("probes-page: %d verdicts (%s), %d sources, %d weeks; agrees with probe.py status; wrote %s"
          % (n, ", ".join("%s %d" % (v, by_verdict[v]) for v in VERDICTS), len(sources), len(weeks), OUT))


if __name__ == "__main__":
    main()
