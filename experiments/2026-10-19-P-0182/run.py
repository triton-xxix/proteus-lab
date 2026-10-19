"""P-0182: fast.ai lesson 5, from scratch in numpy. Linear model and a one-hidden-layer net, hand-written
gradients, against the one-line rule "women survive, men do not", on held-out Titanic rows.

Features as in Jeremy Howard's "Linear model and neural net from scratch" notebook: Sex, Age (mode-filled),
SibSp, Parch, log(Fare+1), Pclass and Embarked dummies, each divided by its column max, plus a constant.
Twenty random 80/20 splits so one lucky split cannot carry the answer.
"""
import json
import numpy as np
import pandas as pd

HERE = "/Users/triton/PROTEUS/experiments/2026-10-19-P-0182"
df = pd.read_csv(HERE + "/titanic.csv")
for c in ["Age", "Embarked", "Fare"]:
    df[c] = df[c].fillna(df[c].mode()[0])
df["LogFare"] = np.log1p(df["Fare"])
X = pd.DataFrame({
    "male": (df["Sex"] == "male").astype(float),
    "Age": df["Age"], "SibSp": df["SibSp"], "Parch": df["Parch"], "LogFare": df["LogFare"],
    "P1": (df["Pclass"] == 1).astype(float), "P2": (df["Pclass"] == 2).astype(float),
    "EC": (df["Embarked"] == "C").astype(float), "EQ": (df["Embarked"] == "Q").astype(float),
})
X = X / X.max()
X["const"] = 1.0
X = X.values
y = df["Survived"].values.astype(float)


def sig(z):
    return 1 / (1 + np.exp(-z))


def train_linear(Xt, yt, rng, lr=0.5, epochs=400):
    w = (rng.random(Xt.shape[1]) - 0.5) * 0.1
    for _ in range(epochs):
        p = sig(Xt @ w)
        w -= lr * Xt.T @ (p - yt) / len(yt)
    return lambda Xv: sig(Xv @ w)


def train_net(Xt, yt, rng, hidden=20, lr=0.5, epochs=1500):
    W1 = (rng.random((Xt.shape[1], hidden)) - 0.5) * 0.5
    w2 = (rng.random(hidden) - 0.5) * 0.5
    b2 = 0.0
    n = len(yt)
    for _ in range(epochs):
        h_pre = Xt @ W1
        h = np.maximum(h_pre, 0)
        p = sig(h @ w2 + b2)
        g = (p - yt) / n                      # dLoss/dlogit for log loss
        gw2 = h.T @ g
        gb2 = g.sum()
        gh = np.outer(g, w2) * (h_pre > 0)
        gW1 = Xt.T @ gh
        W1 -= lr * gW1
        w2 -= lr * gw2
        b2 -= lr * gb2
    return lambda Xv: sig(np.maximum(Xv @ W1, 0) @ w2 + b2)


rows = []
for seed in range(20):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y))
    cut = int(0.8 * len(y))
    tr, va = idx[:cut], idx[cut:]
    rule = (X[va, 0] == 0).astype(float)          # female -> survives
    lin = train_linear(X[tr], y[tr], rng)(X[va])
    net = train_net(X[tr], y[tr], rng)(X[va])
    acc = lambda p: float(((p > 0.5) == (y[va] == 1)).mean())
    rows.append({"seed": seed, "rule": acc(rule), "linear": acc(lin), "net": acc(net)})

r = pd.DataFrame(rows)
summary = {
    "splits": len(r),
    "mean_accuracy": {k: round(float(r[k].mean()), 4) for k in ["rule", "linear", "net"]},
    "sd": {k: round(float(r[k].std()), 4) for k in ["rule", "linear", "net"]},
    "linear_beats_rule_splits": int((r["linear"] > r["rule"]).sum()),
    "net_beats_rule_splits": int((r["net"] > r["rule"]).sum()),
    "net_beats_linear_splits": int((r["net"] > r["linear"]).sum()),
    "mean_gain_over_rule_pts": {
        "linear": round(float((r["linear"] - r["rule"]).mean() * 100), 2),
        "net": round(float((r["net"] - r["rule"]).mean() * 100), 2),
    },
}
json.dump({"summary": summary, "rows": rows}, open(HERE + "/results.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
