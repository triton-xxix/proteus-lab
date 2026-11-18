"""P-0476: who tops up the mayhem fee payer, and is the trading wallet really in its transactions?

Two legs, keyless on the public RPC, read only:

1. link: getTransaction on --fetch of the payer's newest signatures; is the trading wallet in the
   static keys or in meta.loadedAddresses (address lookup tables), and which programs are called.
2. top-ups: the payer's balance every --every seconds for --samples samples; any rise is an inbound
   transfer. Also how far back --pages pages of 1,000 signatures reach, to size a full search.

    python3 topups.py --fetch 20 --samples 14 --every 25 --pages 3
"""
import argparse, json, sys, time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-18-P-0475"))
from feepayer import rpc, PAYER, WALLET, HALT  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", type=int, default=20)
    ap.add_argument("--samples", type=int, default=14)
    ap.add_argument("--every", type=int, default=25)
    ap.add_argument("--pages", type=int, default=3)
    a = ap.parse_args()
    if HALT.exists():
        print("HALT")
        return 1
    out = {"at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "payer": PAYER}

    # paging reach
    before, newest, oldest, total = None, None, None, 0
    first_page = []
    for p in range(a.pages):
        params = {"limit": 1000}
        if before:
            params["before"] = before
        s = rpc("getSignaturesForAddress", [PAYER, params])
        if "result" not in s or not s["result"]:
            out["page_error"] = s.get("error", "empty")
            break
        page = s["result"]
        if p == 0:
            first_page = page
            newest = page[0]["blockTime"]
        oldest = page[-1]["blockTime"]
        before = page[-1]["signature"]
        total += len(page)
        time.sleep(0.5)
    if newest and oldest:
        out["pages"] = a.pages
        out["signatures_paged"] = total
        out["reach_s"] = newest - oldest
        out["pages_for_24h"] = round(86400 / max(1, (newest - oldest) / a.pages))
    print(json.dumps(out), flush=True)

    # link
    rows, programs = [], Counter()
    step = max(1, len(first_page) // a.fetch)
    for x in first_page[::step][: a.fetch]:
        r = rpc("getTransaction", [x["signature"], {"encoding": "json", "maxSupportedTransactionVersion": 0}])
        tx = r.get("result")
        if not tx:
            continue
        msg, meta = tx["transaction"]["message"], tx["meta"]
        keys = msg["accountKeys"]
        la = meta.get("loadedAddresses") or {}
        loaded_w, loaded_r = la.get("writable") or [], la.get("readonly") or []
        allkeys = keys + loaded_w + loaded_r
        for ix in msg.get("instructions", []):
            programs[allkeys[ix["programIdIndex"]]] += 1
        rows.append({
            "sig": x["signature"][:16],
            "version": tx.get("version"),
            "static_keys": len(keys),
            "loaded": len(loaded_w) + len(loaded_r),
            "wallet_static": WALLET in keys,
            "wallet_loaded_writable": WALLET in loaded_w,
            "wallet_loaded_readonly": WALLET in loaded_r,
            "lookup_tables": [t["accountKey"] for t in msg.get("addressTableLookups", [])],
        })
        time.sleep(0.35)
    out["fetched"] = len(rows)
    out["wallet_static"] = sum(1 for r in rows if r["wallet_static"])
    out["wallet_loaded"] = sum(1 for r in rows if r["wallet_loaded_writable"] or r["wallet_loaded_readonly"])
    out["wallet_anywhere"] = sum(1 for r in rows if r["wallet_static"] or r["wallet_loaded_writable"] or r["wallet_loaded_readonly"])
    out["lookup_tables"] = sorted({t for r in rows for t in r["lookup_tables"]})
    out["programs"] = dict(programs.most_common(8))
    print(json.dumps({k: out[k] for k in ("fetched", "wallet_static", "wallet_loaded", "wallet_anywhere", "lookup_tables", "programs")}), flush=True)

    # balance watch
    samples = []
    for i in range(a.samples):
        b = rpc("getBalance", [PAYER])
        if "result" in b:
            samples.append({"t": round(time.time(), 1), "sol": b["result"]["value"] / 1e9})
        if i < a.samples - 1:
            time.sleep(a.every)
    steps = [round(samples[i + 1]["sol"] - samples[i]["sol"], 6) for i in range(len(samples) - 1)]
    out["balance_samples"] = len(samples)
    out["watch_s"] = round(samples[-1]["t"] - samples[0]["t"], 1) if len(samples) > 1 else 0
    out["rises"] = sum(1 for d in steps if d > 0)
    out["largest_rise_sol"] = max(steps) if steps else None
    out["balance_first"] = samples[0]["sol"] if samples else None
    out["balance_last"] = samples[-1]["sol"] if samples else None
    if len(samples) > 1 and out["watch_s"]:
        out["sol_per_day"] = round((samples[-1]["sol"] - samples[0]["sol"]) / out["watch_s"] * 86400, 1)
    (HERE / "results.json").write_text(json.dumps({"summary": out, "rows": rows, "samples": samples}, indent=1))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
