"""P-0374: how much has actually traded on the exchange book's non-weather markets?

Reads exchange/BOOK.csv, takes every market that is not a Munich daily high, asks Smarkets' keyless
volumes endpoint once per market, and reports how many still answer and how many sit under 100.
Volumes only: no prices are requested, so this cannot leak a price into a later blind call.
"""
import csv
import json
import pathlib
import statistics
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).parent
BOOK = "/Users/triton/PROTEUS/exchange/BOOK.csv"
API = "https://api.smarkets.com/v3/markets/%s/volumes/"
THRESH = 100

markets = {}
for r in csv.DictReader(open(BOOK)):
    if r["market"] == "Highest Temperature":
        continue
    m = markets.setdefault(r["market_id"], {"market_id": r["market_id"], "event": r["event"], "market": r["market"],
                                            "calls": [], "open": False})
    m["calls"].append(r["id"])
    if not r["outcome"]:
        m["open"] = True

rows = []
for mid, m in markets.items():
    req = urllib.request.Request(API % mid, headers={"User-Agent": "proteus-exchange/0.1", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        v = (data.get("volumes") or [None])[0]
        rows.append({**m, "reported": bool(v), "volume": (v or {}).get("volume"), "error": None})
    except (urllib.error.URLError, TimeoutError) as e:
        rows.append({**m, "reported": False, "volume": None, "error": str(e)[:80]})
    time.sleep(0.4)

rep = [r for r in rows if r["reported"]]
vols = sorted(r["volume"] or 0 for r in rep)
open_rows = [r for r in rows if r["open"]]
out = {
    "book_non_weather_markets": len(rows), "calls_on_them": sum(len(r["calls"]) for r in rows),
    "reported": len(rep), "errors": sum(1 for r in rows if r["error"]),
    "reported_share": round(len(rep) / len(rows), 3) if rows else None,
    "under_threshold": sum(v < THRESH for v in vols), "threshold": THRESH,
    "median_volume": statistics.median(vols) if vols else None,
    "min_volume": vols[0] if vols else None, "max_volume": vols[-1] if vols else None,
    "open_markets": len(open_rows), "open_reported": sum(r["reported"] for r in open_rows),
    "open_detail": [{k: r[k] for k in ("calls", "event", "market", "reported", "volume")} for r in open_rows],
    "smallest": sorted(({k: r[k] for k in ("calls", "event", "volume")} for r in rep), key=lambda x: x["volume"] or 0)[:8],
}
(HERE / "results.json").write_text(json.dumps({"summary": out, "rows": rows}, indent=1))
print(json.dumps(out, indent=1))
