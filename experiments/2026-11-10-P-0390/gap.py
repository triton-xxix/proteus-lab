"""P-0390: GeckoTerminal new_pools page v /pools/ADDRESS at a two-second gap.
Three rounds; each round reads page 1 of Solana new_pools, takes the first 3 pools with volume, then
reads each pool's single endpoint about 2 s apart. Records one-hour volume and transaction counts from
both, the real gap in seconds, and any 429 waits. Keyless. Run: python3 gap.py (writes results.json)."""
import json, os, statistics, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://api.geckoterminal.com/api/v2/networks/solana/"
waits = []


def get(path):
    for attempt in range(4):
        req = urllib.request.Request(BASE + path, headers={"Accept": "application/json",
                                                           "User-Agent": "proteus-probe"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r), time.time()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                waits.append(path)
                time.sleep(15)
                continue
            raise
    return None, time.time()


def h1(a):
    t = a["transactions"]["h1"]
    return float(a["volume_usd"]["h1"] or 0), t["buys"] + t["sells"]


reads = []
for rnd in range(3):
    page, t_page = get("new_pools?page=1")
    if not page:
        continue
    picks = [p for p in page["data"] if float(p["attributes"]["volume_usd"]["h1"] or 0) > 0][:3]
    for p in picks:
        a = p["attributes"]
        pv, ptx = h1(a)
        time.sleep(2)
        single, t_single = get("pools/" + a["address"])
        if not single:
            continue
        sv, stx = h1(single["data"]["attributes"])
        reads.append({"round": rnd, "pool": a["address"], "name": a["name"],
                      "created": a["pool_created_at"], "gap_s": round(t_single - t_page, 1),
                      "page_vol_h1": pv, "single_vol_h1": sv, "page_tx_h1": ptx, "single_tx_h1": stx,
                      "ratio": round(sv / pv, 3) if pv else None})
    time.sleep(10)

ratios = [r["ratio"] for r in reads if r["ratio"] is not None]
res = {"reads": len(reads), "single_above": sum(1 for r in reads if r["single_vol_h1"] > r["page_vol_h1"]),
       "equal": sum(1 for r in reads if r["single_vol_h1"] == r["page_vol_h1"]),
       "single_below": sum(1 for r in reads if r["single_vol_h1"] < r["page_vol_h1"]),
       "tx_differ": sum(1 for r in reads if r["single_tx_h1"] != r["page_tx_h1"]),
       "median_ratio": round(statistics.median(ratios), 3) if ratios else None,
       "max_ratio": max(ratios) if ratios else None,
       "median_gap_s": round(statistics.median([r["gap_s"] for r in reads]), 1) if reads else None,
       "max_gap_s": max((r["gap_s"] for r in reads), default=None),
       "rate_limit_waits": len(waits), "rows": reads}
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
for r in reads:
    print(r["round"], r["name"], r["gap_s"], r["page_vol_h1"], r["single_vol_h1"], r["page_tx_h1"], r["single_tx_h1"])
