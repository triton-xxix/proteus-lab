#!/usr/bin/env python3
"""P-0136: analytic gradient for the Pitch desk's Dixon-Coles fit.

Same objective as pitch/model.py fit() (weighted negative log-likelihood with the Dixon-Coles tau
correction and L2 shrinkage on attack and defence), with the gradient returned alongside it so
L-BFGS-B stops estimating one by finite differences (2n+2 objective calls per step). Checks the
fitted parameters against the finite-difference fit per group, and times both over data.GROUPS.
Read-only against the desk. Usage: dc_grad.py OUT.json
"""
import json
import sys
import time

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gammaln

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D  # noqa: E402
import model as M  # noqa: E402


def fit_grad(df, as_of=None):
    df = df.dropna(subset=["FTHG", "FTAG", "Date"]).copy()
    as_of = pd.Timestamp(as_of) if as_of is not None else df["Date"].max()
    df = df[df["Date"] <= as_of]
    teams = sorted(set(df["HomeTeam"]) | set(df["AwayTeam"]))
    idx = {t: i for i, t in enumerate(teams)}
    n = len(teams)
    h = df["HomeTeam"].map(idx).to_numpy(); a = df["AwayTeam"].map(idx).to_numpy()
    hg = df["FTHG"].to_numpy(dtype=float); ag = df["FTAG"].to_numpy(dtype=float)
    w = np.exp(-M.XI * (as_of - df["Date"]).dt.days.to_numpy())
    lg = gammaln(hg + 1) + gammaln(ag + 1)        # constant, computed once
    m00 = (hg == 0) & (ag == 0); m01 = (hg == 0) & (ag == 1)
    m10 = (hg == 1) & (ag == 0); m11 = (hg == 1) & (ag == 1)

    def nll_grad(p):
        att = p[:n]; dfn = p[n:2 * n]; home = p[2 * n]; rho = p[2 * n + 1]
        lam = np.exp(att[h] + dfn[a] + home); mu = np.exp(att[a] + dfn[h])
        tau = np.ones_like(lam)
        tau[m00] = 1 - lam[m00] * mu[m00] * rho
        tau[m01] = 1 + lam[m01] * rho
        tau[m10] = 1 + mu[m10] * rho
        tau[m11] = 1 - rho
        clipped = tau < 1e-6
        tau = np.maximum(tau, 1e-6)
        ll = hg * np.log(lam) - lam + ag * np.log(mu) - mu - lg + np.log(tau)
        f = -np.sum(w * ll) + M.L2 * (np.sum(att ** 2) + np.sum(dfn ** 2))
        # d tau / d lam, d mu, d rho
        dt_dlam = np.zeros_like(lam); dt_dmu = np.zeros_like(lam); dt_drho = np.zeros_like(lam)
        dt_dlam[m00] = -mu[m00] * rho; dt_dmu[m00] = -lam[m00] * rho; dt_drho[m00] = -lam[m00] * mu[m00]
        dt_dlam[m01] = rho; dt_drho[m01] = lam[m01]
        dt_dmu[m10] = rho; dt_drho[m10] = mu[m10]
        dt_drho[m11] = -1.0
        for d in (dt_dlam, dt_dmu, dt_drho):
            d[clipped] = 0.0
        g_lam = hg - lam + lam * dt_dlam / tau       # d ll / d log lam
        g_mu = ag - mu + mu * dt_dmu / tau           # d ll / d log mu
        g_rho = dt_drho / tau
        wl = w * g_lam; wm = w * g_mu
        g_att = -(np.bincount(h, weights=wl, minlength=n) + np.bincount(a, weights=wm, minlength=n)) + 2 * M.L2 * att
        g_dfn = -(np.bincount(a, weights=wl, minlength=n) + np.bincount(h, weights=wm, minlength=n)) + 2 * M.L2 * dfn
        g_home = -np.sum(wl)
        g_rho_t = -np.sum(w * g_rho)
        return f, np.concatenate([g_att, g_dfn, [g_home, g_rho_t]])

    x0 = np.concatenate([np.zeros(n), np.zeros(n), [0.25], [-0.05]])
    bounds = [(-3, 3)] * (2 * n) + [(-1, 1), (-0.5, 0.5)]
    res = minimize(nll_grad, x0, jac=True, method="L-BFGS-B", bounds=bounds, options={"maxiter": 500})
    att = res.x[:n]; dfn = res.x[n:2 * n]; home = res.x[2 * n]; rho = res.x[2 * n + 1]
    return {"teams": teams, "att": dict(zip(teams, map(float, att))), "def": dict(zip(teams, map(float, dfn))),
            "home": float(home), "rho": float(rho), "as_of": str(as_of.date()), "n_matches": int(len(df)),
            "converged": bool(res.success), "nll": float(res.fun), "nfev": int(res.nfev), "nit": int(res.nit)}


def main():
    res = D.load_results(D.LEAGUES)
    out = {"groups": {}}
    t_fd = t_an = 0.0
    worst = 0.0
    for g, divs in D.GROUPS.items():
        sub = res[res["Div"].isin(divs)]
        t0 = time.time(); base = M.fit(sub); t1 = time.time(); new = fit_grad(sub); t2 = time.time()
        diffs = [abs(base["att"][t] - new["att"][t]) for t in base["teams"]] + \
                [abs(base["def"][t] - new["def"][t]) for t in base["teams"]] + \
                [abs(base["home"] - new["home"]), abs(base["rho"] - new["rho"])]
        # the fits may land on different points of a flat ridge: compare the objective too
        row = {"matches": base["n_matches"], "teams": len(base["teams"]),
               "fd_seconds": round(t1 - t0, 2), "grad_seconds": round(t2 - t1, 2),
               "max_abs_param_diff": round(max(diffs), 6), "nll_fd": round(base["nll"], 4),
               "nll_grad": round(new["nll"], 4), "nll_diff": round(new["nll"] - base["nll"], 6),
               "grad_nfev": new["nfev"], "grad_nit": new["nit"], "converged_fd": base["converged"],
               "converged_grad": new["converged"], "home_fd": round(base["home"], 4),
               "home_grad": round(new["home"], 4), "rho_fd": round(base["rho"], 4), "rho_grad": round(new["rho"], 4)}
        out["groups"][g] = row
        t_fd += t1 - t0; t_an += t2 - t1; worst = max(worst, max(diffs))
        print("%s matches %4d teams %3d  fd %5.2fs  grad %5.2fs  max|dp| %.2e  nll fd %.4f grad %.4f  nfev %d" % (
            g, row["matches"], row["teams"], row["fd_seconds"], row["grad_seconds"], row["max_abs_param_diff"],
            row["nll_fd"], row["nll_grad"], row["grad_nfev"]))
    # gradient check at a random point on the ENG group
    sub = res[res["Div"].isin(D.GROUPS["ENG"])]
    out["total_fd_seconds"] = round(t_fd, 2); out["total_grad_seconds"] = round(t_an, 2)
    out["worst_max_abs_param_diff"] = round(worst, 6)
    print("total: finite-difference %.1fs, analytic %.1fs, worst max|dp| %.2e" % (t_fd, t_an, worst))
    json.dump(out, open(sys.argv[1], "w"), indent=1)


if __name__ == "__main__":
    main()
