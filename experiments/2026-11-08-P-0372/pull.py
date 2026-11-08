"""P-0372: tonight's one-hour volume on GeckoTerminal's newest Solana pools, against the Grinder's gate.

Keyless, three pages, measured only. The gate is read from grinder/paper.py's numbers as of tonight:
vol_h1 at least 10,000 USD, age 1 to 48 hours, liquidity at least 20,000 USD, vol_h24 at least 200,000 USD.
Nothing here changes a rule. Top-10 holders, LP lock and holder count are not in this feed, so a pool
that clears these four is not a pool that clears the whole gate.
"""
import datetime as dt
import json
import pathlib
import statistics
import time
import urllib.request

HERE = pathlib.Path(__file__).parent
BASE = "https://api.geckoterminal.com/api/v2/networks/solana/new_pools?page=%d"
VOL_H1, AGE_MIN, AGE_MAX, LIQ, VOL_H24 = 10_000.0, 1.0, 48.0, 20_000.0, 200_000.0
now = dt.datetime.now(dt.timezone.utc)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


rows = []
for page in (1, 2, 3):
    req = urllib.request.Request(BASE % page, headers={"User-Agent": "proteus-lab/0.1", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    for p in data.get("data", []):
        a = p["attributes"]
        created = dt.datetime.fromisoformat(a["pool_created_at"].replace("Z", "+00:00"))
        rows.append({
            "pool": p["id"], "name": a.get("name"),
            "age_h": round((now - created).total_seconds() / 3600, 3),
            "vol_h1": num(a["volume_usd"].get("h1")), "vol_h24": num(a["volume_usd"].get("h24")),
            "liq": num(a.get("reserve_in_usd")),
        })
    time.sleep(3)

vols = sorted(r["vol_h1"] for r in rows)
n = len(vols)
clear = [r for r in rows if r["vol_h1"] >= VOL_H1]
age_ok = [r for r in rows if AGE_MIN <= r["age_h"] <= AGE_MAX]
four = [r for r in rows if r["vol_h1"] >= VOL_H1 and AGE_MIN <= r["age_h"] <= AGE_MAX
        and r["liq"] >= LIQ and r["vol_h24"] >= VOL_H24]
out = {
    "pulled_at": now.isoformat(), "pools": n,
    "age_h_min": min(r["age_h"] for r in rows), "age_h_max": max(r["age_h"] for r in rows),
    "age_h_median": statistics.median(r["age_h"] for r in rows),
    "vol_h1_median": statistics.median(vols), "vol_h1_p90": vols[int(n * 0.9)], "vol_h1_max": vols[-1],
    "vol_h1_zero": sum(v == 0 for v in vols),
    "clear_vol_h1": len(clear), "clear_within_half_of_line": sum(VOL_H1 / 2 <= v < VOL_H1 for v in vols),
    "in_age_window": len(age_ok), "liq_ok": sum(r["liq"] >= LIQ for r in rows),
    "clear_all_four_feed_gates": len(four),
    "gate_failures_of_those_clearing_vol": {
        "age": sum(not (AGE_MIN <= r["age_h"] <= AGE_MAX) for r in clear),
        "liq": sum(r["liq"] < LIQ for r in clear),
        "vol_h24": sum(r["vol_h24"] < VOL_H24 for r in clear)},
    "top": sorted(rows, key=lambda r: -r["vol_h1"])[:8],
}
(HERE / "results.json").write_text(json.dumps({"summary": out, "rows": rows}, indent=1))
print(json.dumps(out, indent=1))
