#!/usr/bin/env python3
"""P-0147: a per-referee home-advantage offset in the Pitch desk's Dixon-Coles, out of sample.

Rules fixed before the first run (14 Oct 2026, nightly):
- Groups ENG (E0, E1) and SCO (SC0), every season in the desk cache. Test matches: E0, E1, SC0 from
  1 Aug 2023 (2022-23 is burn-in for referee offsets), to the latest result.
- Walk forward by calendar month: fit on everything before the month's first day, predict that month.
- Plain: the desk objective (time decay XI, L2 on attack and defence), analytic gradient from P-0136.
- Referee: same, plus log(lambda_home) += r[referee], L2_REF = 2.0 on r (strong shrinkage: about 20
  games before an offset moves far). A referee unseen before the month gets r = 0.
- Scores: 1X2 Brier (sum of three squared errors) and over-2.5 Brier, against Pinnacle closing
  (PSCH/PSCD/PSCA, PC>2.5, PC<2.5), margin removed proportionally; matches without closing odds are
  scored for the models only and counted separately.
"""
import json
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gammaln

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D  # noqa: E402
import model as M  # noqa: E402

L2_REF = 2.0
TEST_FROM = pd.Timestamp("2023-08-01")


def fit(df, as_of, use_ref):
    df = df[df["Date"] < as_of]
    teams = sorted(set(df["HomeTeam"]) | set(df["AwayTeam"]))
    idx = {t: i for i, t in enumerate(teams)}
    refs = sorted(set(df["Referee"].dropna())) if use_ref else []
    ridx = {r: i for i, r in enumerate(refs)}
    n, R = len(teams), len(refs)
    h = df["HomeTeam"].map(idx).to_numpy(); a = df["AwayTeam"].map(idx).to_numpy()
    k = df["Referee"].map(ridx).fillna(-1).astype(int).to_numpy() if use_ref else np.full(len(df), -1)
    has = k >= 0; kk = np.where(has, k, 0)
    hg = df["FTHG"].to_numpy(float); ag = df["FTAG"].to_numpy(float)
    w = np.exp(-M.XI * (as_of - df["Date"]).dt.days.to_numpy())
    lg = gammaln(hg + 1) + gammaln(ag + 1)
    m00 = (hg == 0) & (ag == 0); m01 = (hg == 0) & (ag == 1); m10 = (hg == 1) & (ag == 0); m11 = (hg == 1) & (ag == 1)

    def f(p):
        att = p[:n]; dfn = p[n:2 * n]; home = p[2 * n]; rho = p[2 * n + 1]; r = p[2 * n + 2:]
        roff = np.where(has, r[kk], 0.0) if R else 0.0
        lam = np.exp(att[h] + dfn[a] + home + roff); mu = np.exp(att[a] + dfn[h])
        tau = np.ones_like(lam)
        tau[m00] = 1 - lam[m00] * mu[m00] * rho; tau[m01] = 1 + lam[m01] * rho
        tau[m10] = 1 + mu[m10] * rho; tau[m11] = 1 - rho
        clipped = tau < 1e-6; tau = np.maximum(tau, 1e-6)
        ll = hg * np.log(lam) - lam + ag * np.log(mu) - mu - lg + np.log(tau)
        val = -np.sum(w * ll) + M.L2 * (np.sum(att ** 2) + np.sum(dfn ** 2)) + L2_REF * np.sum(r ** 2)
        dl = np.zeros_like(lam); dm = np.zeros_like(lam); dr = np.zeros_like(lam)
        dl[m00] = -mu[m00] * rho; dm[m00] = -lam[m00] * rho; dr[m00] = -lam[m00] * mu[m00]
        dl[m01] = rho; dr[m01] = lam[m01]; dm[m10] = rho; dr[m10] = mu[m10]; dr[m11] = -1.0
        for d in (dl, dm, dr):
            d[clipped] = 0.0
        wl = w * (hg - lam + lam * dl / tau); wm = w * (ag - mu + mu * dm / tau)
        g_att = -(np.bincount(h, weights=wl, minlength=n) + np.bincount(a, weights=wm, minlength=n)) + 2 * M.L2 * att
        g_dfn = -(np.bincount(a, weights=wl, minlength=n) + np.bincount(h, weights=wm, minlength=n)) + 2 * M.L2 * dfn
        g = [g_att, g_dfn, [-np.sum(wl)], [-np.sum(w * dr / tau)]]
        if R:
            g.append(-np.bincount(kk[has], weights=wl[has], minlength=R) + 2 * L2_REF * r)
        return val, np.concatenate(g)

    x0 = np.concatenate([np.zeros(2 * n), [0.25, -0.05], np.zeros(R)])
    bounds = [(-3, 3)] * (2 * n) + [(-1, 1), (-0.5, 0.5)] + [(-1, 1)] * R
    res = minimize(f, x0, jac=True, method="L-BFGS-B", bounds=bounds, options={"maxiter": 500})
    p = res.x
    return {"idx": idx, "att": p[:n], "def": p[n:2 * n], "home": p[2 * n], "rho": p[2 * n + 1],
            "ref": {r: p[2 * n + 2 + i] for r, i in ridx.items()}}


