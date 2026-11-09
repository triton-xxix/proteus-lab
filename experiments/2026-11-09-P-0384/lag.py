"""P-0384 (number confirmed by the GO line): new_pools page against the single-pool endpoint, GeckoTerminal, Solana.

Twelve pools from page 1 of new_pools, read on the page and immediately after on the single endpoint, in three rounds a minute apart.
Rate limit is about 30 calls a minute, so 13 calls a round with a 2.5 s gap. Numbers: h1 volume in USD and reserve in USD on both.
"""
import json
import pathlib
import statistics
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).parent
BASE = "https://api.geckoterminal.com/api/v2/networks/solana"
UA = {"User-Agent": "proteus-research/1.0", "Accept": "application/json;version=20230302"}


RETRIES = {"429": 0}


def get(path):
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(BASE + path, headers=UA), timeout=30).read())
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == 4:
                raise
            RETRIES["429"] += 1
            time.sleep(20 + 10 * i)


def row(a):
    a = a["attributes"]
    return {"h1": float(a["volume_usd"]["h1"] or 0), "reserve": float(a["reserve_in_usd"] or 0), "created": a["pool_created_at"], "name": a["name"]}


rounds = []
chosen = None
for r in range(3):
    t0 = time.time()
    page = {p["attributes"]["address"]: row(p) for p in get("/new_pools?page=1")["data"]}
    if chosen is None:
        chosen = list(page)[:12]
    rec = {"round": r, "at": t0, "page_size": len(page), "pools": []}
    for addr in chosen:
        time.sleep(2.5)
        try:
            s = row(get(f"/pools/{addr}")["data"])
        except Exception as e:
            rec["pools"].append({"address": addr, "error": str(e)[:80]})
            continue
        rec["pools"].append({"address": addr, "on_page": addr in page, "page": page.get(addr), "single": s, "secs_after_page": round(time.time() - t0, 1)})
    rounds.append(rec)
    if r < 2:
        time.sleep(max(0, 60 - (time.time() - t0)))

(HERE / "results.json").write_text(json.dumps(rounds, indent=1))
ratios, zero = [], 0
for r in rounds:
    for p in r["pools"]:
        if p.get("on_page") and p.get("page") and p["single"]["h1"] > 0:
            if p["page"]["h1"] == 0:
                zero += 1
            else:
                ratios.append(max(p["page"]["h1"], p["single"]["h1"]) / min(p["page"]["h1"], p["single"]["h1"]))
print("429 retries", RETRIES["429"])
print("pairs with both above zero", len(ratios), "page zero while single above", zero)
if ratios:
    print("ratio of larger to smaller h1: median", round(statistics.median(ratios), 3), "p90", round(sorted(ratios)[int(0.9 * len(ratios))], 3), "max", round(max(ratios), 2),
          "share within 1.1x", round(sum(x <= 1.1 for x in ratios) / len(ratios), 2), "over 2x", round(sum(x > 2 for x in ratios) / len(ratios), 2))
for r in rounds:
    print("round", r["round"], "on page", sum(1 for p in r["pools"] if p.get("on_page")), "of", len(r["pools"]), "errors", sum(1 for p in r["pools"] if "error" in p),
          "median secs after page", statistics.median([p["secs_after_page"] for p in r["pools"] if "secs_after_page" in p] or [0]))
