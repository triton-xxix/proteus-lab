"""P-0067 slice: do the API-backed sources of 3d-asset-server answer 'low poly tree' keyless, with a licence?
Endpoints copied from the repo's src/providers/*.ts; the server itself needs npm and was not run."""
import json, re, time, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (ProteusProbe)", "Accept": "application/json,text/html"}
Q = "low poly tree"


def get(url):
    t = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)
        return r.status, r.read().decode("utf-8", "replace"), round(time.time() - t, 2)
    except urllib.error.HTTPError as e:
        return e.code, "", round(time.time() - t, 2)
    except Exception as e:
        return repr(e)[:80], "", round(time.time() - t, 2)


out = {}
# BlenderKit: public search API, free filter, licence field per asset
s, body, dt = get("https://www.blenderkit.com/api/v1/search/?" + urllib.parse.urlencode({"query": Q + " asset_type:model is_free:true", "page_size": 5}))
try:
    j = json.loads(body); res = j.get("results", [])
    out["blenderkit"] = {"status": s, "s": dt, "count": j.get("count"), "first": [(a.get("name"), a.get("license")) for a in res[:3]]}
except Exception:
    out["blenderkit"] = {"status": s, "s": dt, "body": body[:120]}
# Poly Haven: whole model catalogue, filter locally; all CC0
s, body, dt = get("https://api.polyhaven.com/assets?type=models")
try:
    j = json.loads(body)
    hits = [k for k, v in j.items() if re.search(r"tree", (v.get("name", "") + " " + " ".join(v.get("tags", []))), re.I)]
    out["polyhaven"] = {"status": s, "s": dt, "models": len(j), "tree_hits": len(hits), "first": hits[:3], "licence": "CC0 (site-wide)"}
except Exception:
    out["polyhaven"] = {"status": s, "s": dt, "body": body[:120]}
# ambientCG v3 (materials and HDRIs, few models)
s, body, dt = get("https://ambientcg.com/api/v3/assets?" + urllib.parse.urlencode({"q": Q, "limit": 5, "include": "title"}))
try:
    j = json.loads(body)
    out["ambientcg"] = {"status": s, "s": dt, "total": j.get("totalResults"), "first": [a.get("title") or a.get("id") for a in j.get("assets", j.get("foundAssets", []))[:3]], "licence": "CC0 (site-wide)"}
except Exception:
    out["ambientcg"] = {"status": s, "s": dt, "body": body[:120]}
# itch.io HTML search, asset classification
s, body, dt = get("https://itch.io/search?" + urllib.parse.urlencode({"q": Q, "classification": "assets"}))
out["itchio"] = {"status": s, "s": dt, "game_cells": len(re.findall(r'class="game_cell', body)), "licence": "per item, read from each page"}
# ShareTextures tag list
s, body, dt = get("https://api2.sharetextures.com/api/v0/for-frontend/tag-paths")
try:
    tags = json.loads(body).get("data", [])
    out["sharetextures"] = {"status": s, "s": dt, "tags": len(tags), "tree_tags": [t for t in tags if "tree" in t.lower()][:5]}
except Exception:
    out["sharetextures"] = {"status": s, "s": dt, "body": body[:120]}
# Kenney and Quaternius: HTML catalogues
for name, url in [("kenney", "https://kenney.nl/assets?q=" + urllib.parse.quote(Q)), ("quaternius", "https://quaternius.com/")]:
    s, body, dt = get(url)
    out[name] = {"status": s, "s": dt, "bytes": len(body), "mentions_tree": len(re.findall(r"tree", body, re.I))}
out["link_only_by_design"] = ["fab", "poliigon", "turbosquid"]
print(json.dumps(out, indent=1))
with open(__file__.replace("sources.py", "results.json"), "w") as f:
    json.dump(out, f, indent=1)