def probs(P, home, away, ref):
    if home not in P["idx"] or away not in P["idx"]:
        return None
    i, j = P["idx"][home], P["idx"][away]
    lam = np.exp(P["att"][i] + P["def"][j] + P["home"] + P["ref"].get(ref, 0.0))
    mu = np.exp(P["att"][j] + P["def"][i])
    kgoals = np.arange(M.MAX_GOALS + 1)
    g = np.outer(np.exp(M._logpois(kgoals, lam)), np.exp(M._logpois(kgoals, mu)))
    for x in range(2):
        for y in range(2):
            g[x, y] *= M._tau(x, y, lam, mu, P["rho"])
    g = np.clip(g, 0, None); g /= g.sum()
    tot = np.add.outer(kgoals, kgoals)
    return np.array([np.tril(g, -1).sum(), np.trace(g), np.triu(g, 1).sum()]), float(g[tot > 2].sum())


def main():
    out_path = sys.argv[1]
    allres = D.load_results(("E0", "E1", "SC0"))
    rows = []
    for grp, divs in (("ENG", ("E0", "E1")), ("SCO", ("SC0",))):
        df = allres[allres["Div"].isin(divs)].dropna(subset=["Date"]).copy()
        test = df[df["Date"] >= TEST_FROM]
        months = sorted(set(test["Date"].dt.to_period("M")))
        for mth in months:
            start = mth.to_timestamp()
            plain = fit(df, start, False); withref = fit(df, start, True)
            for _, m in test[test["Date"].dt.to_period("M") == mth].iterrows():
                a = probs(plain, m["HomeTeam"], m["AwayTeam"], None)
                b = probs(withref, m["HomeTeam"], m["AwayTeam"], m.get("Referee"))
                if a is None or b is None:
                    continue
                y = np.array([m["FTHG"] > m["FTAG"], m["FTHG"] == m["FTAG"], m["FTHG"] < m["FTAG"]], float)
                o = float(m["FTHG"] + m["FTAG"] > 2)
                row = {"div": m["Div"], "date": str(m["Date"].date()), "ref_seen": m.get("Referee") in withref["ref"],
                       "b_plain": float(((a[0] - y) ** 2).sum()), "b_ref": float(((b[0] - y) ** 2).sum()),
                       "o_plain": (a[1] - o) ** 2, "o_ref": (b[1] - o) ** 2}
                try:
                    imp = 1 / np.array([m["PSCH"], m["PSCD"], m["PSCA"]], float)
                    if np.all(np.isfinite(imp)):
                        row["b_mkt"] = float(((imp / imp.sum() - y) ** 2).sum())
                    io = 1 / np.array([m["PC>2.5"], m["PC<2.5"]], float)
                    if np.all(np.isfinite(io)):
                        row["o_mkt"] = float((io[0] / io.sum() - o) ** 2)
                except (KeyError, TypeError, ValueError):
                    pass
                rows.append(row)
            print(grp, mth, len(rows), flush=True)
    R = pd.DataFrame(rows)
    d = R["b_ref"] - R["b_plain"]
    od = R["o_ref"] - R["o_plain"]
    mk = R.dropna(subset=["b_mkt"])
    summ = {
        "n": len(R), "n_with_close": len(mk), "share_ref_seen": round(float(R["ref_seen"].mean()), 3),
        "brier_plain": round(R["b_plain"].mean(), 5), "brier_ref": round(R["b_ref"].mean(), 5),
        "ref_minus_plain": round(d.mean(), 5), "se": round(d.std() / np.sqrt(len(d)), 5),
        "over_plain": round(R["o_plain"].mean(), 5), "over_ref": round(R["o_ref"].mean(), 5),
        "over_ref_minus_plain": round(od.mean(), 5), "over_se": round(od.std() / np.sqrt(len(od)), 5),
        "on_close_rows": {"plain": round(mk["b_plain"].mean(), 5), "ref": round(mk["b_ref"].mean(), 5),
                          "market": round(mk["b_mkt"].mean(), 5)},
        "over_on_close_rows": {"plain": round(mk.dropna(subset=["o_mkt"])["o_plain"].mean(), 5),
                               "ref": round(mk.dropna(subset=["o_mkt"])["o_ref"].mean(), 5),
                               "market": round(mk["o_mkt"].mean(), 5)},
        "by_div": {dv: round(float((g["b_ref"] - g["b_plain"]).mean()), 5) for dv, g in R.groupby("div")},
    }
    json.dump(summ, open(out_path, "w"), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
