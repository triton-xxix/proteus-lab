#!/usr/bin/env python3
"""Dixon-Coles (1997) bivariate Poisson with time decay. Version 0: pure Dixon-Coles, fitted jointly
on Premier League and Championship so promoted and relegated sides carry their strength across.
Elo blend is version 1 and not claimed yet.

fit(results_df, as_of) -> params; predict(params, home, away) -> dict of probabilities.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gammaln

XI = 0.0065          # time decay per day (half-life about 107 days), Dixon-Coles' own order of magnitude
MAX_GOALS = 10
L2 = 0.02            # shrinkage on attack and defence; also pins the identifiability of the model


def _tau_vec(x, y, lam, mu, rho):
    t = np.ones_like(lam)
    m = (x == 0) & (y == 0); t[m] = 1 - lam[m] * mu[m] * rho
    m = (x == 0) & (y == 1); t[m] = 1 + lam[m] * rho
    m = (x == 1) & (y == 0); t[m] = 1 + mu[m] * rho
    m = (x == 1) & (y == 1); t[m] = 1 - rho
    return np.clip(t, 1e-6, None)


def _tau(x, y, lam, mu, rho):
    if x == 0 and y == 0:
        return 1 - lam * mu * rho
    if x == 0 and y == 1:
        return 1 + lam * rho
    if x == 1 and y == 0:
        return 1 + mu * rho
    if x == 1 and y == 1:
        return 1 - rho
    return 1.0


def _logpois(k, lam):
    return k * np.log(lam) - lam - gammaln(k + 1)


def fit(df, as_of=None):
    df = df.dropna(subset=["FTHG", "FTAG", "Date"]).copy()
    as_of = pd.Timestamp(as_of) if as_of is not None else df["Date"].max()
    df = df[df["Date"] <= as_of]
    teams = sorted(set(df["HomeTeam"]) | set(df["AwayTeam"]))
    idx = {t: i for i, t in enumerate(teams)}
    n = len(teams)
    h = df["HomeTeam"].map(idx).to_numpy(); a = df["AwayTeam"].map(idx).to_numpy()
    hg = df["FTHG"].to_numpy(dtype=float); ag = df["FTAG"].to_numpy(dtype=float)
    w = np.exp(-XI * (as_of - df["Date"]).dt.days.to_numpy())
    lg = gammaln(hg + 1) + gammaln(ag + 1)        # constant, computed once
    m00 = (hg == 0) & (ag == 0); m01 = (hg == 0) & (ag == 1)
    m10 = (hg == 1) & (ag == 0); m11 = (hg == 1) & (ag == 1)

    # Same objective as before 14 Oct 2026, returned with its analytic gradient so L-BFGS-B stops
    # estimating one by finite differences (P-0136; P-0148: 2025-26 backtest Brier identical to 5
    # decimals over 3,134 matches, max p_home move 0.003, about 23x faster).
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
        f = -np.sum(w * ll) + L2 * (np.sum(att ** 2) + np.sum(dfn ** 2))
        dt_dlam = np.zeros_like(lam); dt_dmu = np.zeros_like(lam); dt_drho = np.zeros_like(lam)
        dt_dlam[m00] = -mu[m00] * rho; dt_dmu[m00] = -lam[m00] * rho; dt_drho[m00] = -lam[m00] * mu[m00]
        dt_dlam[m01] = rho; dt_drho[m01] = lam[m01]
        dt_dmu[m10] = rho; dt_drho[m10] = mu[m10]
        dt_drho[m11] = -1.0
        for d in (dt_dlam, dt_dmu, dt_drho):
            d[clipped] = 0.0
        wl = w * (hg - lam + lam * dt_dlam / tau)     # d ll / d log lam, weighted
        wm = w * (ag - mu + mu * dt_dmu / tau)        # d ll / d log mu, weighted
        g_att = -(np.bincount(h, weights=wl, minlength=n) + np.bincount(a, weights=wm, minlength=n)) + 2 * L2 * att
        g_dfn = -(np.bincount(a, weights=wl, minlength=n) + np.bincount(h, weights=wm, minlength=n)) + 2 * L2 * dfn
        return f, np.concatenate([g_att, g_dfn, [-np.sum(wl)], [-np.sum(w * dt_drho / tau)]])

    x0 = np.concatenate([np.zeros(n), np.zeros(n), [0.25], [-0.05]])
    bounds = [(-3, 3)] * (2 * n) + [(-1, 1), (-0.5, 0.5)]
    res = minimize(nll_grad, x0, jac=True, method="L-BFGS-B", bounds=bounds, options={"maxiter": 500})
    att = res.x[:n]; dfn = res.x[n:2 * n]; home = res.x[2 * n]; rho = res.x[2 * n + 1]
    return {"teams": teams, "att": dict(zip(teams, map(float, att))), "def": dict(zip(teams, map(float, dfn))),
            "home": float(home), "rho": float(rho), "as_of": str(as_of.date()), "n_matches": int(len(df)),
            "converged": bool(res.success), "nll": float(res.fun)}


def predict(params, home, away):
    if home not in params["att"] or away not in params["att"]:
        return None
    lam = float(np.exp(params["att"][home] + params["def"][away] + params["home"]))
    mu = float(np.exp(params["att"][away] + params["def"][home]))
    rho = params["rho"]
    k = np.arange(MAX_GOALS + 1)
    ph = np.exp(_logpois(k, lam)); pa = np.exp(_logpois(k, mu))
    grid = np.outer(ph, pa)
    for x in range(2):
        for y in range(2):
            grid[x, y] *= _tau(x, y, lam, mu, rho)
    grid = np.clip(grid, 0, None); grid /= grid.sum()
    p_home = float(np.tril(grid, -1).sum()); p_away = float(np.triu(grid, 1).sum()); p_draw = float(np.trace(grid))
    tot = np.add.outer(k, k)
    over25 = float(grid[tot > 2.5].sum())
    return {"p_home": round(p_home, 4), "p_draw": round(p_draw, 4), "p_away": round(p_away, 4),
            "p_over25": round(over25, 4), "lam": round(lam, 3), "mu": round(mu, 3)}
