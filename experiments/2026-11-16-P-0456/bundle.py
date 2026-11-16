#!/usr/bin/env python3
"""P-0456: for 20 live pump.fun creates, what share of the 1,000,000,000 supply do the creator plus
every other wallet that bought in the creation slot hold at the end of that slot?

Called shot (before the run): at least 8 of 20 have a same-slot buyer besides the creator, and the
median creator-plus-bundle share is between 2% and 10%.

Read-only, keyless. Listener and creator logic from experiments/2026-11-13-P-0440/listen.py
(same mint-authority filter, same 2 s pace). For each sampled create: getSignaturesForAddress on
the mint, keep successful transactions in the create's slot, read each one's postTokenBalances for
the mint, take each owner's last balance in the slot, and drop the bonding curve (the owner whose
balance is the largest, the unsold curve stock). Nobody buys anything.
"""
import asyncio, importlib.util, json, os, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("listen", "/Users/triton/PROTEUS/experiments/2026-11-13-P-0440/listen.py")
L = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0]]
spec.loader.exec_module(L)
MIN, SAMPLE = 1.5, 20


def slot_holders(create):
    t = L.stake(create["sig"])
    if not t or "mint" not in t:
        return {"sig": create["sig"], "status": (t or {}).get("status", "no-tx")}
    mint, creator, slot = t["mint"], t["creator"], create["slot"]
    sigs = L.rpc("getSignaturesForAddress", [mint, {"limit": 40, "commitment": "confirmed"}]) or []
    same = [s for s in sigs if s.get("slot") == slot and s.get("err") is None]
    same.sort(key=lambda s: s.get("blockTime") or 0)
    last = {}
    for s in same[:8]:
        tx = L.rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1,
                                                       "commitment": "confirmed"}])
        if not tx:
            continue
        for b in tx["meta"].get("postTokenBalances") or []:
            if b["mint"] == mint and b.get("owner"):
                last[b["owner"]] = float(b["uiTokenAmount"]["uiAmount"] or 0)
    if not last:
        return {"sig": create["sig"], "status": "no-balances"}
    # first run: dropping only the single largest owner left another curve-sized balance in the
    # bundle (shares of 100%), so every owner holding half the supply or more counts as curve stock
    curve = max(last, key=last.get)
    curve_like = {o for o, v in last.items() if v >= 0.5 * L.SUPPLY}
    others = {o: v for o, v in last.items() if o not in curve_like}
    creator_tok = others.get(creator, 0.0)
    bundle = {o: v for o, v in others.items() if o != creator and v > 0}
    return {"sig": create["sig"], "mint": mint, "slot": slot, "same_slot_txs": len(same), "read_txs": min(len(same), 8),
            "creator_share": creator_tok / L.SUPPLY, "bundle_wallets": len(bundle),
            "bundle_share": sum(bundle.values()) / L.SUPPLY,
            "creator_plus_bundle_share": (creator_tok + sum(bundle.values())) / L.SUPPLY,
            "curve_share_left": last[curve] / L.SUPPLY, "curve_like_owners": len(curve_like),
            "holders": {o[:8]: round(v / L.SUPPLY, 4) for o, v in sorted(last.items(), key=lambda x: -x[1])[:8]}}


def main():
    creates, msgs = asyncio.run(L.hear(MIN * 60))
    pick = creates[:: max(1, len(creates) // SAMPLE)][:SAMPLE]
    rows = [slot_holders(c) for c in pick]
    good = [r for r in rows if "creator_plus_bundle_share" in r]
    cpb = [r["creator_plus_bundle_share"] for r in good]
    res = {"listened_min": MIN, "creates_heard": len(creates), "sampled": len(rows), "read": len(good),
           "with_same_slot_buyer": sum(1 for r in good if r["bundle_wallets"] > 0),
           "median_creator_share": round(st.median([r["creator_share"] for r in good]), 4) if good else None,
           "median_creator_plus_bundle": round(st.median(cpb), 4) if cpb else None,
           "max_creator_plus_bundle": round(max(cpb), 4) if cpb else None,
           "over_10pct": sum(1 for v in cpb if v >= 0.10),
           "median_bundle_share_where_bundled": round(st.median([r["bundle_share"] for r in good if r["bundle_wallets"]]), 4)
           if any(r["bundle_wallets"] for r in good) else None,
           "rows": rows}
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))


if __name__ == "__main__":
    main()
