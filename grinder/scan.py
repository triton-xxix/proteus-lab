#!/usr/bin/env python3
"""The Grinder: nightly snapshot of young Solana tokens. Keyless sources only.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/scan.py --snapshot [--limit 120]

Sources: DexScreener (profiles, boosts, search, token-pairs), rugcheck.xyz (risk report), public
Solana RPC (mint and freeze authority, supply, largest accounts). pump.fun's own API is geo-blocked
from here and is not used.

Writes one JSON line per token to grinder/cache/snapshots-YYYY-MM-DD.jsonl (gitignored, full detail)
and one compact row per token to grinder/SNAPSHOTS.csv (committed; the pre-registration record).
"""
import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

ROOT = "/Users/triton/PROTEUS/"
CACHE = ROOT + "grinder/cache/"
SNAP_CSV = ROOT + "grinder/SNAPSHOTS.csv"
UA = {"User-Agent": "proteus-lab/0.1 (+https://github.com/triton-xxix/proteus-lab)", "Accept": "application/json"}
RPC = "https://api.mainnet-beta.solana.com"
SNAP_FIELDS = [
    "ts", "mint", "symbol", "name", "dex", "pair", "pair_created_at", "age_h", "price_usd",
    "liq_usd", "mcap_usd", "vol_h1", "vol_h24", "buys_h1", "sells_h1", "chg_h1", "chg_h24",
    "mint_auth", "freeze_auth", "top10_pct", "holders", "lp_locked_pct", "rug_score", "rug_risks",
    "socials",
]


def get(url, **kw):
    for attempt in range(3):
        try:
            r = requests.get(url, headers=UA, timeout=25, **kw)
            if r.status_code == 429:
                time.sleep(2 + attempt * 2)
                continue
            if r.ok:
                return r.json()
            return None
        except Exception:
            time.sleep(1)
    return None


def rpc(method, params):
    try:
        r = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=25)
        return r.json().get("result")
    except Exception:
        return None


GT = "https://api.geckoterminal.com/api/v2/networks/solana/"
WATCHLIST = CACHE + "watchlist.jsonl"
WATCH_H = 48


def gecko(path):
    """GeckoTerminal public API, keyless, about 30 calls a minute. Returns base-token mints in order."""
    d = get(GT + path) or {}
    out = []
    for p in d.get("data", []) or []:
        try:
            tid = p["relationships"]["base_token"]["data"]["id"]
            if tid.startswith("solana_"):
                out.append((tid.split("_", 1)[1], (p.get("attributes") or {}).get("pool_created_at")))
        except Exception:
            continue
    time.sleep(2.1)
    return out


def watchlist_update(new_items):
    """Append tonight's brand-new pools; return every mint first seen within WATCH_H hours. This is
    how a pool that is minutes old tonight becomes a 1-to-48h candidate on the next run."""
    os.makedirs(CACHE, exist_ok=True)
    now = time.time()
    seen = {}
    if os.path.exists(WATCHLIST):
        for line in open(WATCHLIST):
            try:
                e = json.loads(line); seen[e["mint"]] = e["first_seen"]
            except Exception:
                continue
    with open(WATCHLIST, "a") as fh:
        for mint, created in new_items:
            if mint in seen:
                continue
            seen[mint] = now
            fh.write(json.dumps({"mint": mint, "first_seen": now, "pool_created_at": created}) + "\n")
    return [m for m, t in seen.items() if now - t <= WATCH_H * 3600]


def discover(limit):
    """Candidate Solana mints, in the order they are scanned (the limit cuts the tail).

    Order changed 2026-09-24 after two nights of zero entries. The v0.2 order put GeckoTerminal's
    new_pools first: pools minutes old with a few thousand dollars in them, which cannot clear a
    $20k liquidity or $200k volume gate by construction, and the limit then cut everything else.
    The gate never got a fair test. Now the feeds that surface pools already trading in size come
    first: GeckoTerminal trending pools over 1h, 6h and 24h, then the pump-fun and pumpswap pools
    by 24h transactions, then DexScreener boosts and profiles. The new_pools watchlist still runs
    (a pool minutes old tonight is a 1-to-48h candidate tomorrow) but its mints go last.
    """
    mints = []

    def add(addr):
        if addr and addr not in mints:
            mints.append(addr)

    for dur in ("1h", "6h", "24h"):
        for m, _ in gecko("trending_pools?page=1&duration=%s" % dur):
            add(m)
    for dex in ("pump-fun", "pumpswap"):
        for page in (1, 2):
            for m, _ in gecko("dexes/%s/pools?page=%d&sort=h24_tx_count_desc" % (dex, page)):
                add(m)

    for url in ("https://api.dexscreener.com/token-boosts/top/v1",
                "https://api.dexscreener.com/token-boosts/latest/v1",
                "https://api.dexscreener.com/token-profiles/latest/v1"):
        for t in (get(url) or []):
            if t.get("chainId") == "solana":
                add(t.get("tokenAddress"))
    for url in ("https://api.rugcheck.xyz/v1/stats/trending", "https://api.rugcheck.xyz/v1/stats/recent"):
        for t in (get(url) or []):
            add(t.get("mint") or t.get("address"))

    fresh = []
    for page in (1, 2, 3):
        fresh += gecko("new_pools?page=%d" % page)
    for m in watchlist_update(fresh):
        add(m)
    return mints[:limit]


