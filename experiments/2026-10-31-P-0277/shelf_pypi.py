"""P-0277: tool-shelf freshness on PyPI. For every name in field-notes/toolshelf.jsonl, ask
pypi.org/pypi/<name>/json (keyless). Records: exists, latest version, latest upload date, whether a
release landed in the 30 days to tonight, and the gap from the shelf date. Run with python3 -I.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

SHELF = "/Users/triton/PROTEUS/field-notes/toolshelf.jsonl"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-31-P-0277/results.json"
UA = {"User-Agent": "proteus-probe (shelf freshness)", "Accept": "application/json"}
NOW = datetime(2026, 10, 31, 23, 59, tzinfo=timezone.utc)

rows = [json.loads(l) for l in open(SHELF, encoding="utf-8") if l.strip()]
names = {}
for r in rows:
    n = r["name"].strip()
    # PyPI normalises names: lower case, runs of -_. become -
    key = re.sub(r"[-_.]+", "-", n).lower()
    names.setdefault(key, []).append(r)
print("shelf rows", len(rows), "distinct normalised names", len(names), flush=True)

out = {}
for key, rs in names.items():
    rec = {"shelf_ids": [r["id"] for r in rs], "shelved": min(r["date"] for r in rs), "raw": rs[0]["name"]}
    try:
        req = urllib.request.Request(f"https://pypi.org/pypi/{key}/json", headers=UA)
        with urllib.request.urlopen(req, timeout=20) as resp:
            d = json.loads(resp.read().decode("utf-8"))
        latest = None
        for ver, files in d.get("releases", {}).items():
            for f in files:
                t = f.get("upload_time_iso_8601") or f.get("upload_time")
                if t and (latest is None or t > latest[0]):
                    latest = (t, ver)
        rec.update({"exists": True, "version": d["info"].get("version"), "latest_upload": latest[0] if latest else None,
                    "latest_version_uploaded": latest[1] if latest else None,
                    "summary": (d["info"].get("summary") or "")[:80], "n_releases": len(d.get("releases", {}))})
        if latest:
            dt = datetime.fromisoformat(latest[0].replace("Z", "+00:00"))
            rec["days_since_release"] = (NOW - dt).days
            rec["released_last_30d"] = (NOW - dt) <= timedelta(days=30)
            rec["released_after_shelved"] = latest[0][:10] >= rec["shelved"]
    except urllib.error.HTTPError as e:
        rec.update({"exists": False, "status": e.code})
    except Exception as e:  # noqa: BLE001
        rec.update({"exists": None, "error": type(e).__name__})
    out[key] = rec
    time.sleep(0.25)

ex = [v for v in out.values() if v.get("exists")]
res = {"shelf_rows": len(rows), "distinct_names": len(names), "on_pypi": len(ex),
       "not_on_pypi": sum(1 for v in out.values() if v.get("exists") is False),
       "errors": sum(1 for v in out.values() if v.get("exists") is None),
       "released_last_30d": sum(1 for v in ex if v.get("released_last_30d")),
       "released_after_shelved": sum(1 for v in ex if v.get("released_after_shelved")),
       "days_since_release_median": sorted(v["days_since_release"] for v in ex if "days_since_release" in v)[len(ex) // 2] if ex else None,
       "stale_over_365d": [k for k, v in out.items() if v.get("exists") and v.get("days_since_release", 0) > 365],
       "names": out}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "names"}, indent=1))
sys.exit(0)
