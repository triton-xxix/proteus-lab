"""P-0290: does a bot's acceptance of my challenges track the rating gap, its games played or its
last-seen time? Reads games/lichess/CHALLENGES.csv, pulls each bot's public profile keyless
(lichess.org/api/user/<name>, 1.2 s apart, cached in sandbox/lichess-users/), and compares bots
that ever accepted with bots that never did. Rank-sum style permutation tests, stdlib only.
Writes results.json beside this script. Run with python3 -I."""
import csv
import json
import random
import statistics as st
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = Path("/Users/triton/PROTEUS/sandbox/lichess-users")
CACHE.mkdir(parents=True, exist_ok=True)
rows = list(csv.DictReader(open("/Users/triton/PROTEUS/games/lichess/CHALLENGES.csv")))

bots = {}
for r in rows:
    b = bots.setdefault(r["opponent"].lower(), {"asked": 0, "accepted": 0, "declined": 0, "refused": 0, "noanswer": 0, "gaps": []})
    b["asked"] += 1
    v = r["verdict"]
    if v == "accepted":
        b["accepted"] += 1
    elif v == "declined":
        b["declined"] += 1
    elif v.startswith("refused"):
        b["refused"] += 1
    else:
        b["noanswer"] += 1
    try:
        b["gaps"].append(int(r["my_rating"]) - int(r["opp_rating"]))
    except ValueError:
        pass

now_ms = time.time() * 1000
for name, b in bots.items():
    f = CACHE / f"{name}.json"
    if not f.exists():
        try:
            req = urllib.request.Request(f"https://lichess.org/api/user/{name}", headers={"User-Agent": "Mozilla/5.0 proteus-p0290"})
            f.write_bytes(urllib.request.urlopen(req, timeout=20).read())
        except Exception as e:  # noqa: BLE001
            b["profile_error"] = str(e)[:60]
            continue
        time.sleep(1.2)
    p = json.loads(f.read_text())
    if p.get("disabled") or p.get("tosViolation"):
        b["closed"] = True
    perfs = p.get("perfs", {})
    b["games_all"] = (p.get("count") or {}).get("all")
    b["blitz"] = (perfs.get("blitz") or {}).get("rating")
    b["seen_days"] = round((now_ms - p["seenAt"]) / 86400000, 1) if p.get("seenAt") else None

# a bot is an acceptor if it ever accepted; compare acceptors with bots that only declined or refused
acc = [b for b in bots.values() if b["accepted"]]
never = [b for b in bots.values() if not b["accepted"] and (b["declined"] or b["refused"])]


def perm(xs, ys, n=5000, seed=1):
    """two-sided permutation p for a difference in medians"""
    xs, ys = [x for x in xs if x is not None], [y for y in ys if y is not None]
    if len(xs) < 3 or len(ys) < 3:
        return None, len(xs), len(ys)
    d0 = abs(st.median(xs) - st.median(ys))
    pool, k, rng, hits = xs + ys, len(xs), random.Random(seed), 0
    for _ in range(n):
        rng.shuffle(pool)
        hits += abs(st.median(pool[:k]) - st.median(pool[k:])) >= d0
    return round(hits / n, 4), len(xs), len(ys)


out = {"bots": len(bots), "challenges": len(rows), "acceptors": len(acc), "never_accepted": len(never),
       "profile_errors": sum(1 for b in bots.values() if "profile_error" in b),
       "closed_accounts": sum(1 for b in bots.values() if b.get("closed"))}
for key, fn in {"gap_median": lambda b: st.median(b["gaps"]) if b["gaps"] else None,
                "games_all": lambda b: b.get("games_all"),
                "blitz": lambda b: b.get("blitz"),
                "seen_days": lambda b: b.get("seen_days")}.items():
    a = [fn(b) for b in acc]
    z = [fn(b) for b in never]
    p, na, nz = perm(a, z)
    out[key] = {"acceptors_median": st.median([x for x in a if x is not None]) if na else None,
                "never_median": st.median([x for x in z if x is not None]) if nz else None,
                "n": [na, nz], "perm_p": p}
# accept share by gap band, over bots
bands = [(-10_000, 300), (300, 600), (600, 900), (900, 10_000)]
out["by_gap_band"] = []
for lo, hi in bands:
    inb = [b for b in acc + never if b["gaps"] and lo <= st.median(b["gaps"]) < hi]
    out["by_gap_band"].append({"gap": f"{lo}..{hi}", "bots": len(inb), "acceptors": sum(1 for b in inb if b["accepted"])})
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
