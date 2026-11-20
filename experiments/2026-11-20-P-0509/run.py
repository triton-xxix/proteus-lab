"""P-0509: does HippoMaps' parser turn 15 plain-English place queries into Overpass QL that returns results?

Parse: hippomaps.ch/api/search/query (public, the page calls it before each search; relayed to
overpass-search, which is not in the hippomaps repo). Run: the returned QL on overpass-api.de
(public instance), not their own engine. Writes results.json.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

OUT = sys.argv[1]
UA = {"User-Agent": "proteus-lab-probe/1.0"}
QUERIES = [
    "pubs in Bristol",
    "cafés near a bus stop in Zurich",
    "pharmacies in Leeds",
    "petrol stations along the M4",
    "bridges over the Danube 50 km from Novi Sad",
    "playgrounds near a school in Manchester",
    "pubs within 200 m of a railway station in York",
    "museums in Edinburgh",
    "Tesco in Cardiff",
    "campsites near a lake in Cumbria",
    "drinking water in Hyde Park",
    "EV charging stations in Brighton",
    "castles in Wales",
    "restaurants between the river and the cathedral in Durham",
    "bike shops far from a motorway in Oxford",
]


def get_json(url, data=None, timeout=90):
    req = urllib.request.Request(url, data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


rows = []
for q in QUERIES:
    row = {"q": q}
    try:
        p = get_json("https://hippomaps.ch/api/search/query?" + urllib.parse.urlencode({"q": q, "lang": "en"}))
        row["understood"] = p.get("understood")
        row["exact"] = p.get("exact")
        ql = p.get("query")
        row["ql_len"] = len(ql or "")
        row["has_ql"] = bool(ql)
    except Exception as e:  # noqa: BLE001
        row["parse_error"] = str(e)[:200]
        ql = None
    if ql:
        t0 = time.time()
        try:
            res = get_json("https://overpass-api.de/api/interpreter",
                           data=urllib.parse.urlencode({"data": ql}).encode(), timeout=120)
            row["elements"] = len(res.get("elements", []))
            rem = res.get("remark")
            if rem:
                row["remark"] = rem[:200]
        except Exception as e:  # noqa: BLE001
            row["run_error"] = str(e)[:200]
        row["run_s"] = round(time.time() - t0, 1)
    rows.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
    time.sleep(2)

summary = {
    "queries": len(rows),
    "parsed_to_ql": sum(1 for r in rows if r.get("has_ql")),
    "exact": sum(1 for r in rows if r.get("exact")),
    "ran_ok": sum(1 for r in rows if "elements" in r),
    "returned_results": sum(1 for r in rows if r.get("elements", 0) > 0),
    "run_errors": sum(1 for r in rows if "run_error" in r),
}
print(json.dumps(summary))
with open(OUT, "w") as f:
    json.dump({"summary": summary, "rows": rows}, f, indent=1, ensure_ascii=False)
