"""P-0220: distance-and-angle logistic xG on StatsBomb open data (World Cup 2022, 64 matches).

Train on the first 44 matches by date, test on the last 20. Compare test log loss with the base rate
(training goal share for every shot) and with StatsBomb's own shot xG on the same shots.
Non-penalty open-play and set-piece shots; penalties dropped.
"""
import json, math, os, time, urllib.request
import numpy as np

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/"
CACHE = "/Users/triton/PROTEUS/sandbox/p0220-statsbomb/"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-25-P-0220/results.json"
os.makedirs(CACHE, exist_ok=True)


def get(path):
    local = CACHE + path.replace("/", "_")
    if os.path.exists(local):
        return json.load(open(local))
    with urllib.request.urlopen(BASE + path, timeout=60) as r:
        raw = r.read()
    open(local, "wb").write(raw)
    return json.loads(raw)


matches = sorted(get("matches/43/106.json"), key=lambda m: (m["match_date"], m["kick_off"] or ""))
shots = []  # (match_index, distance, angle, goal, sb_xg)
for i, m in enumerate(matches):
    for e in get("events/%d.json" % m["match_id"]):
        if e["type"]["name"] != "Shot" or e["shot"]["type"]["name"] == "Penalty":
            continue
        x, y = e["location"][0], e["location"][1]
        dx, dy = 120 - x, abs(40 - y)
        dist = math.hypot(dx, dy)
        # angle subtended by the goal mouth (posts at y 36 and 44)
        a = math.atan2(8 * dx, dx * dx + dy * dy - 16)
        if a < 0:
            a += math.pi
        shots.append((i, dist, a, 1 if e["shot"]["outcome"]["name"] == "Goal" else 0, e["shot"].get("statsbomb_xg")))

S = np.array([s[:4] for s in shots], dtype=float)
sb = np.array([s[4] for s in shots], dtype=float)
train, test = S[:, 0] < 44, S[:, 0] >= 44


def feats(M):
    return np.column_stack([np.ones(len(M)), M[:, 1], M[:, 2]])


X, y = feats(S), S[:, 3]
mu, sd = X[train, 1:].mean(0), X[train, 1:].std(0)
Xn = X.copy()
Xn[:, 1:] = (X[:, 1:] - mu) / sd
w = np.zeros(3)
for _ in range(5000):  # plain gradient descent, convex, converges well inside this
    p = 1 / (1 + np.exp(-Xn[train] @ w))
    w -= 0.5 * Xn[train].T @ (p - y[train]) / train.sum()


def ll(p, t):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return float(-np.mean(t * np.log(p) + (1 - t) * np.log(1 - p)))


p_model = 1 / (1 + np.exp(-Xn[test] @ w))
base = y[train].mean()
res = {
    "competition": "FIFA World Cup 2022 (StatsBomb 43/106)",
    "shots_total": int(len(S)), "train_shots": int(train.sum()), "test_shots": int(test.sum()),
    "test_goals": int(y[test].sum()), "train_goal_rate": round(float(base), 4),
    "logloss_base": round(ll(np.full(test.sum(), base), y[test]), 4),
    "logloss_model": round(ll(p_model, y[test]), 4),
    "logloss_statsbomb_xg": round(ll(sb[test], y[test]), 4),
    "test_xg_sum_model": round(float(p_model.sum()), 1), "test_xg_sum_statsbomb": round(float(sb[test].sum()), 1),
    "weights_standardised": [round(float(v), 3) for v in w],
}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
