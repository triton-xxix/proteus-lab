"""Ran-it, 16 Nov 2026: does solders decode live pump.fun transactions from the public RPC?

Pulls the latest signatures on the pump.fun program from api.mainnet-beta.solana.com (keyless),
fetches each transaction as base64, decodes it with solders (installed to sandbox/solders-lib),
finds the pump.fun instructions, names them by Anchor discriminator, and for create instructions
reads name, symbol and uri from the borsh args. Writes results.json beside this file.
"""
import base64
import hashlib
import json
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/solders-lib")
from solders.transaction import VersionedTransaction  # noqa: E402
from solders.pubkey import Pubkey  # noqa: E402

RPC = "https://api.mainnet-beta.solana.com"
PUMP = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")
N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 40
OUT = Path(__file__).with_name("results-idl.json" if "--idl" in sys.argv else "results.json")

NAMES = ["create", "create_v2", "buy", "sell", "buy_exact_sol_in", "withdraw", "initialize",
         "set_params", "extend_account", "migrate", "collect_creator_fee", "claim_token_incentives",
         "sync_user_volume_accumulator", "close_user_volume_accumulator", "init_user_volume_accumulator"]
DISC = {hashlib.sha256(f"global:{n}".encode()).digest()[:8]: n for n in NAMES}
IDL = Path(__file__).with_name("pump-idl.json")
USE_IDL = "--idl" in sys.argv
if USE_IDL:  # second pass: names from the public IDL (pump-fun/pump-public-docs)
    DISC = {bytes(i["discriminator"]): i["name"] for i in json.loads(IDL.read_text())["instructions"]}
MAX_FETCH = 60
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58decode(s):
    n = 0
    for ch in s:
        n = n * 58 + B58.index(ch)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\0" * (len(s) - len(s.lstrip("1"))) + raw


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json",
                                                          "User-Agent": "proteus-ranit/0.1"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())
        except Exception as e:  # 429s on the public RPC
            time.sleep(1.5 * (attempt + 1))
            err = e
    return {"error": str(err)}


def borsh_str(buf, i):
    n = int.from_bytes(buf[i:i + 4], "little")
    return buf[i + 4:i + 4 + n].decode("utf-8", "replace"), i + 4 + n


def main():
    sigs = rpc("getSignaturesForAddress", [str(PUMP), {"limit": N}]).get("result", [])
    stats = Counter()
    kinds = Counter()
    creates = []
    unknown = Counter()
    t0 = time.time()
    for s in sigs:
        if s.get("err"):
            stats["failed_on_chain"] += 1
            continue
        res = rpc("getTransaction", [s["signature"], {"encoding": "base64",
                                                      "maxSupportedTransactionVersion": 0}])
        tx = (res or {}).get("result")
        time.sleep(0.25)
        if not tx:
            stats["fetch_failed"] += 1
            continue
        stats["fetched"] += 1
        try:
            vt = VersionedTransaction.from_bytes(base64.b64decode(tx["transaction"][0]))
        except Exception:
            stats["decode_failed"] += 1
            continue
        stats["decoded"] += 1
        msg = vt.message
        keys = list(msg.account_keys)
        loaded = tx.get("meta", {}).get("loadedAddresses") or {}
        keys += [Pubkey.from_string(k) for k in loaded.get("writable", []) + loaded.get("readonly", [])]
        hit = False
        ixs = [(keys[ix.program_id_index], bytes(ix.data), list(ix.accounts), "top") for ix in msg.instructions]
        for grp in (tx.get("meta") or {}).get("innerInstructions") or []:
            for ii in grp["instructions"]:
                ixs.append((keys[ii["programIdIndex"]], b58decode(ii["data"]), ii["accounts"], "inner"))
        for prog, data, accts, where in ixs:
            if prog != PUMP:
                continue
            hit = True
            stats[f"pump_ix_{where}"] += 1
            if len(data) < 8:
                continue
            name = DISC.get(data[:8])
            if name is None:
                unknown[data[:8].hex()] += 1
                kinds["unknown"] += 1
                continue
            kinds[name] += 1
            if name.startswith("create"):
                try:
                    nm, i = borsh_str(data, 8)
                    sym, i = borsh_str(data, i)
                    uri, i = borsh_str(data, i)
                    mint = str(keys[accts[0]])
                    creates.append({"sig": s["signature"][:16], "name": nm, "symbol": sym,
                                    "uri": uri[:80], "mint": mint})
                except Exception as e:
                    creates.append({"sig": s["signature"][:16], "parse_error": str(e)})
        if not hit:
            stats["no_pump_ix_found"] += 1
        if stats["fetched"] >= MAX_FETCH:
            break
    out = {"rpc": RPC, "signatures": len(sigs), "secs": round(time.time() - t0, 1),
           "stats": stats, "instruction_kinds": kinds, "unknown_discriminators": unknown,
           "creates": creates}
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps({k: v for k, v in out.items() if k != "creates"}))
    print("creates parsed:", len([c for c in creates if "name" in c]), "of", len(creates))
    for c in creates[:5]:
        print("  ", c)


if __name__ == "__main__":
    main()
