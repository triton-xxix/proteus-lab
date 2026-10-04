"""P-0058: is football-data's latest result really 20 Sep? Cached files vs live, plus fixturedownload's view."""
import io
import json
import os

import pandas as pd
import requests

CACHE = "/Users/triton/PROTEUS/pitch/cache/"
UA = {"User-Agent": "Mozilla/5.0 (proteus probe)"}
out = {"cache": {}, "live": {}}
for div in ["E0", "E1", "SP1", "D1", "I1", "F1", "N1", "P1", "SC0"]:
    p = f"{CACHE}{div}-2627.csv"
    if os.path.exists(p):
        df = pd.read_csv(p, encoding="utf-8-sig", on_bad_lines="skip")
        d = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        out["cache"][div] = {"rows": len(df), "max_date": str(d.max().date()),
                             "mtime": pd.Timestamp(os.path.getmtime(p), unit="s").isoformat()}
    r = requests.get(f"https://www.football-data.co.uk/mmz4281/2627/{div}.csv", headers=UA, timeout=40)
    live = {"status": r.status_code, "last_modified": r.headers.get("Last-Modified")}
    if r.ok:
        df = pd.read_csv(io.StringIO(r.content.decode("utf-8-sig", "replace")), on_bad_lines="skip")
        d = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        live.update(rows=len(df), max_date=str(d.max().date()),
                    after_20sep=int((d > "2026-09-20").sum()))
    out["live"][div] = live

# What matches does fixturedownload say were played after 20 Sep in E0?
fd = {}
for name in sorted(os.listdir(CACHE)):
    if name.startswith("fixturedownload"):
        fd[name] = pd.Timestamp(os.path.getmtime(CACHE + name), unit="s").isoformat()
out["fixturedownload_files"] = fd
json.dump(out, open("/Users/triton/PROTEUS/experiments/2026-10-04-P-0058/results.json", "w"), indent=2)
for div in out["live"]:
    c = out["cache"].get(div, {})
    l = out["live"][div]
    print(div, "cache", c.get("rows"), c.get("max_date"), "| live", l.get("status"), l.get("rows"),
          l.get("max_date"), "after 20 Sep", l.get("after_20sep"), "LM", l.get("last_modified"))
print("fixturedownload files:", fd)
