"""P-0046: xG from scratch on StatsBomb open data.

Distance-and-angle logistic regression against a constant baseline and StatsBomb's own xG,
out of sample, split by match. Keyless: raw.githubusercontent.com/statsbomb/open-data.
"""
import json
import math
import os
import random
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
CACHE = "/Users/triton/PROTEUS/sandbox/statsbomb"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-01-P-0046"
COMPS = [(43, 106, "World Cup 2022"), (55, 282, "Euro 2024")]


def get(path):
    local = os.path.join(CACHE, path.replace("/", "_"))
    if os.path.exists(local):
        with open(local) as f:
            return json.load(f)
    with urllib.request.urlopen(f"{BASE}/{path}", timeout=60) as r:
        body = r.read()
    with open(local, "wb") as f:
        f.write(body)
    return json.loads(body)


def shots_for(match_id):
    rows = []
    for e in get(f"events/{match_id}.json"):
        if e.get("type", {}).get("name") != "Shot":
            continue
        s = e["shot"]
        if s.get("type", {}).get("name") == "Penalty":
            continue
        x, y = e["location"][0], e["location"][1]
        dx, dy = 120 - x, 40 - y
        dist = math.hypot(dx, dy)
        a1 = math.atan2(44 - y, dx)
        a2 = math.atan2(36 - y, dx)
        angle = abs(a1 - a2)
        rows.append({
            "match": match_id,
            "dist": dist,
            "angle": angle,
            "head": 1.0 if s.get("body_part", {}).get("name") == "Head" else 0.0,
            "goal": 1.0 if s.get("outcome", {}).get("name") == "Goal" else 0.0,
            "sb": s.get("statsbomb_xg"),
        })
    return rows


def fit_logit(X, y, iters=5000, lr=0.1):
    mu, sd = X.mean(0), X.std(0)
    Z = (X - mu) / sd
    Z = np.hstack([np.ones((len(Z), 1)), Z])
    w = np.zeros(Z.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Z @ w))
        w -= lr * Z.T @ (p - y) / len(y)
    return lambda Xn: 1 / (1 + np.exp(-np.hstack([np.ones((len(Xn), 1)), (Xn - mu) / sd]) @ w))


def scores(p, y):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    ll = float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
    br = float(np.mean((p - y) ** 2))
    return round(ll, 4), round(br, 4)


def main():
    os.makedirs(CACHE, exist_ok=True)
    match_ids = []
    for comp, season, name in COMPS:
        ms = get(f"matches/{comp}/{season}.json")
        match_ids += [m["match_id"] for m in ms]
        print(name, len(ms), "matches")
    with ThreadPoolExecutor(8) as ex:
        per = list(ex.map(shots_for, match_ids))
    rows = [r for rs in per for r in rs]
    random.seed(46)
    test_matches = set(random.sample(match_ids, len(match_ids) // 3))
    tr = [r for r in rows if r["match"] not in test_matches]
    te = [r for r in rows if r["match"] in test_matches]
    ytr = np.array([r["goal"] for r in tr])
    yte = np.array([r["goal"] for r in te])

    result = {"matches": len(match_ids), "shots_train": len(tr), "shots_test": len(te),
              "goal_rate_train": round(float(ytr.mean()), 4), "test": {}}
    result["test"]["constant"] = scores(np.full(len(te), ytr.mean()), yte)
    for name, cols in [("dist_angle", ["dist", "angle"]), ("dist_angle_head", ["dist", "angle", "head"])]:
        f = fit_logit(np.array([[r[c] for c in cols] for r in tr]), ytr)
        result["test"][name] = scores(f(np.array([[r[c] for c in cols] for r in te])), yte)
    sb = np.array([r["sb"] for r in te], dtype=float)
    result["test"]["statsbomb_xg"] = scores(sb, yte)
    result["test_goals"] = int(yte.sum())
    result["note"] = "scores are (log loss, Brier), lower is better; penalties excluded; split by match, seed 46"
    with open(os.path.join(OUT, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
