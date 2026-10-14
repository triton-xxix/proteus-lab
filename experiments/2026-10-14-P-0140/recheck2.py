#!/usr/bin/env python3
"""P-0140: recheck the P-0137 cohort (85 pump.fun pools captured 13 Oct 11:28Z to 11:33Z) at 24h+.
Two counts, so graduated tokens are not undercounted:
  1. curve pool: reserve_in_usd of the captured pool address (pools/multi, 30 a call);
  2. token: the base mint from (1), then tokens/multi gives total_reserve_in_usd across every pool the
     token has (a graduated token's PumpSwap pool included); for any token above the line, tokens/{mint}/pools
     lists the pools so the dex can be named.
GeckoTerminal keyless, about 30 requests a minute."""
import json, time
from datetime import datetime, timezone
import requests

B = "https://api.geckoterminal.com/api/v2"
H = {"Accept": "application/json", "User-Agent": "proteus-lab/0.1"}
SRC = "/Users/triton/PROTEUS/experiments/2026-10-13-P-0137/cohort.json"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-14-P-0140/results.json"
LIQ = 5000.0
calls = {"n": 0, "429": 0, "status": {}}


def get(path):
    for _ in range(4):
        calls["n"] += 1
        r = requests.get(B + path, headers=H, timeout=30)
        calls["status"][str(r.status_code)] = calls["status"].get(str(r.status_code), 0) + 1
        if r.status_code == 429:
            calls["429"] += 1; time.sleep(20); continue
        return r
    return r


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


c = json.load(open(SRC))
now = datetime.now(timezone.utc)
pools = c["pools"]
addrs = [p["pool"] for p in pools]
created = [datetime.strptime(p["created"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) for p in pools]
age_h = [round((now - t).total_seconds() / 3600, 2) for t in created]
print("recheck at", now.strftime("%Y-%m-%dT%H:%M:%SZ"), "cohort", len(addrs), "age", min(age_h), "to", max(age_h), "h", flush=True)

# 1. curve pools
curve, mint_of = {}, {}
for i in range(0, len(addrs), 30):
    r = get("/networks/solana/pools/multi/" + ",".join(addrs[i:i + 30]))
    for x in (r.json().get("data") or []) if r.status_code == 200 else []:
        a = x["attributes"]
        curve[a["address"]] = {"liq": fnum(a.get("reserve_in_usd")), "fdv": fnum(a.get("fdv_usd")),
                               "vol24": fnum(((a.get("volume_usd") or {}).get("h24"))),
                               "tx24": (a.get("transactions") or {}).get("h24")}
        base = ((x.get("relationships") or {}).get("base_token") or {}).get("data") or {}
        if base.get("id"):
            mint_of[a["address"]] = base["id"].split("_", 1)[-1]
    time.sleep(2.2)
print("pools/multi returned", len(curve), "of", len(addrs), "; mints", len(mint_of), flush=True)

# 2. tokens, total reserve across all pools
mints = sorted(set(mint_of.values()))
tok = {}
for i in range(0, len(mints), 30):
    r = get("/networks/solana/tokens/multi/" + ",".join(mints[i:i + 30]))
    for x in (r.json().get("data") or []) if r.status_code == 200 else []:
        a = x["attributes"]
        tok[a["address"]] = {"total_reserve": fnum(a.get("total_reserve_in_usd")), "fdv": fnum(a.get("fdv_usd")),
                             "vol24": fnum(((a.get("volume_usd") or {}).get("h24"))), "symbol": a.get("symbol")}
    time.sleep(2.2)
print("tokens/multi returned", len(tok), "of", len(mints), flush=True)

# 3. name the dex for any token above the line by total reserve
above_tok = [m for m in mints if (tok.get(m, {}).get("total_reserve") or 0) > LIQ]
dex_of = {}
for m in above_tok:
    r = get("/networks/solana/tokens/%s/pools" % m)
    if r.status_code == 200:
        dex_of[m] = [{"pool": x["attributes"]["address"], "dex": x["relationships"]["dex"]["data"]["id"],
                      "liq": fnum(x["attributes"].get("reserve_in_usd"))} for x in (r.json().get("data") or [])]
    time.sleep(2.2)

rows = []
for p, h in zip(pools, age_h):
    a = p["pool"]; m = mint_of.get(a)
    cv = curve.get(a) or {}; tk = tok.get(m) or {}
    rows.append({"pool": a, "name": p["name"], "mint": m, "age_h": h, "liq_at_capture": p["liq_at_capture"],
                 "curve_liq": cv.get("liq"), "curve_returned": a in curve, "token_total_reserve": tk.get("total_reserve"),
                 "token_fdv": tk.get("fdv"), "token_vol24": tk.get("vol24"), "curve_tx24": cv.get("tx24"),
                 "above_curve": (cv.get("liq") or 0) > LIQ, "above_token": (tk.get("total_reserve") or 0) > LIQ,
                 "pools": dex_of.get(m)})
summary = {
    "cohort": len(rows), "age_h": [min(age_h), max(age_h)],
    "curve_returned": sum(r["curve_returned"] for r in rows), "token_returned": sum(1 for r in rows if r["token_total_reserve"] is not None),
    "above_5k_curve": sum(r["above_curve"] for r in rows), "above_5k_token_total": sum(r["above_token"] for r in rows),
    "above_5k_at_capture": c.get("above_5k_at_capture"),
    "graduated_named": {r["name"]: [q["dex"] for q in (r["pools"] or [])] for r in rows if r["above_token"]},
    "curve_liq_median": sorted([r["curve_liq"] or 0 for r in rows])[len(rows) // 2],
    "curve_tx24_zero": sum(1 for r in rows if not ((r["curve_tx24"] or {}).get("buys") or (r["curve_tx24"] or {}).get("sells"))),
    "calls": calls,
}
json.dump({"probe": "P-0140", "rechecked_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "liq_line": LIQ, "summary": summary, "rows": rows},
          open(OUT, "w"), indent=1)
print(json.dumps(summary), flush=True)
for r in rows:
    if r["above_curve"] or r["above_token"] or (r["liq_at_capture"] or 0) > LIQ:
        print("  %-28s capture %8.0f  curve %8s  token total %8s  %s" % (r["name"], r["liq_at_capture"] or 0, r["curve_liq"], r["token_total_reserve"],
                                                                    [q["dex"] for q in (r["pools"] or [])]))
