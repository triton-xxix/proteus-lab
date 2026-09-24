#!/usr/bin/env python3
"""The Pitch: score any model against the closing line over the history the desk holds.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/pitch/backtest.py --run [--models dc,elo,sot] [--seasons 2425,2526,2627] [--groups ENG,ESP,...]
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/pitch/backtest.py --report

--run walks forward week by week through each test season: every model is refitted on all matches
strictly before the week (all seasons in the cache, back to 2022-23) and predicts that week's
matches. One row per match per model goes to pitch/backtest/predictions.csv with the pre-close and
closing average odds beside it. Fitting groups are countries (data.GROUPS); each runs in its own
process. --report scores what is on disk:

  Brier, RPS and log loss for every model and for the market's pre-close and closing prices with the
  overround removed proportionally; the log-opinion-pool weight the model earns against the closing
  price (fitted in sample, so it flatters the model; a weight of 0.00 is still a clean negative) and
  the same weight fitted on the other test season and applied out of sample; a replay of the desk's
  paper rule (back the 1X2 side where model minus pre-close market exceeds 3 points, quarter Kelly,
  cap 10) at pre-close average odds, settled on results and scored on closing-line value; and the
  same for a blend of the three models with the market, weights fitted on the other season.

Nothing here is a live prediction. The live desk still commits from predict.py. Written 2026-09-24.
"""
import argparse
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D  # noqa: E402
import models as Z  # noqa: E402

ROOT = "/Users/triton/PROTEUS/"
OUT = ROOT + "pitch/backtest/"
PRED = OUT + "predictions.csv"
REPORT = OUT + "REPORT.md"
SUMMARY = OUT + "summary.json"
EDGE, KELLY, CAP, BANK = 0.03, 0.25, 10.0, 100.0
ODDS = ["AvgH", "AvgD", "AvgA", "AvgCH", "AvgCD", "AvgCA"]


def season_of(d):
    return "%02d%02d" % (d.year % 100 if d.month >= 8 else (d.year - 1) % 100, (d.year + 1) % 100 if d.month >= 8 else d.year % 100)


def run_group(args):
    group, divs, seasons, model_names = args
    res = D.load_results(divs)
    if res.empty:
        return []
    res["season"] = res["Date"].map(season_of)
    res["week"] = res["Date"].dt.to_period("W-SUN").dt.start_time
    test = res[res["season"].isin(seasons)]
    out = []
    models = {n: Z.ZOO[n]() for n in model_names}
    for wk, g in test.groupby("week"):
        as_of = wk - pd.Timedelta(days=1)
        for n, m in models.items():
            try:
                m.fit(res, as_of)
            except Exception as e:
                print(group, wk.date(), n, "fit failed", e, file=sys.stderr); continue
        for _, r in g.iterrows():
            base = {"group": group, "div": r["Div"], "season": r["season"], "date": r["Date"].date().isoformat(),
                    "week": wk.date().isoformat(), "home": r["HomeTeam"], "away": r["AwayTeam"],
                    "hg": int(r["FTHG"]), "ag": int(r["FTAG"])}
            for c in ODDS:
                base[c] = r.get(c, np.nan)
            for n, m in models.items():
                p = m.predict(r["HomeTeam"], r["AwayTeam"])
                if p is None:
                    continue
                out.append({**base, "model": n, "ph": round(p[0], 4), "pd": round(p[1], 4), "pa": round(p[2], 4)})
        print(group, wk.date(), "matches", len(g), "rows", len(out), file=sys.stderr, flush=True)
    return out


def run(models, seasons, groups):
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, D.GROUPS[g], seasons, models) for g in groups]
    with Pool(min(len(jobs), max(1, os.cpu_count() - 2))) as pool:
        parts = pool.map(run_group, jobs)
    rows = [r for p in parts for r in p]
    df = pd.DataFrame(rows)
    if os.path.exists(PRED):
        old = pd.read_csv(PRED)
        old = old[~(old["model"].isin(models) & old["season"].isin(seasons) & old["group"].isin(groups))]
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(PRED, index=False)
    print("wrote", len(rows), "rows to", PRED)


# ---------------------------------------------------------------- scoring

def devig(o):
    inv = 1 / o
    return inv / inv.sum(axis=1, keepdims=True)


def metrics(P, y):
    Y = np.eye(3)[y]
    brier = np.mean(np.sum((P - Y) ** 2, axis=1))
    cP, cY = np.cumsum(P, axis=1)[:, :2], np.cumsum(Y, axis=1)[:, :2]
    rps = np.mean(np.sum((cP - cY) ** 2, axis=1) / 2)
    ll = -np.mean(np.log(np.clip(P[np.arange(len(y)), y], 1e-9, None)))
    return brier, rps, ll


def pool_probs(Ps, ws):
    L = sum(w * np.log(np.clip(P, 1e-9, None)) for P, w in zip(Ps, ws))
    E = np.exp(L - L.max(axis=1, keepdims=True))
    return E / E.sum(axis=1, keepdims=True)


