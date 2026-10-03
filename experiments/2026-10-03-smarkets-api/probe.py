"""Can Smarkets' politics and current-affairs markets be read keyless? (3 Oct 2026)"""
import json
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent
API = "https://api.smarkets.com/v3"
UA = {"User-Agent": "proteus-probe/0.1", "Accept": "application/json"}


def get(path):
    try:
        with urllib.request.urlopen(urllib.request.Request(API + path, headers=UA), timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return None, repr(e)[:300]


res = {}
st, ev = get("/events/?type_domain=politics&state=upcoming&state=live&limit=50&sort=id")
res["politics_events"] = {"status": st, "n": len(ev.get("events", [])) if isinstance(ev, dict) else None}
if isinstance(ev, dict) and ev.get("events"):
    res["with_markets"] = []
    mk = None
    for e in ev["events"]:
        st2, m = get(f"/events/{e['id']}/markets/")
        if isinstance(m, dict) and m.get("markets"):
            res["with_markets"].append({"event": e["name"], "id": e["id"], "parent": e.get("parent_id"),
                                        "markets": [x["name"] for x in m["markets"]][:5], "n": len(m["markets"])})
            mk = mk or m
    res["events_with_markets"] = len(res["with_markets"])
    if mk:
        mid = mk["markets"][0]["id"]
        st3, ct = get(f"/markets/{mid}/contracts/")
        st4, px = get(f"/markets/{mid}/last_executed_prices/")
        st5, q = get(f"/markets/{mid}/quotes/")
        res["contracts"] = {"status": st3, "sample": ct if isinstance(ct, str) else [c.get("name") for c in ct.get("contracts", [])][:8]}
        res["last_executed"] = {"status": st4, "sample": px if isinstance(px, str) else json.dumps(px)[:400]}
        res["quotes"] = {"status": st5, "sample": q if isinstance(q, str) else json.dumps(q)[:400]}
else:
    res["raw"] = ev if isinstance(ev, str) else json.dumps(ev)[:400]
(OUT / "result.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
