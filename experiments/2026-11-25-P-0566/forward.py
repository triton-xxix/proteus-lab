"""P-0566: copycat tickers a week or more on.

P-0555 (23 Nov) found later mints of a shared ticker looked worse at first sighting (rug_score 31 v 1,
liquidity 2,836 v 13,169 USD). This reads them forward: 20 later mints of shared tickers, first seen 7 to
45 days ago, each paired with a single-ticker mint first seen on the same UTC date (seeded pick), and asks
today's liquidity (DexScreener tokens API, keyless, max liquidity over the mint's pairs; no pairs = 0) and
rugcheck's keyless summary score. Read-only GETs, paced.
Called shot: under 100 USD liquidity now for about 60% of later mints against about 35% of singles.
"""
import csv, datetime, json, random, statistics, time, urllib.request, urllib.error
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS")
HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "proteus-probe/1", "Accept": "application/json"}
csv.field_size_limit(10**7)

first = {}
for r in csv.DictReader(open(ROOT / "grinder/SNAPSHOTS.csv")):
    m = r["mint"]
    if m and m not in first:
        first[m] = r
by_sym = defaultdict(list)
for m, r in first.items():
    s = (r["symbol"] or "").strip().casefold()
    if s:
        by_sym[s].append(m)
now = datetime.datetime.now(datetime.timezone.utc)
def age_days(m):
    return (now - datetime.datetime.fromisoformat(first[m]["ts"].replace("Z", "+00:00"))).days
laters, singles_by_day = [], defaultdict(list)
for s, ms in by_sym.items():
    ms = sorted(ms, key=lambda m: first[m]["ts"])
    if len(ms) > 1:
        laters += [(m, s) for m in ms[1:] if 7 <= age_days(m) <= 45]
    else:
        m = ms[0]
        if 7 <= age_days(m) <= 45:
            singles_by_day[first[m]["ts"][:10]].append(m)
rng = random.Random(566)
rng.shuffle(laters)
pairs = []
for m, s in laters:
    day = first[m]["ts"][:10]
    pool = [x for x in singles_by_day.get(day, []) if x not in [p[1] for p in pairs]]
    if pool:
        pairs.append((m, rng.choice(pool), s))
    if len(pairs) == 20:
        break


def get(url):
    try:
        return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25))
    except urllib.error.HTTPError as e:
        return {"_http": e.code}
    except Exception as e:
        return {"_err": type(e).__name__}


mints = [p[0] for p in pairs] + [p[1] for p in pairs]
liq = {m: 0.0 for m in mints}
for i in range(0, len(mints), 30):
    res = get("https://api.dexscreener.com/tokens/v1/solana/" + ",".join(mints[i:i + 30]))
    if isinstance(res, list):
        for p in res:
            a = (p.get("baseToken") or {}).get("address")
            if a in liq:
                liq[a] = max(liq[a], float((p.get("liquidity") or {}).get("usd") or 0))
    else:
        print("dexscreener batch error", res)
    time.sleep(1.2)
rug = {}
for m in mints:
    r = get("https://api.rugcheck.xyz/v1/tokens/%s/report/summary" % m)
    rug[m] = r.get("score_normalised", r.get("score")) if isinstance(r, dict) and "_http" not in r and "_err" not in r else r
    time.sleep(1.0)

rows = []
for later, single, sym in pairs:
    rows.append({"symbol": sym, "first_seen": first[later]["ts"],
                 "later": {"mint": later, "liq_then": first[later]["liq_usd"], "liq_now": liq[later], "rug_now": rug[later]},
                 "single": {"mint": single, "symbol": first[single]["symbol"], "liq_then": first[single]["liq_usd"],
                            "liq_now": liq[single], "rug_now": rug[single]}})


def summ(side):
    now_l = [r[side]["liq_now"] for r in rows]
    rugs = [r[side]["rug_now"] for r in rows if isinstance(r[side]["rug_now"], (int, float))]
    return {"n": len(now_l), "under_100_now": sum(x < 100 for x in now_l), "zero_pairs_or_0": sum(x == 0 for x in now_l),
            "median_liq_now": round(statistics.median(now_l), 2) if now_l else None,
            "median_rug_now": statistics.median(rugs) if rugs else None, "rug_answered": len(rugs)}


both_dead = sum(r["later"]["liq_now"] < 100 and r["single"]["liq_now"] < 100 for r in rows)
later_only = sum(r["later"]["liq_now"] < 100 <= r["single"]["liq_now"] for r in rows)
single_only = sum(r["single"]["liq_now"] < 100 <= r["later"]["liq_now"] for r in rows)
out = {"pool": {"later_mints_7_to_45d": len(laters), "days_with_singles": len(singles_by_day)}, "pairs": len(pairs),
       "later": summ("later"), "single": summ("single"),
       "paired_under_100": {"both": both_dead, "later_only": later_only, "single_only": single_only}, "rows": rows}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
