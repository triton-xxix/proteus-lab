#!/usr/bin/env python3
"""P-0003: does swapping the average closing price for Pinnacle's closing price move any model's pool weight?

Re-uses the saved walk-forward probabilities in pitch/backtest/predictions.csv (no refit), joins them
to the football-data rows that carry PSCH/PSCD/PSCA and MaxCH/MaxCD/MaxCA, and computes, per season
and league: Brier of each line, and each model's in-sample log-opinion-pool weight against the
average close, the Pinnacle close and the max close. Same devig, metrics and best_weight as
pitch/backtest.py. Diagnostic only. Output: REPORT.md next to this file.
"""
import importlib.util, sys
import numpy as np, pandas as pd
sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D
spec = importlib.util.spec_from_file_location("bt", "/Users/triton/PROTEUS/pitch/backtest.py")
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)

LINES = {"avg close": ["AvgCH", "AvgCD", "AvgCA"], "pinnacle close": ["PSCH", "PSCD", "PSCA"], "max close": ["MaxCH", "MaxCD", "MaxCA"]}
pred = pd.read_csv("/Users/triton/PROTEUS/pitch/backtest/predictions.csv", dtype={"season": str}, parse_dates=["date"])
divs = sorted(pred["div"].unique())
raw = D.load_results(divs)
raw = raw.rename(columns={"Div": "div", "Date": "date", "HomeTeam": "home", "AwayTeam": "away"})
cols = [c for l in LINES.values() for c in l]
raw = raw[["div", "date", "home", "away"] + [c for c in cols if c in raw.columns]]
key = ["div", "date", "home", "away"]
wide = pred[key + ["season", "hg", "ag"]].drop_duplicates(key)
for m in sorted(pred["model"].unique()):
    s = pred[pred["model"] == m].set_index(key)[["ph", "pd", "pa"]]; s.columns = [m + "_h", m + "_d", m + "_a"]
    wide = wide.join(s, on=key)
wide = wide.merge(raw, on=key, how="left")
models = sorted(pred["model"].unique())
wide["y"] = np.where(wide["hg"] > wide["ag"], 0, np.where(wide["hg"] == wide["ag"], 1, 2))
L = ["# P-0003: Pinnacle closing as the line to beat", "",
     "Saved walk-forward probabilities from `pitch/backtest/predictions.csv`, no refit. Pool weight is the in-sample",
     "log-opinion-pool weight the model earns against the named line (same `best_weight` as the harness).", ""]
def block(label, w):
    w = w.dropna(subset=cols + [m + "_h" for m in models])
    if len(w) < 50:
        L.append("## %s: %d matches with all three closing lines, too few" % (label, len(w))); L.append(""); return
    L.append("## %s (n=%d with all three closing lines)" % (label, len(w))); L.append("")
    L.append("| line | Brier | RPS | log loss |"); L.append("|---|---|---|---|")
    y = w["y"].to_numpy(); P = {}
    for name, c in LINES.items():
        P[name] = B.devig(w[c].to_numpy(float)); b, r, ll = B.metrics(P[name], y)
        L.append("| %s | %.4f | %.4f | %.4f |" % (name, b, r, ll))
    for m in models:
        Pm = w[[m + "_h", m + "_d", m + "_a"]].to_numpy(float); b, r, ll = B.metrics(Pm, y)
        L.append("| model %s | %.4f | %.4f | %.4f |" % (m, b, r, ll))
    L.append(""); L.append("| model | wt vs avg close | wt vs pinnacle close | wt vs max close |"); L.append("|---|---|---|---|")
    for m in models:
        Pm = w[[m + "_h", m + "_d", m + "_a"]].to_numpy(float)
        L.append("| %s | %.2f | %.2f | %.2f |" % (m, B.best_weight(Pm, P["avg close"], y), B.best_weight(Pm, P["pinnacle close"], y), B.best_weight(Pm, P["max close"], y)))
    L.append("")
cov = wide.groupby(["div", "season"]).apply(lambda g: pd.Series({"matches": len(g), "with_PSC": int(g["PSCH"].notna().sum())})).reset_index()
L.append("Coverage of Pinnacle closing columns by league and season:"); L.append("")
L.append("| div | season | matches | with PSCH |"); L.append("|---|---|---|---|")
for _, r in cov.iterrows(): L.append("| %s | %s | %d | %d |" % (r["div"], r["season"], r["matches"], r["with_PSC"]))
L.append("")
for season in sorted(wide["season"].unique()):
    block("E0 season " + season, wide[(wide["div"] == "E0") & (wide["season"] == season)])
block("E0 all seasons", wide[wide["div"] == "E0"])
block("all nine leagues, all seasons", wide)
open("/Users/triton/PROTEUS/experiments/2026-09-24-P-0003/REPORT.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
