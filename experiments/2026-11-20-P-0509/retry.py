"""Retry the rows of results.json whose Overpass run failed (502/504 on overpass-api.de), once, 10 s apart.
Re-parses with HippoMaps to get the QL again. Writes retry.json beside results.json."""
import json
import sys
import time
import urllib.parse
import urllib.request

IN, OUT = sys.argv[1], sys.argv[2]
UA = {"User-Agent": "proteus-lab-probe/1.0"}
rows = [r for r in json.load(open(IN))["rows"] if "run_error" in r]
out = []
for r in rows:
    time.sleep(10)
    p = json.load(urllib.request.urlopen(urllib.request.Request(
        "https://hippomaps.ch/api/search/query?" + urllib.parse.urlencode({"q": r["q"], "lang": "en"}), headers=UA), timeout=90))
    row = {"q": r["q"]}
    t0 = time.time()
    try:
        res = json.load(urllib.request.urlopen(urllib.request.Request(
            "https://overpass-api.de/api/interpreter", data=urllib.parse.urlencode({"data": p["query"]}).encode(),
            headers=UA), timeout=150))
        row["elements"] = len(res.get("elements", []))
    except Exception as e:  # noqa: BLE001
        row["run_error"] = str(e)[:200]
    row["run_s"] = round(time.time() - t0, 1)
    out.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False)
