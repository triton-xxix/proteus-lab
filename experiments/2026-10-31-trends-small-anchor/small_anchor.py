"""Refill row 51 (31 Oct 2026): resolve P-0250's zero terms with an anchor near 1% of "spreadsheet".

Modes:
  calibrate   pair each candidate anchor with "spreadsheet" and print its share, to pick one near 0.01
  run ANCHOR  pair every P-0250 term that read zero against "spreadsheet" (last 14 days) with ANCHOR
Same keyless Trends JSON API and helpers as P-0150 (its source head is exec'd, as P-0250 did).
Worldwide, today 3-m, two-second gap. Writes results.json beside this file.
"""
import json, os, sys, time, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1] if len(sys.argv) > 1 else "calibrate"
ANCHOR = sys.argv[2] if len(sys.argv) > 2 else None
sys.argv = sys.argv[:1]
src = open("/Users/triton/PROTEUS/experiments/2026-10-28-P-0150/trends.py").read()
ns = {}
exec(compile(src.split("res = {'cookie_status'")[0], "trends_head", "exec"), ns)
get = ns["get"]

CANDIDATES = ["sumproduct", "xlookup", "pivot table", "countifs", "vlookup", "index match"]


def pair(a, b):
    req = {"comparisonItem": [{"keyword": a, "geo": "", "time": "today 3-m"},
                              {"keyword": b, "geo": "", "time": "today 3-m"}], "category": 0, "property": ""}
    s, body = get("https://trends.google.com/trends/api/explore?hl=en-US&tz=0&req=" + urllib.parse.quote(json.dumps(req)))
    if s != 200:
        return {"explore_status": s}
    w = [x for x in json.loads(body[body.index("{"):])["widgets"] if x["id"] == "TIMESERIES"][0]
    s2, b2 = get("https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=0&req="
                 + urllib.parse.quote(json.dumps(w["request"])) + "&token=" + w["token"])
    if s2 != 200:
        return {"explore_status": s, "series_status": s2}
    pts = json.loads(b2[b2.index("{"):])["default"]["timelineData"]
    v = [p["value"][0] for p in pts]
    b_ = [p["value"][1] for p in pts]
    return {"explore_status": s, "series_status": s2, "points": len(pts),
            "share_all": round(sum(v) / (sum(b_) or 1), 4),
            "share_last14": round(sum(v[-14:]) / (sum(b_[-14:]) or 1), 4),
            "a_nonzero_days": sum(1 for x in v if x > 0), "b_nonzero_days": sum(1 for x in b_ if x > 0)}


res = {"mode": MODE, "cookie_status": get("https://trends.google.com/trends/explore?geo=&q=test")[0], "rows": []}
if MODE == "calibrate":
    for c in CANDIDATES:
        r = pair(c, "spreadsheet")
        r["anchor_candidate"] = c
        res["rows"].append(r)
        print(c, json.dumps(r))
        time.sleep(2)
    out = os.path.join(HERE, "calibrate.json")
else:
    res["anchor"] = ANCHOR
    prev = json.load(open("/Users/triton/PROTEUS/experiments/2026-10-28-P-0250/results.json"))["rows"]
    zeros = [r for r in prev if r.get("share_last14") == 0]
    res["zero_terms_from_p0250"] = len(zeros)
    fails = 0
    for z in zeros:
        if fails >= 3:
            res["rows"].append({"term": z["term"], "status": "not tried (3 refusals in a row)"})
            continue
        r = pair(z["term"], ANCHOR)
        r["term"] = z["term"]
        r["repo"] = z["repo"]
        r["rising_p0150"] = z.get("rising_p0150")
        fails = 0 if r.get("series_status") == 200 else fails + 1
        res["rows"].append(r)
        print(z["term"], json.dumps(r))
        time.sleep(2)
    scored = [r for r in res["rows"] if "share_last14" in r]
    res["summary"] = {"zero_terms": len(zeros), "scored": len(scored),
                      "now_nonzero_last14": sum(r["share_last14"] > 0 for r in scored),
                      "still_zero_last14": sum(r["share_last14"] == 0 for r in scored),
                      "at_1pct_of_small_anchor": sum(r["share_last14"] >= 0.01 for r in scored)}
    print(json.dumps(res["summary"]))
    out = os.path.join(HERE, "results.json")
json.dump(res, open(out, "w"), indent=1)
