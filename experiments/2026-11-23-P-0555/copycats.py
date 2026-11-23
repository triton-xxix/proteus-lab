"""P-0555: same ticker on two or more mints in grinder/SNAPSHOTS.csv.

Usage: python3 -I copycats.py SNAPSHOTS.csv OUT_JSON
For each ticker (symbol, case-folded) seen on 2+ distinct mints, order mints by
first sighting. Compare the first mint with the later ones on: chg_h24 at first
sighting, rug_score, liquidity, and whether the mint is seen again on a later
night (a crude survival proxy). Singles (tickers on one mint) are the baseline.
"""
import csv, json, statistics as st, sys
from collections import defaultdict

src, out = sys.argv[1:3]
first = {}; nights = defaultdict(set)
for r in csv.DictReader(open(src, encoding="utf-8")):
    m = r["mint"]; nights[m].add(r["ts"][:10])
    if m not in first:
        first[m] = r
by_sym = defaultdict(list)
for m, r in first.items():
    by_sym[(r["symbol"] or "").strip().casefold()].append(m)

def f(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def stats(mints):
    ch = [f(first[m]["chg_h24"]) for m in mints]; ch = [c for c in ch if c is not None]
    rs = [f(first[m]["rug_score"]) for m in mints]; rs = [c for c in rs if c is not None]
    lq = [f(first[m]["liq_usd"]) for m in mints]; lq = [c for c in lq if c is not None]
    again = [len(nights[m]) > 1 for m in mints]
    return {"n": len(mints), "median_chg_h24": st.median(ch) if ch else None,
            "median_rug_score": st.median(rs) if rs else None,
            "median_liq_usd": st.median(lq) if lq else None,
            "seen_again_pct": round(100 * sum(again) / len(again), 1) if again else None}

multi = {s: sorted(ms, key=lambda m: first[m]["ts"]) for s, ms in by_sym.items() if len(ms) > 1 and s}
singles = [ms[0] for s, ms in by_sym.items() if len(ms) == 1]
firsts = [ms[0] for ms in multi.values()]
laters = [m for ms in multi.values() for m in ms[1:]]
top = sorted(multi.items(), key=lambda kv: -len(kv[1]))[:15]
res = {"mints": len(first), "tickers": len(by_sym), "tickers_on_2plus_mints": len(multi),
       "mints_on_shared_tickers": sum(len(v) for v in multi.values()),
       "singles": stats(singles), "first_of_shared": stats(firsts), "later_of_shared": stats(laters),
       "top": [{"symbol": s, "mints": len(ms), "names": sorted({first[m]["name"] for m in ms})[:5]} for s, ms in top]}
json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)
for k in ("mints", "tickers", "tickers_on_2plus_mints", "mints_on_shared_tickers"):
    print(k, res[k])
for k in ("singles", "first_of_shared", "later_of_shared"):
    print(k, res[k])
for t in res["top"]:
    print(" ", t["symbol"], t["mints"], t["names"])
