"""P-0172: read live pump.fun bonding-curve accounts from public Solana RPC and check
(1) constant product: virtual_sol * virtual_token against the launch k of 30 SOL x 1,073,000,000 tokens,
(2) where a completed curve stops: real SOL reserves at completion.
Keyless. PDA derived in pure Python (no solders on this Mac). Mints from DexScreener's public
token-profile and boost feeds plus the Grinder ledger's pump mints."""
import base64, csv, hashlib, json, struct, sys, time, urllib.request

RPC = "https://api.mainnet-beta.solana.com"
PUMP = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
OUT = "/Users/triton/PROTEUS/state/agents/inspector-2026-10-18/curve-results.json"
LEDGER = "/Users/triton/PROTEUS/grinder/LEDGER.csv"
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58d(s):
    n = 0
    for c in s:
        n = n * 58 + B58.index(c)
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + b

def b58e(b):
    n = int.from_bytes(b, "big"); s = ""
    while n:
        n, r = divmod(n, 58); s = B58[r] + s
    pad = len(b) - len(b.lstrip(b"\x00"))
    return "1" * pad + s

# ed25519 on-curve check (point decompression)
P = 2**255 - 19
D = (-121665 * pow(121666, P - 2, P)) % P
def on_curve(b):
    y = int.from_bytes(b, "little") & ((1 << 255) - 1)
    if y >= P:
        return False
    u = (y * y - 1) % P; v = (D * y * y + 1) % P
    x2 = u * pow(v, P - 2, P) % P
    if x2 == 0:
        return True
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P == 0:
        return True
    x = x * pow(2, (P - 1) // 4, P) % P
    return (x * x - x2) % P == 0

def pda(seeds, prog):
    pb = b58d(prog)
    for bump in range(255, -1, -1):
        h = hashlib.sha256(b"".join(seeds) + bytes([bump]) + pb + b"ProgramDerivedAddress").digest()
        if not on_curve(h):
            return b58e(h)
    raise ValueError("no pda")

def get(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json", "User-Agent": "proteus-probe"})
    return json.load(urllib.request.urlopen(req, timeout=25))

def mints():
    out = []
    for u in ["https://api.dexscreener.com/token-profiles/latest/v1",
              "https://api.dexscreener.com/token-boosts/latest/v1"]:
        try:
            for r in get(u):
                a = r.get("tokenAddress", "")
                if r.get("chainId") == "solana" and a.endswith("pump"):
                    out.append(("dexscreener", a))
        except Exception as e:
            print("feed fail", u, e)
    with open(LEDGER) as f:
        for r in csv.reader(f):
            for c in r:
                if c.endswith("pump") and len(c) > 40:
                    out.append(("ledger", c))
    seen, uniq = set(), []
    for s, a in out:
        if a not in seen:
            seen.add(a); uniq.append((s, a))
    return uniq

K0 = 30 * 10**9 * 1_073_000_000 * 10**6  # lamports x raw token units (6 decimals)

def main():
    ms = mints()
    print("mints", len(ms))
    rows = []
    batch = [(s, m, pda([b"bonding-curve", b58d(m)], PUMP)) for s, m in ms[:100]]
    for i in range(0, len(batch), 50):
        chunk = batch[i:i + 50]
        r = get(RPC, {"jsonrpc": "2.0", "id": 1, "method": "getMultipleAccounts",
                      "params": [[c[2] for c in chunk], {"encoding": "base64"}]})
        for (src, m, curve), acc in zip(chunk, r["result"]["value"]):
            if not acc or acc["owner"] != PUMP:
                rows.append({"mint": m, "src": src, "curve": curve, "found": False}); continue
            d = base64.b64decode(acc["data"][0])
            vt, vs, rt, rs, sup = struct.unpack_from("<5Q", d, 8)
            complete = bool(d[48])
            rows.append({"mint": m, "src": src, "curve": curve, "found": True, "len": len(d),
                         "virtual_token": vt, "virtual_sol": vs, "real_token": rt, "real_sol": rs,
                         "supply": sup, "complete": complete,
                         "k_ratio": (vt * vs) / K0 if vt and vs else None,
                         "lamports": acc["lamports"]})
        time.sleep(1)
    found = [r for r in rows if r["found"]]
    live = [r for r in found if not r["complete"]]
    done = [r for r in found if r["complete"]]
    live_k = sorted(r["k_ratio"] for r in live if r["k_ratio"])
    done_vals = [(r["virtual_sol"] / 1e9, r["real_sol"] / 1e9, r["real_token"], r["virtual_token"] / 1e6) for r in done]
    summ = {"mints_tried": len(batch), "curves_found": len(found), "live": len(live), "complete": len(done),
            "live_k_ratio_min": live_k[0] if live_k else None, "live_k_ratio_max": live_k[-1] if live_k else None,
            "live_within_1pct": sum(1 for k in live_k if abs(k - 1) <= 0.01),
            "complete_sample": done_vals[:15]}
    # implied real SOL at completion from launch k: tokens left on curve when real_token hits 0
    vt_end = 1_073_000_000 - 793_100_000
    summ["implied_completion_virtual_sol"] = 30 * 1_073_000_000 / vt_end
    summ["implied_completion_real_sol"] = summ["implied_completion_virtual_sol"] - 30
    print(json.dumps(summ, indent=1))
    json.dump({"summary": summ, "rows": rows}, open(OUT, "w"), indent=1)

main()
