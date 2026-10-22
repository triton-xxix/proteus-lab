"""P-0197: how many graduation-watcher rows carry a quote token as the mint? Reads mint, timing, latency
and liquidity only; never P or any exit field, so D-013's blind read stays blind.
Usage: python3 mints.py
"""
import collections
import json

QUOTES = {"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
          "So11111111111111111111111111111111111111112": "wSOL",
          "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT"}
G2_FROM, W2_FROM, W2_TO = 1791028800, 1791995640, 1792600440
BLIND = {"P", "A", "B", "D", "exit", "exit_t", "exit_reason", "pnl", "fill"}

rows = [json.loads(l) for l in open("/Users/triton/PROTEUS/grinder/graduates/closed.jsonl")]
keys = collections.Counter(k for r in rows for k in r)


def window(r):
    if r["block_t"] < G2_FROM:
        return "before G2"
    if r["block_t"] < W2_FROM:
        return "G2 window one"
    return "G2 window two" if r["entry_t"] < W2_TO else "after window two"


def counted(r):
    return r.get("latency_s") is not None and r["latency_s"] <= 120 and (r.get("liq") or 0) >= 50000


tab = collections.defaultdict(lambda: collections.Counter())
for r in rows:
    w = window(r)
    q = QUOTES.get(r.get("mint"))
    tab[w]["rows"] += 1
    tab[w]["counted_g2"] += counted(r)
    if q:
        tab[w][q] += 1
        tab[w][q + " counted"] += counted(r)
repeats = collections.Counter(r.get("mint") for r in rows if counted(r) and r["block_t"] >= G2_FROM)
out = {"fields_seen": sorted(k for k in keys if k not in BLIND),
       "by_window": {w: dict(c) for w, c in tab.items()},
       "g2_counted_mints_seen_more_than_once": [[m, n, QUOTES.get(m, "")] for m, n in repeats.most_common(8) if n > 1]}
json.dump(out, open("/Users/triton/PROTEUS/experiments/2026-10-22-P-0197/result.json", "w"), indent=1)
print(json.dumps(out, indent=1))
