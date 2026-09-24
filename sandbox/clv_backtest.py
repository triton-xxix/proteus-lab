#!/usr/bin/env python3
"""Does the Pitch's Dixon-Coles add anything to the closing price? Replays arXiv 2608.11505's test
on our own E0/E1 data.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/sandbox/clv_backtest.py

Walk-forward over 2025-26: refit weekly on everything strictly before the week, predict that week.
Compares model, pre-close average odds (AvgH/D/A, what the desk actually bets into) and closing
average odds (AvgCH/CD/CA), all with overround removed proportionally. Reports Brier, RPS, log loss,
the log-opinion-pool weight on the model against each market line, and a paper-bet replay of the
desk's rule (3 points of edge, quarter Kelly, capped at 10) at pre-close odds, settled on results
and measured on closing-line value.
"""
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D  # noqa: E402
import model as M  # noqa: E402

START, END = pd.Timestamp("2025-08-01"), pd.Timestamp("2026-06-30")


def devig(h, d, a):
    inv = np.array([1 / h, 1 / d, 1 / a])
    return inv / inv.sum()


def metrics(P, y):
    """P: n x 3 (home, draw, away); y: outcome index. Returns Brier, RPS, log loss."""
    Y = np.eye(3)[y]
    brier = np.mean(np.sum((P - Y) ** 2, axis=1))
    cP, cY = np.cumsum(P, axis=1)[:, :2], np.cumsum(Y, axis=1)[:, :2]
    rps = np.mean(np.sum((cP - cY) ** 2, axis=1) / 2)
    ll = -np.mean(np.log(np.clip(P[np.arange(len(y)), y], 1e-9, None)))
    return brier, rps, ll


def pool(Pm, Pk, w):
    """Logarithmic opinion pool: model weight w, market weight 1-w."""
    L = w * np.log(Pm) + (1 - w) * np.log(Pk)
    E = np.exp(L)
    return E / E.sum(axis=1, keepdims=True)


def best_weight(Pm, Pk, y):
    ws = np.linspace(0, 1, 101)
    lls = [metrics(pool(Pm, Pk, w), y)[2] for w in ws]
    return ws[int(np.argmin(lls))], min(lls)


def main():
    res = D.load_results()
    need = ["AvgH", "AvgD", "AvgA", "AvgCH", "AvgCD", "AvgCA"]
    test = res[(res["Date"] >= START) & (res["Date"] <= END)].dropna(subset=need).copy()
    test["week"] = test["Date"].dt.to_period("W-SUN").dt.start_time
    rows = []
    for wk, g in test.groupby("week"):
        params = M.fit(res, as_of=wk - pd.Timedelta(days=1))
        for _, r in g.iterrows():
            pr = M.predict(params, r["HomeTeam"], r["AwayTeam"])
            if not pr:
                continue
            y = 0 if r["FTHG"] > r["FTAG"] else (1 if r["FTHG"] == r["FTAG"] else 2)
            rows.append({"div": r["Div"], "y": y,
                         "m": [pr["p_home"], pr["p_draw"], pr["p_away"]],
                         "pre": devig(r["AvgH"], r["AvgD"], r["AvgA"]),
                         "close": devig(r["AvgCH"], r["AvgCD"], r["AvgCA"]),
                         "odds": [r["AvgH"], r["AvgD"], r["AvgA"]],
                         "codds": [r["AvgCH"], r["AvgCD"], r["AvgCA"]]})
        print("week", wk.date(), "matches", len(g), "cum", len(rows), flush=True)

    for div in ("ALL", "E0", "E1"):
        R = [r for r in rows if div == "ALL" or r["div"] == div]
        y = np.array([r["y"] for r in R])
        Pm = np.array([r["m"] for r in R]); Pm = Pm / Pm.sum(axis=1, keepdims=True)
        Pp = np.array([r["pre"] for r in R]); Pc = np.array([r["close"] for r in R])
        print("\n==", div, "n", len(R))
        for name, P in (("model", Pm), ("pre-close avg", Pp), ("closing avg", Pc)):
            b, rp, ll = metrics(P, y)
            print("%-14s brier %.4f  rps %.4f  logloss %.4f" % (name, b, rp, ll))
        for name, Pk in (("pre-close", Pp), ("closing", Pc)):
            w, ll = best_weight(Pm, Pk, y)
            print("pool weight on model vs %-9s %.2f (logloss %.4f)" % (name, w, ll))

        bank, staked, pnl, clvs, n = 100.0, 0.0, 0.0, [], 0
        for r in R:
            edge = np.array(r["m"]) - r["pre"]
            i = int(np.argmax(edge))
            if edge[i] <= 0.03:
                continue
            o = float(r["odds"][i]); p = r["m"][i]
            f = max(0.0, (p * (o - 1) - (1 - p)) / (o - 1)) * 0.25
            st = round(min(bank * f, 10.0), 2)
            if st < 0.5:
                continue
            ret = st * (o - 1) if r["y"] == i else -st
            bank += ret; staked += st; pnl += ret; n += 1
            clvs.append(o / float(r["codds"][i]) - 1)
        if n:
            print("paper bets %d  staked %.2f  pnl %+.2f  roi %+.1f%%  mean CLV %+.2f%%  beat close %d%%"
                  % (n, staked, pnl, 100 * pnl / staked, 100 * np.mean(clvs), 100 * np.mean(np.array(clvs) > 0)))


if __name__ == "__main__":
    main()