def best_weight(Pm, Pk, y):
    ws = np.linspace(0, 1, 101)
    lls = [metrics(pool_probs([Pm, Pk], [w, 1 - w]), y)[2] for w in ws]
    return float(ws[int(np.argmin(lls))])


def best_blend(Ps, Pk, y):
    """Weights on each model against the market, coordinate descent on log loss, market gets the rest."""
    from scipy.optimize import minimize
    k = len(Ps)

    def ll(v):
        w = np.clip(v, 0, 1)
        if w.sum() > 1:
            w = w / w.sum()
        return metrics(pool_probs(Ps + [Pk], list(w) + [1 - w.sum()]), y)[2]
    res = minimize(ll, np.full(k, 0.1), method="Nelder-Mead", options={"xatol": 1e-3, "fatol": 1e-6})
    w = np.clip(res.x, 0, 1)
    if w.sum() > 1:
        w = w / w.sum()
    return [float(x) for x in w]


def paper(P, y, pre_odds, close_odds):
    """Desk rule at pre-close odds: edge over 3 points, quarter Kelly, cap 10, bank 100, in date order."""
    Ppre = devig(pre_odds)
    bank, staked, pnl, clvs, n, wins = BANK, 0.0, 0.0, [], 0, 0
    for i in range(len(y)):
        edge = P[i] - Ppre[i]; j = int(np.argmax(edge))
        if edge[j] <= EDGE:
            continue
        o = float(pre_odds[i, j]); p = float(P[i, j])
        f = max(0.0, (p * (o - 1) - (1 - p)) / (o - 1)) * KELLY
        st = round(min(bank * f, CAP), 2)
        if st < 0.5:
            continue
        ret = st * (o - 1) if y[i] == j else -st
        bank += ret; staked += st; pnl += ret; n += 1; wins += int(y[i] == j)
        clvs.append(o / float(close_odds[i, j]) - 1)
    if not n:
        return {"bets": 0}
    return {"bets": n, "staked": round(staked, 2), "pnl": round(pnl, 2), "roi_pct": round(100 * pnl / staked, 1),
            "hit_pct": round(100 * wins / n, 1), "clv_pct": round(100 * float(np.mean(clvs)), 2),
            "beat_close_pct": round(100 * float(np.mean(np.array(clvs) > 0)), 1), "end_bank": round(bank, 2)}


def calib(P, y, bins=10):
    """Reliability of the model's home-win probability: predicted vs observed by decile."""
    p = P[:, 0]; o = (y == 0).astype(float)
    edges = np.quantile(p, np.linspace(0, 1, bins + 1))
    out = []
    for i in range(bins):
        m = (p >= edges[i]) & (p <= edges[i + 1] if i == bins - 1 else p < edges[i + 1])
        if m.sum():
            out.append({"n": int(m.sum()), "pred": round(float(p[m].mean()), 3), "obs": round(float(o[m].mean()), 3)})
    return out


