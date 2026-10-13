#!/usr/bin/env python3
"""P-0144: a two-feature xG model (distance, angle) on StatsBomb open data, held-out AUC.

Keyless: raw.githubusercontent.com/statsbomb/open-data/master/data/matches/<comp>/<season>.json
then events/<match_id>.json. Shots only (type.name == "Shot", penalties excluded), goal = outcome Goal.
Features: distance to goal centre (yards, pitch 120x80, goal at x=120 y=40), angle subtended by the
goal mouth (radians, posts at y 36 and 44). Logistic regression with 5-fold CV by match (numpy,
Newton steps), AUC by rank statistic. Also reports AUC of StatsBomb's own xG for the same shots.
Usage: xg.py OUTDIR [--comp 43 --season 106 --matches 50]
"""
import json
import math
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/"
UA = {"User-Agent": "proteus-nightly/1.0"}


def get(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def features(x, y):
    dx = 120.0 - x
    dy = 40.0 - y
    dist = math.hypot(dx, dy)
    # angle subtended by the goal mouth at the shot location (law of cosines form)
    a = math.atan2(7.32 * 1.09361 * dx, dx * dx + dy * dy - (7.32 * 1.09361 / 2) ** 2)  # 8 yards wide
    if a < 0:
        a += math.pi
    return dist, a


def fit_logistic(X, y, iters=25, l2=1e-4):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Xb @ w))
        g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w


def predict(w, X):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    return 1 / (1 + np.exp(-Xb @ w))


def auc(scores, y):
    order = np.argsort(scores)
    ranks = np.empty(len(scores))
    # average ranks for ties
    s = scores[order]
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    npos = y.sum()
    nneg = len(y) - npos
    return (ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    args = sys.argv[2:]
    comp = int(args[args.index("--comp") + 1]) if "--comp" in args else 43
    season = int(args[args.index("--season") + 1]) if "--season" in args else 106
    nmatch = int(args[args.index("--matches") + 1]) if "--matches" in args else 50
    t0 = time.time()
    matches = get("matches/%d/%d.json" % (comp, season))
    matches = sorted(matches, key=lambda m: m["match_id"])[:nmatch]
    rows = []
    failed = 0
    for m in matches:
        try:
            ev = get("events/%d.json" % m["match_id"])
        except Exception as e:  # noqa: BLE001
            failed += 1
            print("match %s failed: %s" % (m["match_id"], e))
            continue
        for e in ev:
            if e.get("type", {}).get("name") != "Shot":
                continue
            sh = e.get("shot", {})
            if sh.get("type", {}).get("name") == "Penalty":
                continue
            loc = e.get("location")
            if not loc:
                continue
            d, a = features(loc[0], loc[1])
            rows.append({"match": m["match_id"], "dist": d, "angle": a,
                         "goal": 1 if sh.get("outcome", {}).get("name") == "Goal" else 0,
                         "sb_xg": sh.get("statsbomb_xg"),
                         "body": sh.get("body_part", {}).get("name"),
                         "header": 1 if sh.get("body_part", {}).get("name") == "Head" else 0})
        time.sleep(0.3)
    print("matches %d (failed %d), shots %d, goals %d, %.0fs" % (
        len(matches) - failed, failed, len(rows), sum(r["goal"] for r in rows), time.time() - t0))
    X = np.array([[r["dist"], r["angle"]] for r in rows])
    y = np.array([r["goal"] for r in rows], dtype=float)
    mids = sorted({r["match"] for r in rows})
    folds = {mid: i % 5 for i, mid in enumerate(mids)}
    f = np.array([folds[r["match"]] for r in rows])
    oof = np.zeros(len(rows))
    for k in range(5):
        tr, te = f != k, f == k
        w = fit_logistic(X[tr], y[tr])
        oof[te] = predict(w, X[te])
    auc_model = auc(oof, y)
    # add header flag as a third feature, same folds
    X3 = np.hstack([X, np.array([[r["header"]] for r in rows])])
    oof3 = np.zeros(len(rows))
    for k in range(5):
        tr, te = f != k, f == k
        w = fit_logistic(X3[tr], y[tr])
        oof3[te] = predict(w, X3[te])
    auc_3 = auc(oof3, y)
    sb = np.array([r["sb_xg"] if r["sb_xg"] is not None else 0 for r in rows])
    auc_sb = auc(sb, y)
    w_all = fit_logistic(X, y)
    res = {"competition": comp, "season": season, "matches": len(matches) - failed, "shots": len(rows),
           "goals": int(y.sum()), "auc_distance_angle_cv5": round(float(auc_model), 4),
           "auc_plus_header_cv5": round(float(auc_3), 4), "auc_statsbomb_xg": round(float(auc_sb), 4),
           "coef_full_fit": {"intercept": round(float(w_all[0]), 4), "dist": round(float(w_all[1]), 4),
                             "angle": round(float(w_all[2]), 4)},
           "seconds": round(time.time() - t0, 1)}
    json.dump(res, open(out / "results.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
