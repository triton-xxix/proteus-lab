"""P-0471: sample the fee-free mayhem wallet's balances instead of chasing its 15 trades a second.

Each sample is three keyless RPC calls on the public endpoint: getBalance, and
getTokenAccountsByOwner once for the classic token program and once for Token-2022 (jsonParsed).
Appends one line to samples.jsonl: time, SOL balance, token accounts held, accounts with a non-zero
balance, and the summed UI token amount (not priced: coins differ, the sum is only a size signal).

    python3 sampler.py --samples 6 --every 240      # a 20 minute test
    python3 sampler.py --samples 288 --every 300    # the 24 hour job

Read only. Standard library. Stops itself after --samples, and at once if the HALT file exists.
"""
import argparse, json, os, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RPC = "https://api.mainnet-beta.solana.com"
WALLET = "BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s"
PROGRAMS = {"token": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "token2022": "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"}
HALT = Path("/Users/triton/PROTEUS/HALT")
SOL_ONLY = False


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json", "User-Agent": "proteus-sampler/0.1"})
    err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except Exception as e:
            err = e
            time.sleep(2 * (attempt + 1))
    return {"error": str(err)}


def sample():
    row = {"at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "t": int(time.time())}
    b = rpc("getBalance", [WALLET])
    row["sol"] = (b.get("result") or {}).get("value", 0) / 1e9 if "result" in b else None
    row["slot"] = ((b.get("result") or {}).get("context") or {}).get("slot")
    if "error" in b:
        row["sol_error"] = str(b["error"])[:160]
    for name, prog in ({} if SOL_ONLY else PROGRAMS).items():
        r = rpc("getTokenAccountsByOwner", [WALLET, {"programId": prog}, {"encoding": "jsonParsed"}])
        if "result" not in r:
            row[name + "_error"] = str(r.get("error"))[:160]
            continue
        accs = r["result"]["value"]
        amounts = [((a["account"]["data"]["parsed"]["info"].get("tokenAmount") or {}).get("uiAmount") or 0) for a in accs]
        row[name + "_accounts"] = len(accs)
        row[name + "_nonzero"] = sum(1 for x in amounts if x > 0)
        row[name + "_ui_sum_m"] = round(sum(amounts) / 1e6, 3)
        time.sleep(0.5)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=6)
    ap.add_argument("--every", type=int, default=240)
    ap.add_argument("--out", default=str(HERE / "samples.jsonl"))
    ap.add_argument("--sol-only", action="store_true",
                    help="skip the token listings: the Token-2022 one answers 413 for this wallet (17 Nov 2026)")
    a = ap.parse_args()
    global SOL_ONLY
    SOL_ONLY = a.sol_only
    for i in range(a.samples):
        if HALT.exists():
            print("HALT, stopping")
            return 1
        row = sample()
        with open(a.out, "a") as f:
            f.write(json.dumps(row) + "\n")
        print(json.dumps(row), flush=True)
        if i < a.samples - 1:
            time.sleep(a.every)
    return 0


if __name__ == "__main__":
    sys.exit(main())
