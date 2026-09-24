#!/usr/bin/env python3
"""P-0006: of pools first seen on one day, what fraction still trade with any volume a day or more later?

Cohorts come from the Grinder's own committed snapshots (grinder/SNAPSHOTS.csv): every mint whose pair was
under 24h old when a scan saw it. The 23 Sep 22:xx scan is the one-day-ago cohort (new_pools-first feed);
the 22 Sep scans are two and three days old. Each mint is rechecked now on DexScreener's keyless
tokens/v1 endpoint (30 mints per call), summing volume over every pair the mint has, so a token that
graduated from the pump.fun curve to pumpswap still counts. Output: results.json and REPORT.md here.
"""
import json, time, urllib.request, urllib.error
from datetime import datetime, timezone
import pandas as pd

HERE = "/Users/triton/PROTEUS/experiments/2026-09-24-P-0006/"
snap = pd.read_csv("/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv")
snap["scan"] = snap["ts"].str[:13]
snap = snap[snap["age_h"] <= 24]
first = snap.sort_values("ts").drop_duplicates("mint")  # the scan that first saw each mint
now = datetime.now(timezone.utc)
first = first[first["scan"] < "2026-09-24"]  # only cohorts at least ~a day old
mints = first["mint"].tolist()
print("cohort mints", len(mints), first.groupby("scan").size().to_dict())

live, calls, errs = {}, 0, []
for i in range(0, len(mints), 30):
    batch = mints[i:i + 30]
    req = urllib.request.Request("https://api.dexscreener.com/tokens/v1/solana/" + ",".join(batch), headers={"User-Agent": "proteus-probe"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            pairs = json.load(r)
    except urllib.error.HTTPError as e:
        errs.append((i, e.code)); continue
    calls += 1
    for p in pairs:
        m = p["baseToken"]["address"]
        v = live.setdefault(m, {"pairs": 0, "vol_h1": 0.0, "vol_h24": 0.0, "txns_h24": 0, "liq": 0.0, "price": None, "dexes": set()})
        v["pairs"] += 1; v["dexes"].add(p.get("dexId"))
        v["vol_h1"] += (p.get("volume") or {}).get("h1") or 0
        v["vol_h24"] += (p.get("volume") or {}).get("h24") or 0
        t = (p.get("txns") or {}).get("h24") or {}; v["txns_h24"] += (t.get("buys") or 0) + (t.get("sells") or 0)
        v["liq"] += (p.get("liquidity") or {}).get("usd") or 0
        if v["price"] is None and p.get("priceUsd"): v["price"] = float(p["priceUsd"])
    time.sleep(0.3)

rows = []
for _, r in first.iterrows():
    v = live.get(r["mint"])
    rows.append({"scan": r["scan"], "mint": r["mint"], "symbol": r["symbol"], "dex_then": r["dex"], "vol_h24_then": r["vol_h24"],
                 "price_then": r["price_usd"], "listed_now": v is not None,
                 "vol_h24_now": v["vol_h24"] if v else 0, "vol_h1_now": v["vol_h1"] if v else 0, "txns_h24_now": v["txns_h24"] if v else 0,
                 "liq_now": v["liq"] if v else 0, "price_now": v["price"] if v else None, "dexes_now": sorted(x for x in v["dexes"] if x) if v else []})
df = pd.DataFrame(rows)
df["ratio"] = df["price_now"] / df["price_then"]
L = ["# P-0006: do yesterday's new pools still trade?", "", "Checked %s UTC, %d DexScreener calls, errors %s." % (now.strftime("%Y-%m-%d %H:%M"), calls, errs), "",
     "| first seen (scan hour UTC) | mints | still listed | any 24h volume | 24h vol >= $1k | 24h vol >= $10k | any 1h volume | median price now/then |", "|---|---|---|---|---|---|---|---|"]
for scan, g in list(df.groupby("scan")) + [("all", df)]:
    n = len(g)
    L.append("| %s | %d | %d | %d (%.0f%%) | %d (%.0f%%) | %d (%.0f%%) | %d (%.0f%%) | %.3f |" % (
        scan, n, g["listed_now"].sum(), (g["vol_h24_now"] > 0).sum(), 100 * (g["vol_h24_now"] > 0).mean(),
        (g["vol_h24_now"] >= 1000).sum(), 100 * (g["vol_h24_now"] >= 1000).mean(), (g["vol_h24_now"] >= 10000).sum(), 100 * (g["vol_h24_now"] >= 10000).mean(),
        (g["vol_h1_now"] > 0).sum(), 100 * (g["vol_h1_now"] > 0).mean(), g["ratio"].median()))
L.append("")
L.append("Median 24h volume at first sight by scan: " + ", ".join("%s $%.0f" % (s, v) for s, v in df.groupby("scan")["vol_h24_then"].median().items()))
L.append("Price down 90%% or more (or unlisted): %d of %d." % (((df["ratio"] <= 0.1) | df["ratio"].isna()).sum(), len(df)))
L.append("Moved off the pump.fun curve to another dex: %d of %d first seen on pumpfun." % (
    sum(1 for _, r in df.iterrows() if r["dex_then"] == "pumpfun" and any(d != "pumpfun" for d in r["dexes_now"])), (df["dex_then"] == "pumpfun").sum()))
open(HERE + "REPORT.md", "w").write("\n".join(L) + "\n")
df.to_json(HERE + "results.json", orient="records", indent=1)
print("\n".join(L))
