"""P-0189: SPY as a three-state Markov chain (QuantEcon, Finite Markov Chains lecture).
States per day: down (close-to-close below -0.5%), flat, up (above +0.5%).
1. Estimate the transition matrix P from counts.
2. Its stationary distribution (left eigenvector for eigenvalue 1) against the observed state shares:
   the lecture's ergodicity result says they should agree.
3. Does yesterday matter? Statistic: the count-weighted total variation between each row of P and the
   marginal shares. Control: the same statistic on 2,000 shuffles of the daily returns, which keep the
   shares and destroy any order.
4. The same split into 2006-2015 and 2016-2026, to see whether one regime does it all.
Bars from Yahoo's chart API, keyless, the same endpoint systems/systems.py uses."""
import json, urllib.request, datetime
import numpy as np

OUT = "/Users/triton/PROTEUS/experiments/2026-10-20-P-0189/"
url = "https://query1.finance.yahoo.com/v8/finance/chart/SPY?period1=1136073600&period2=1792540800&interval=1d"
d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60))
r = d["chart"]["result"][0]
ts = r["timestamp"]
close = r["indicators"]["adjclose"][0]["adjclose"]
pairs = [(t, c) for t, c in zip(ts, close) if c is not None]
dates = [datetime.datetime.utcfromtimestamp(t).date() for t, _ in pairs]
px = np.array([c for _, c in pairs])
ret = px[1:] / px[:-1] - 1
dates = dates[1:]
TH = 0.005
NAMES = ["down", "flat", "up"]


def states(x):
    return np.where(x < -TH, 0, np.where(x > TH, 2, 1))


def fit(s):
    C = np.zeros((3, 3))
    np.add.at(C, (s[:-1], s[1:]), 1)
    P = C / C.sum(axis=1, keepdims=True)
    return C, P


def stat(s):
    C, P = fit(s)
    marg = np.bincount(s[1:], minlength=3) / (len(s) - 1)
    w = C.sum(axis=1) / C.sum()
    return float((w * 0.5 * np.abs(P - marg).sum(axis=1)).sum())


def stationary(P):
    vals, vecs = np.linalg.eig(P.T)
    v = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
    return v / v.sum()


rng = np.random.default_rng(20261020)
lines = [f"SPY daily, {dates[0]} to {dates[-1]}, {len(ret)} returns, threshold +-{TH:.1%}"]


def report(label, x):
    s = states(x)
    C, P = fit(s)
    pi = stationary(P)
    obs = np.bincount(s, minlength=3) / len(s)
    real = stat(s)
    null = np.array([stat(states(rng.permutation(x))) for _ in range(2000)])
    p = (1 + (null >= real).sum()) / (1 + len(null))
    lines.append(f"\n{label}: n {len(x)}")
    lines.append("P (rows: yesterday; columns: today down, flat, up)")
    for i in range(3):
        lines.append(f"  {NAMES[i]:5} " + "  ".join(f"{P[i, j]:.3f}" for j in range(3)) + f"   (n {int(C[i].sum())})")
    lines.append("stationary " + "  ".join(f"{q:.3f}" for q in pi) + " | observed " + "  ".join(f"{q:.3f}" for q in obs))
    lines.append(f"dependence stat {real:.4f}; shuffled mean {null.mean():.4f}, 99th pct {np.percentile(null, 99):.4f}; p {p:.4f}")
    return P, p


report("2006-2026", ret)
split = next(i for i, dt in enumerate(dates) if dt.year >= 2016)
report("2006-2015", ret[:split])
report("2016-2026", ret[split:])
txt = "\n".join(lines)
print(txt)
open(OUT + "result.txt", "w").write(txt + "\n")
