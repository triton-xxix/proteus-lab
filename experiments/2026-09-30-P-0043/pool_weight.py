#!/usr/bin/env python3
"""P-0043: the log-opinion-pool test of arXiv 2608.11505 on the Pitch desk's walk-forward backtest.

p(w) proportional to market^(1-w) * model^w, renormalised. Market = Shin de-vigged average closing odds
(AvgC*), with the opening average as a second benchmark. Weight fitted on the earlier season(s),
profile traced on [0,1] and [-1,1] for fit and test, per model, all leagues pooled and per group.
Input: pitch/backtest/predictions.csv (committed 24 Sep). Output: REPORT.md, profile.json."""
import json, math, collections
import pandas as pd
import numpy as np

OUT = "/Users/triton/PROTEUS/experiments/2026-09-30-P-0043/"
df = pd.read_csv("/Users/triton/PROTEUS/pitch/backtest/predictions.csv")


def shin(odds):
    pi = 1.0 / np.asarray(odds, float)
    B = pi.sum()
    if not np.isfinite(B) or B <= 1:
        return pi / B
    def probs(z):
        return (np.sqrt(z * z + 4 * (1 - z) * pi * pi / B) - z) / (2 * (1 - z))
    lo, hi = 0.0, 0.4
    for _ in range(60):
        mid = (lo + hi) / 2
        if probs(mid).sum() > 1:
            lo = mid
        else:
            hi = mid
    p = probs((lo + hi) / 2)
    return p / p.sum()


def market(cols):
    m = df[cols].to_numpy(float)
    ok = np.isfinite(m).all(axis=1) & (m > 1).all(axis=1)
    out = np.full(m.shape, np.nan)
    for i in np.where(ok)[0]:
        out[i] = shin(m[i])
    return out

df[["mcH", "mcD", "mcA"]] = market(["AvgCH", "AvgCD", "AvgCA"])
df[["moH", "moD", "moA"]] = market(["AvgH", "AvgD", "AvgA"])
df["y"] = np.select([df.hg > df.ag, df.hg == df.ag], [0, 1], 2)


def pool(M, S, w):
    lp = (1 - w) * np.log(M) + w * np.log(np.clip(S, 1e-9, 1))
    lp -= lp.max(axis=1, keepdims=True)
    p = np.exp(lp)
    return p / p.sum(axis=1, keepdims=True)


def logloss(P, y):
    return float(-np.log(np.clip(P[np.arange(len(y)), y], 1e-12, 1)).mean())


def rps(P, y):
    Y = np.zeros_like(P); Y[np.arange(len(y)), y] = 1
    c = np.cumsum(P - Y, axis=1)[:, :2]
    return float((c ** 2).sum(axis=1).mean() / 2)


GRID01 = np.round(np.linspace(0, 1, 21), 3)
GRIDNEG = np.round(np.linspace(-1, 1, 81), 3)
seasons = sorted(df.season.unique())
test_season = seasons[-1]
fit_seasons = seasons[:-1]
L = ["# P-0043: log-pool weight on the Pitch backtest (arXiv 2608.11505 method)", "",
     "Input `pitch/backtest/predictions.csv` (walk-forward, committed 24 Sep). Seasons %s; weight fitted on %s, "
     "tested on %s. Market is Shin de-vigged average closing odds unless stated." % (seasons, fit_seasons, test_season), ""]
res = {}
for mkt_name, mc in (("close", ["mcH", "mcD", "mcA"]), ("open", ["moH", "moD", "moA"])):
    for model in sorted(df.model.unique()):
        d = df[(df.model == model)].dropna(subset=mc + ["ph", "pd", "pa"])
        fit, test = d[d.season.isin(fit_seasons)], d[d.season == test_season]
        rows = {}
        for name, part in (("fit", fit), ("test", test)):
            M, S, y = part[mc].to_numpy(), part[["ph", "pd", "pa"]].to_numpy(), part.y.to_numpy()
            prof01 = [logloss(pool(M, S, w), y) for w in GRID01]
            profneg = [logloss(pool(M, S, w), y) for w in GRIDNEG]
            rows[name] = {"n": len(part), "prof01": prof01, "profneg": profneg,
                          "rps_market": rps(M, y), "rps_model": rps(S, y),
                          "ll_market": logloss(M, y), "ll_model": logloss(S, y),
                          "monotone01": all(b >= a - 1e-12 for a, b in zip(prof01, prof01[1:]))}
        w_hat = float(GRID01[int(np.argmin(rows["fit"]["prof01"]))])
        w_neg = float(GRIDNEG[int(np.argmin(rows["fit"]["profneg"]))])
        Mt, St, yt = test[mc].to_numpy(), test[["ph", "pd", "pa"]].to_numpy(), test.y.to_numpy()
        gain = logloss(Mt, yt) - logloss(pool(Mt, St, w_hat), yt)
        res["%s/%s" % (mkt_name, model)] = {"w_hat": w_hat, "w_hat_unconstrained": w_neg, "test_ll_gain_at_w_hat": gain,
                                            "fit": {k: v for k, v in rows["fit"].items() if k != "profneg"},
                                            "test": {k: v for k, v in rows["test"].items() if k != "profneg"}}

L += ["| market | model | n fit | n test | w fitted [0,1] | w unconstrained | monotone fit | monotone test | RPS mkt test | RPS model test | test log-loss gain at w |",
      "|---|---|---|---|---|---|---|---|---|---|---|"]
for k, r in res.items():
    mk, mo = k.split("/")
    L.append("| %s | %s | %d | %d | %.2f | %.3f | %s | %s | %.4f | %.4f | %+.5f |" % (
        mk, mo, r["fit"]["n"], r["test"]["n"], r["w_hat"], r["w_hat_unconstrained"], r["fit"]["monotone01"],
        r["test"]["monotone01"], r["test"]["rps_market"], r["test"]["rps_model"], r["test_ll_gain_at_w_hat"]))

# per group, closing market, each model
L += ["", "Per league group, closing market, weight fitted on the fit seasons:", "",
      "| group | model | n fit | w fitted | RPS mkt test | RPS model test |", "|---|---|---|---|---|---|"]
for g in sorted(df.group.unique()):
    for model in sorted(df.model.unique()):
        d = df[(df.group == g) & (df.model == model)].dropna(subset=["mcH", "mcD", "mcA", "ph", "pd", "pa"])
        fit, test = d[d.season.isin(fit_seasons)], d[d.season == test_season]
        if len(fit) < 50 or len(test) < 50:
            continue
        pr = [logloss(pool(fit[["mcH", "mcD", "mcA"]].to_numpy(), fit[["ph", "pd", "pa"]].to_numpy(), w), fit.y.to_numpy()) for w in GRID01]
        L.append("| %s | %s | %d | %.2f | %.4f | %.4f |" % (g, model, len(fit), GRID01[int(np.argmin(pr))],
                 rps(test[["mcH", "mcD", "mcA"]].to_numpy(), test.y.to_numpy()), rps(test[["ph", "pd", "pa"]].to_numpy(), test.y.to_numpy())))

json.dump({"grid01": GRID01.tolist(), "results": res}, open(OUT + "profile.json", "w"), indent=1)
open(OUT + "REPORT.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