def report():
    df = pd.read_csv(PRED, dtype={"season": str}).dropna(subset=ODDS)
    df = df.sort_values(["date", "div", "home"])
    df["y"] = np.where(df["hg"] > df["ag"], 0, np.where(df["hg"] == df["ag"], 1, 2))
    models = sorted(df["model"].unique())
    seasons = sorted(df["season"].unique())
    # wide: one row per match, columns per model
    key = ["div", "season", "date", "home", "away"]
    wide = df[key + ["y"] + ODDS].drop_duplicates(key).set_index(key)
    for m in models:
        sub = df[df["model"] == m].set_index(key)[["ph", "pd", "pa"]]
        sub.columns = [m + "_h", m + "_d", m + "_a"]
        wide = wide.join(sub, how="left")
    wide = wide.dropna().reset_index()
    summary = {"n_matches": int(len(wide)), "models": models, "seasons": seasons, "slices": {}}

    def P_of(w, m):
        return w[[m + "_h", m + "_d", m + "_a"]].to_numpy(float)

    def evaluate(w, label, wfit=None):
        y = w["y"].to_numpy(); pre = w[["AvgH", "AvgD", "AvgA"]].to_numpy(float); clo = w[["AvgCH", "AvgCD", "AvgCA"]].to_numpy(float)
        Ppre, Pclo = devig(pre), devig(clo)
        s = {"n": int(len(w)), "lines": {}, "paper": {}, "pool_in_sample": {}, "pool_out_of_sample": {}, "calib": {}}
        for name, P in (("pre-close", Ppre), ("closing", Pclo)):
            b, r, l = metrics(P, y); s["lines"][name] = {"brier": round(b, 4), "rps": round(r, 4), "logloss": round(l, 4)}
        for m in models:
            Pm = P_of(w, m); b, r, l = metrics(Pm, y)
            s["lines"][m] = {"brier": round(b, 4), "rps": round(r, 4), "logloss": round(l, 4)}
            s["pool_in_sample"][m] = best_weight(Pm, Pclo, y)
            s["paper"][m] = paper(Pm, y, pre, clo)
            s["calib"][m] = calib(Pm, y)
            if wfit is not None and len(wfit) > 50:
                wgt = best_weight(P_of(wfit, m), devig(wfit[["AvgCH", "AvgCD", "AvgCA"]].to_numpy(float)), wfit["y"].to_numpy())
                Pb = pool_probs([Pm, Pclo], [wgt, 1 - wgt]); b, r, l = metrics(Pb, y)
                s["pool_out_of_sample"][m] = {"weight": wgt, "brier": round(b, 4), "logloss": round(l, 4)}
        # blend of all models with the pre-close market: weights from the other season, applied here
        if wfit is not None and len(wfit) > 50:
            Ps_fit = [P_of(wfit, m) for m in models]; Pk_fit = devig(wfit[["AvgH", "AvgD", "AvgA"]].to_numpy(float))
            ws = best_blend(Ps_fit, Pk_fit, wfit["y"].to_numpy())
            Pb = pool_probs([P_of(w, m) for m in models] + [Ppre], ws + [1 - sum(ws)])
            b, r, l = metrics(Pb, y)
            s["lines"]["blend(pre-close)"] = {"brier": round(b, 4), "rps": round(r, 4), "logloss": round(l, 4)}
            s["blend_weights"] = dict(zip(models, [round(x, 3) for x in ws]))
            s["paper"]["blend(pre-close)"] = paper(Pb, y, pre, clo)
            s["pool_in_sample"]["blend(pre-close)"] = best_weight(Pb, Pclo, y)
        summary["slices"][label] = s
        return s

    for season in seasons:
        w = wide[wide["season"] == season]; other = wide[wide["season"] != season]
        evaluate(w, "season " + season, other)
        for div in sorted(w["div"].unique()):
            evaluate(w[w["div"] == div], "season %s %s" % (season, div), other[other["div"] == div])
    evaluate(wide, "all seasons")
    for div in sorted(wide["div"].unique()):
        evaluate(wide[wide["div"] == div], "all seasons " + div)
    json.dump(summary, open(SUMMARY, "w"), indent=1)
    write_report(summary)
    print("report ->", REPORT)


def write_report(s):
    L = ["# Pitch backtest report", "", "Generated by `pitch/backtest.py --report`. %d scored matches, models: %s, seasons: %s."
         % (s["n_matches"], ", ".join(s["models"]), ", ".join(s["seasons"])),
         "Market lines are average odds from football-data with the overround removed proportionally. Paper rule: back",
         "the side where model minus pre-close market exceeds 3 points, quarter Kelly, cap 10, bank 100, at pre-close odds.",
         "CLV is the pre-close price taken over the closing price, so positive means the market moved our way.", ""]
    for label, sl in s["slices"].items():
        L += ["## %s (n=%d)" % (label, sl["n"]), "", "| line | Brier | RPS | log loss | pool wt vs close (in-sample) | out-of-sample pooled log loss |", "|---|---|---|---|---|---|"]
        for name, m in sorted(sl["lines"].items(), key=lambda kv: kv[1]["rps"]):
            w_in = sl["pool_in_sample"].get(name); oos = sl["pool_out_of_sample"].get(name)
            L.append("| %s | %.4f | %.4f | %.4f | %s | %s |" % (name, m["brier"], m["rps"], m["logloss"],
                     "" if w_in is None else "%.2f" % w_in, "" if not oos else "%.4f (wt %.2f)" % (oos["logloss"], oos["weight"])))
        L += ["", "| paper rule | bets | staked | pnl | ROI | hit | mean CLV | beat close | end bank |", "|---|---|---|---|---|---|---|---|---|"]
        for name, p in sl["paper"].items():
            if p.get("bets"):
                L.append("| %s | %d | %.2f | %+.2f | %+.1f%% | %.1f%% | %+.2f%% | %.1f%% | %.2f |" % (name, p["bets"], p["staked"], p["pnl"], p["roi_pct"], p["hit_pct"], p["clv_pct"], p["beat_close_pct"], p["end_bank"]))
            else:
                L.append("| %s | 0 | | | | | | | |" % name)
        if sl.get("blend_weights"):
            L.append("")
            L.append("Blend weights fitted on the other season(s): %s, rest on the pre-close market." % sl["blend_weights"])
        L.append("")
    open(REPORT, "w").write("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true"); ap.add_argument("--report", action="store_true")
    ap.add_argument("--models", default="dc,elo,sot"); ap.add_argument("--seasons", default="2425,2526,2627")
    ap.add_argument("--groups", default=",".join(D.GROUPS))
    a = ap.parse_args()
    if a.run:
        run(a.models.split(","), a.seasons.split(","), a.groups.split(","))
    if a.report:
        report()
    if not (a.run or a.report):
        ap.print_help()
