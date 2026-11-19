"""P-0490: how much of the trading on a mayhem coin is the agent itself?

For the three busiest of P-0473's 19 mints (by signature count then), page getSignaturesForAddress
on the mint and on the mayhem wallet's token account for that mint, and compare the two sets.

- agent share = signatures on the mint that also touch the agent's token account / all on the mint
- timing: seconds from the mint's first signature to the agent account's first, and to the first
  signature on the mint that does not touch the agent's account

No transaction is decoded: "touches the agent's account" is membership of the token account's
signature list. Failed transactions are counted apart.

    python3 share.py

Keyless, read only, standard library.
"""
import json, statistics, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "2026-11-18-P-0473" / "results.json"
RPC = "https://api.mainnet-beta.solana.com"
WALLET = "BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s"
HALT = Path("/Users/triton/PROTEUS/HALT")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) proteus-inventory/0.1"
TOP = 3
MAX_PAGES = 6


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json", "User-Agent": UA})
    err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read())
            if "result" in out:
                return out
            err = out.get("error")
        except Exception as e:
            err = e
        time.sleep(2 * (attempt + 1))
    return {"error": str(err)[:200]}


def all_sigs(address):
    """every signature on an address, newest first; (list, complete?)"""
    out, before = [], None
    for _ in range(MAX_PAGES):
        opts = {"limit": 1000}
        if before:
            opts["before"] = before
        r = rpc("getSignaturesForAddress", [address, opts])
        if "result" not in r:
            return out, False
        page = r["result"]
        out.extend(page)
        if len(page) < 1000:
            return out, True
        before = page[-1]["signature"]
        time.sleep(0.8)
    return out, False


def main():
    if HALT.exists():
        print("HALT")
        return 1
    old = json.loads(OLD.read_text())["rows"]
    busiest = sorted([r for r in old if "sigs" in r], key=lambda r: -r["sigs"])[:TOP]
    rows = []
    for o in busiest:
        mint = o["mint"]
        row = {"mint": mint, "sigs_on_18_nov": o["sigs"]}
        a = rpc("getTokenAccountsByOwner", [WALLET, {"mint": mint}, {"encoding": "jsonParsed"}])
        accs = a.get("result", {}).get("value", [])
        if not accs:
            row["error"] = "no token account: " + str(a.get("error"))
            rows.append(row)
            print(json.dumps(row), flush=True)
            continue
        acct = accs[0]["pubkey"]
        row["agent_token_account"] = acct
        time.sleep(0.8)
        msigs, mdone = all_sigs(mint)
        time.sleep(0.8)
        asigs, adone = all_sigs(acct)
        time.sleep(0.8)
        aset = {s["signature"] for s in asigs}
        mset = {s["signature"] for s in msigs}
        chron = sorted(msigs, key=lambda s: (s.get("slot", 0)))  # oldest first; ties share a slot
        birth = chron[0]
        first_agent = next((s for s in chron if s["signature"] in aset), None)
        first_other = next((s for s in chron if s["signature"] not in aset), None)
        ok = [s for s in msigs if s.get("err") is None]
        both = [s for s in msigs if s["signature"] in aset]
        both_ok = [s for s in ok if s["signature"] in aset]
        life = [s for s in chron if s.get("blockTime") and s["blockTime"] - birth["blockTime"] <= 3600]
        life_agent = [s for s in life if s["signature"] in aset]
        # outsiders in the first minute and how many came before the agent's first
        before_agent = [s for s in chron if first_agent and s["slot"] < first_agent["slot"]]
        row.update({
            "mint_sigs": len(msigs), "mint_complete": mdone,
            "agent_account_sigs": len(asigs), "agent_complete": adone,
            "agent_sigs_not_on_mint": len(aset - mset),
            "both": len(both),
            "agent_share": round(len(both) / len(msigs), 4) if msigs else None,
            "mint_sigs_ok": len(ok), "mint_sigs_failed": len(msigs) - len(ok),
            "agent_share_of_ok": round(len(both_ok) / len(ok), 4) if ok else None,
            "first_hour_sigs": len(life),
            "agent_share_first_hour": round(len(life_agent) / len(life), 4) if life else None,
            "birth_time": birth.get("blockTime"),
            "birth_touches_agent": birth["signature"] in aset,
            "agent_first_after_birth_s": (first_agent["blockTime"] - birth["blockTime"]) if first_agent else None,
            "agent_first_slots_after_birth": (first_agent["slot"] - birth["slot"]) if first_agent else None,
            "other_first_after_birth_s": (first_other["blockTime"] - birth["blockTime"]) if first_other else None,
            "other_first_slots_after_birth": (first_other["slot"] - birth["slot"]) if first_other else None,
            "sigs_before_agent_first": len(before_agent),
            "last_sig_h_after_birth": round((chron[-1]["blockTime"] - birth["blockTime"]) / 3600, 2),
        })
        rows.append(row)
        print(json.dumps(row), flush=True)

    good = [r for r in rows if "agent_share" in r]
    summary = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "coins": len(rows), "scored": len(good),
        "median_agent_share": statistics.median([r["agent_share"] for r in good]) if good else None,
        "agent_shares": [r["agent_share"] for r in good],
        "agent_first_after_birth_s": [r["agent_first_after_birth_s"] for r in good],
        "birth_touches_agent": [r["birth_touches_agent"] for r in good],
        "sigs_before_agent_first": [r["sigs_before_agent_first"] for r in good],
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
