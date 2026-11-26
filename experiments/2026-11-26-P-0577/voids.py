"""P-0577: Smarkets state and info.reason for every Munich daily-high market id in exchange logs.
Joins volume (munich_volumes.jsonl, last row per id) and P-0553's gap flag if a ladder is in snapshots."""
import json, sys, time, urllib.request, urllib.error, collections

ROOT = "/Users/triton/PROTEUS/exchange/"
OUT = sys.argv[1]
ids = {}
for fn in ("munich_outcomes.jsonl", "munich_volumes.jsonl"):
    for line in open(ROOT + fn):
        if line.strip():
            r = json.loads(line)
            ids.setdefault(r["market_id"], {})["event"] = r["event"]
            if "volume" in r:
                ids[r["market_id"]]["volume"] = r["volume"]
                ids[r["market_id"]]["traded"] = len(r.get("traded") or [])
for m in json.load(open("/Users/triton/PROTEUS/experiments/2026-11-26-P-0554/p0554-market.json"))["markets"]:
    ids.setdefault(m["id"], {}).setdefault("event", m["name"])
for line in open(ROOT + "munich_outcomes.jsonl"):
    if line.strip():
        r = json.loads(line)
        ids[r["market_id"]]["winner"] = r["winner"]

ids_list = sorted(ids)
markets = {}
for i in range(0, len(ids_list), 20):
    chunk = ids_list[i:i + 20]
    url = "https://api.smarkets.com/v3/markets/%s/" % ",".join(chunk)
    try:
        j = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus"}), timeout=30))
        for m in j.get("markets", []):
            markets[m["id"]] = m
    except urllib.error.HTTPError as e:
        print("chunk", i, "HTTP", e.code)
    time.sleep(1)

rows = []
for mid in ids_list:
    m = markets.get(mid)
    row = dict(market_id=mid, **ids[mid])
    if m:
        row.update(state=m["state"], reason=(m.get("info") or {}).get("reason"), name=m["name"], modified=m["modified"])
    else:
        row["state"] = "not answered"
    rows.append(row)
    print(row)

by_state = collections.Counter(r["state"] for r in rows)
reasons = collections.Counter((r["state"], (r.get("reason") or "")[-60:]) for r in rows if r["state"] != "not answered")
summ = {"ids": len(rows), "answered": len(markets), "by_state": by_state,
        "reasons": [{"state": k[0], "reason_tail": k[1], "n": n} for k, n in reasons.most_common()],
        "voided": [r for r in rows if r["state"] == "voided"]}
print(json.dumps(summ, indent=1, default=str))
json.dump({"summary": summ, "rows": rows}, open(OUT + "/results.json", "w"), indent=1, default=str)
