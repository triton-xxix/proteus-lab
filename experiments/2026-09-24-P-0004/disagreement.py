#!/usr/bin/env python3
"""P-0004: bookmaker disagreement (MaxH minus AvgH, and D, A) as a feature, E0 first, nine leagues for context.

Re-uses the saved walk-forward probabilities in pitch/backtest/predictions.csv (no refit) and joins the
pre-close Max and Avg prices from football-data. Disagreement per outcome: d_k = Max_k / Avg_k - 1,
known before the close, so a live desk could use it.

Three questions:
1. Does disagreement predict which way the price moves to the close? (corr of d_k with close minus
   pre-close devigged probability)
2. As a feature: p' = softmax(log p + b_k * d_k), three coefficients fitted leave-one-season-out on log
   loss, applied to the held-out season. Base p is the pre-close average price or the desk's DC model.
   Does out-of-sample log loss improve?
3. Pool weight: does the adjusted pre-close price or the adjusted DC earn any log-opinion-pool weight
   against the average closing price (same best_weight as the harness)?
Output: REPORT.md next to this file.
"""
import importlib.util, sys
import numpy as np, pandas as pd
from scipy.optimize import minimize
sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D
spec = importlib.util.spec_from_file_location("bt", "/Users/triton/PROTEUS/pitch/backtest.py")
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)

HERE = "/Users/triton/PROTEUS/experiments/2026-09-24-P-0004/"
pred = pd.read_csv("/Users/triton/PROTEUS/pitch/backtest/predictions.csv", dtype={"season": str}, parse_dates=["date"])
key = ["div", "date", "home", "away"]
wide = pred[pred["model"] == "dc"][key + ["season", "hg", "ag", "AvgH", "AvgD", "AvgA", "AvgCH", "AvgCD", "AvgCA", "ph", "pd", "pa"]]
raw = D.load_results(sorted(pred["div"].unique())).rename(columns={"Div": "div", "Date": "date", "HomeTeam": "home", "AwayTeam": "away"})
MAX = ["MaxH", "MaxD", "MaxA"]
wide = wide.merge(raw[key + [c for c in MAX if c in raw.columns]].drop_duplicates(key), on=key, how="left")
wide = wide.dropna(subset=MAX + ["AvgH", "AvgD", "AvgA", "AvgCH", "AvgCD", "AvgCA"]).reset_index(drop=True)
wide["y"] = np.where(wide["hg"] > wide["ag"], 0, np.where(wide["hg"] == wide["ag"], 1, 2))


def feats(w):
    return w[MAX].to_numpy(float) / w[["AvgH", "AvgD", "AvgA"]].to_numpy(float) - 1


def adjust(P, d, b):
    z = np.log(np.clip(P, 1e-9, 1)) + d * b
    z -= z.max(axis=1, keepdims=True); E = np.exp(z)
    return E / E.sum(axis=1, keepdims=True)


def ll(P, y):
    return float(-np.mean(np.log(np.clip(P[np.arange(len(y)), y], 1e-12, 1))))


def fit_b(P, d, y):
    r = minimize(lambda b: ll(adjust(P, d, b), y), np.zeros(3), method="Nelder-Mead", options={"xatol": 1e-4, "fatol": 1e-7, "maxiter": 4000})
    return r.x


def base(w, which):
    return B.devig(w[["AvgH", "AvgD", "AvgA"]].to_numpy(float)) if which == "pre-close" else w[["ph", "pd", "pa"]].to_numpy(float)


L = ["# P-0004: bookmaker disagreement as a feature", "",
     "Disagreement d_k = Max_k / Avg_k - 1 on the pre-close prices, per outcome. Saved walk-forward DC probabilities",
     "from `pitch/backtest/predictions.csv`, no refit. Coefficients fitted leave-one-season-out on log loss; every",
     "number in the out-of-sample tables is on a season the coefficients never saw. Pool weight is `best_weight`",
     "against the devigged average closing price, as in the harness.", ""]


def section(label, w):
    y = w["y"].to_numpy(); d = feats(w)
    pre = B.devig(w[["AvgH", "AvgD", "AvgA"]].to_numpy(float)); clo = B.devig(w[["AvgCH", "AvgCD", "AvgCA"]].to_numpy(float))
    L.append("## %s (n=%d)" % (label, len(w))); L.append("")
    L.append("Disagreement, median (90th pct): H %.3f (%.3f), D %.3f (%.3f), A %.3f (%.3f)" % tuple(
        v for k in range(3) for v in (np.median(d[:, k]), np.percentile(d[:, k], 90))))
    mv = clo - pre
    L.append("Correlation of d_k with the move to close (close minus pre-close prob): H %+.3f, D %+.3f, A %+.3f" % tuple(
        np.corrcoef(d[:, k], mv[:, k])[0, 1] for k in range(3)))
    L.append(""); L.append("| base | season | log loss base | log loss adjusted | change | b_H, b_D, b_A (fitted elsewhere) | pool wt base v close | pool wt adjusted v close |")
    L.append("|---|---|---|---|---|---|---|---|")
    tot = {}
    for which in ("pre-close", "dc"):
        for s in sorted(w["season"].unique()):
            te = w[w["season"] == s]; tr = w[w["season"] != s]
            if len(te) < 50 or len(tr) < 100: continue
            b = fit_b(base(tr, which), feats(tr), tr["y"].to_numpy())
            P0 = base(te, which); P1 = adjust(P0, feats(te), b); yt = te["y"].to_numpy()
            Pc = B.devig(te[["AvgCH", "AvgCD", "AvgCA"]].to_numpy(float))
            l0, l1 = ll(P0, yt), ll(P1, yt)
            t = tot.setdefault(which, [0, 0.0, 0.0]); t[0] += len(te); t[1] += l0 * len(te); t[2] += l1 * len(te)
            L.append("| %s | %s | %.4f | %.4f | %+.4f | %s | %.2f | %.2f |" % (which, s, l0, l1, l1 - l0, ", ".join("%+.2f" % x for x in b),
                     B.best_weight(P0, Pc, yt), B.best_weight(P1, Pc, yt)))
    L.append("")
    for which, (n, a, c) in tot.items():
        L.append("Out of sample, %s, all seasons pooled (n=%d): log loss %.4f to %.4f, change %+.4f." % (which, n, a / n, c / n, (c - a) / n))
    L.append("Closing price log loss on the same rows: %.4f." % ll(clo, y))
    L.append("")
    return tot


tE0 = section("E0", wide[wide["div"] == "E0"])
tall = section("all nine leagues", wide)
cov = wide.groupby(["div", "season"]).size().unstack(fill_value=0)
L.append("Rows with Max and Avg pre-close prices, by league and season:"); L.append(""); L.append("```"); L.append(cov.to_string()); L.append("```")
open(HERE + "REPORT.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