def best_pair(mint):
    pairs = get("https://api.dexscreener.com/token-pairs/v1/solana/" + mint) or []
    pairs = [p for p in pairs if (p.get("quoteToken") or {}).get("symbol") in ("SOL", "WSOL", "USDC", "USDT")]
    if not pairs:
        return None
    return max(pairs, key=lambda p: ((p.get("liquidity") or {}).get("usd") or 0))


def rug(mint):
    rep = get("https://api.rugcheck.xyz/v1/tokens/%s/report" % mint)
    if not rep:
        time.sleep(1.5)
        rep = get("https://api.rugcheck.xyz/v1/tokens/%s/report" % mint)
    if not rep:
        summ = get("https://api.rugcheck.xyz/v1/tokens/%s/report/summary" % mint) or {}
        return {"score": summ.get("score_normalised"), "risks": [r.get("name") for r in summ.get("risks", [])],
                "lp_locked": summ.get("lpLockedPct"), "holders": None, "top10": None}
    # rugcheck's topHolders list includes the liquidity pool's own token account (checked 2026-09-24:
    # the pumpswap pool sat first at 7.5 percent). The rule is about holders, so accounts owned by a
    # market are left out of the top-10 share.
    pools = {m.get("pubkey") for m in (rep.get("markets") or []) if m.get("pubkey")}
    top = [h for h in (rep.get("topHolders") or []) if h.get("owner") not in pools and h.get("address") not in pools]
    top10 = sum(float(h.get("pct") or 0) for h in top[:10]) if top else None
    return {"score": rep.get("score_normalised"), "risks": [r.get("name") for r in rep.get("risks", [])],
            "lp_locked": (rep.get("markets") or [{}])[0].get("lp", {}).get("lpLockedPct") if rep.get("markets") else None,
            "holders": rep.get("totalHolders"), "top10": top10}


def authorities(mint):
    """Mint and freeze authority from the public RPC. Top-10 share is NOT read here any more:
    getTokenLargestAccounts answers 429 "Too many requests for a specific RPC call" on the public
    endpoint even for a single call (checked 2026-09-24), which is why two thirds of snapshot rows
    had no top10_pct. rugcheck's full report carries the top holders and is used instead."""
    res = rpc("getAccountInfo", [mint, {"encoding": "jsonParsed"}]) or {}
    info = (((res.get("value") or {}).get("data") or {}).get("parsed") or {}).get("info") or {}
    return {"mint_auth": info.get("mintAuthority"), "freeze_auth": info.get("freezeAuthority"), "top10": None}


def snapshot(limit):
    ts = datetime.now(timezone.utc)
    ts_iso = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(CACHE, exist_ok=True)
    mints = discover(limit)
    print("candidates", len(mints), file=sys.stderr)
    rows = []
    with open(CACHE + "snapshots-%s.jsonl" % ts.strftime("%Y-%m-%d"), "a") as raw:
        for i, mint in enumerate(mints):
            p = best_pair(mint)
            if not p:
                continue
            created = p.get("pairCreatedAt")
            age_h = round((ts.timestamp() * 1000 - created) / 3.6e6, 1) if created else None
            r = rug(mint)
            a = authorities(mint)
            top10 = a["top10"] if a["top10"] is not None else r["top10"]
            row = {
                "ts": ts_iso, "mint": mint,
                "symbol": (p.get("baseToken") or {}).get("symbol"), "name": (p.get("baseToken") or {}).get("name"),
                "dex": p.get("dexId"), "pair": p.get("pairAddress"), "pair_created_at": created, "age_h": age_h,
                "price_usd": p.get("priceUsd"), "liq_usd": (p.get("liquidity") or {}).get("usd"),
                "mcap_usd": p.get("marketCap") or p.get("fdv"),
                "vol_h1": (p.get("volume") or {}).get("h1"), "vol_h24": (p.get("volume") or {}).get("h24"),
                "buys_h1": ((p.get("txns") or {}).get("h1") or {}).get("buys"),
                "sells_h1": ((p.get("txns") or {}).get("h1") or {}).get("sells"),
                "chg_h1": (p.get("priceChange") or {}).get("h1"), "chg_h24": (p.get("priceChange") or {}).get("h24"),
                "mint_auth": a["mint_auth"], "freeze_auth": a["freeze_auth"], "top10_pct": top10,
                # rugcheck reports totalHolders 0 for fresh tokens it has not indexed; 0 means unknown, so
            # write empty and let the rules treat it as unmeasured (found by the first nightly run).
            "holders": (r["holders"] if r["holders"] else None), "lp_locked_pct": r["lp_locked"], "rug_score": r["score"],
                "rug_risks": ";".join(x for x in r["risks"] if x), "socials": len((p.get("info") or {}).get("socials") or []),
            }
            rows.append(row)
            raw.write(json.dumps({"row": row, "pair": p}) + "\n")
            time.sleep(0.35)
    new = not os.path.exists(SNAP_CSV)
    with open(SNAP_CSV, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SNAP_FIELDS, extrasaction="ignore")
        if new:
            w.writeheader()
        for row in rows:
            w.writerow(row)
    print("snapshot rows", len(rows))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", action="store_true")
    ap.add_argument("--limit", type=int, default=120)
    args = ap.parse_args()
    if args.snapshot:
        snapshot(args.limit)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
