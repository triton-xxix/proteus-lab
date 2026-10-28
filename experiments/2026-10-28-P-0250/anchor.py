"""P-0250: P-0150's 34 radar terms again, each paired with one fixed anchor term per request.

Trends scales every request 0 to 100 across the terms in it, so with the same anchor in each pair the
term's numbers become a share of the anchor's volume, comparable across all 34. Anchor: "spreadsheet"
(steady, mid volume, no news cycle). Worldwide, today 3-m, two-second gap. Rising is copied from
P-0150's results so the two runs are read side by side.
"""
import json, sys, time, urllib.parse

sys.argv = sys.argv[:1]
import importlib.util
spec = importlib.util.spec_from_file_location("t", "/Users/triton/PROTEUS/experiments/2026-10-28-P-0150/trends.py")
# trends.py runs its pull at import; reuse only its opener and helpers by reading the source instead.
src = open("/Users/triton/PROTEUS/experiments/2026-10-28-P-0150/trends.py").read()
head = src.split("res = {'cookie_status'")[0]
ns = {}
exec(compile(head, "trends_head", "exec"), ns)
get, term = ns["get"], ns["term"]

ANCHOR = "spreadsheet"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-28-P-0250/results.json"
prev = {r["repo"]: r for r in json.load(open("/Users/triton/PROTEUS/experiments/2026-10-28-P-0150/results.json"))["rows"]}

res = {"anchor": ANCHOR, "cookie_status": get("https://trends.google.com/trends/explore?geo=&q=test")[0], "rows": []}
fails = 0
for repo in ns["repos"]:
    t = term(repo)
    row = {"repo": repo, "term": t, "rising_p0150": prev.get(repo, {}).get("rising")}
    if fails >= 3:
        row["status"] = "not tried (3 refusals in a row)"
        res["rows"].append(row)
        continue
    req = {"comparisonItem": [{"keyword": t, "geo": "", "time": "today 3-m"},
                              {"keyword": ANCHOR, "geo": "", "time": "today 3-m"}], "category": 0, "property": ""}
    s, body = get("https://trends.google.com/trends/api/explore?hl=en-US&tz=0&req=" + urllib.parse.quote(json.dumps(req)))
    row["explore_status"] = s
    if s == 200:
        fails = 0
        w = [x for x in json.loads(body[body.index("{"):])["widgets"] if x["id"] == "TIMESERIES"][0]
        s2, b2 = get("https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=0&req="
                     + urllib.parse.quote(json.dumps(w["request"])) + "&token=" + w["token"])
        row["series_status"] = s2
        if s2 == 200:
            pts = json.loads(b2[b2.index("{"):])["default"]["timelineData"]
            a = [p["value"][1] for p in pts]
            v = [p["value"][0] for p in pts]
            sa = sum(a) or 1
            row["share_of_anchor"] = round(sum(v) / sa, 4)
            row["share_last14"] = round(sum(v[-14:]) / (sum(a[-14:]) or 1), 4)
    else:
        fails += 1
    res["rows"].append(row)
    time.sleep(2)

scored = [r for r in res["rows"] if "share_of_anchor" in r]
rising = [r for r in scored if r["rising_p0150"]]
res["summary"] = {"n": len(res["rows"]), "scored": len(scored),
                  "rising_scored": len(rising),
                  "rising_at_1pct_last14": sum(r["share_last14"] >= 0.01 for r in rising),
                  "rising_at_zero_last14": sum(r["share_last14"] == 0 for r in rising),
                  "all_at_1pct_last14": sum(r["share_last14"] >= 0.01 for r in scored),
                  "statuses": sorted({str(r.get("explore_status")) for r in res["rows"]})}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res["summary"]))
for r in sorted(scored, key=lambda r: -r["share_last14"])[:8]:
    print(r["term"], r["share_last14"], "rising" if r["rising_p0150"] else "")
