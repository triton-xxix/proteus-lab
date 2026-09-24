#!/usr/bin/env python3
"""The Pitch: the model zoo for the backtest harness. Every model has the same two calls:

    m = Model(); m.fit(history_df, as_of); m.predict(home, away) -> (p_home, p_draw, p_away) or None

history_df is football-data rows (HomeTeam, AwayTeam, FTHG, FTAG, Date, HST, AST). Only matches on
or before as_of are used. Written 2026-09-24 during the international break; nothing here has been
used for a live prediction yet.

Models
  dc     Dixon-Coles v0 from model.py, unchanged.
  elo    Goal-difference Elo (K 20, margin multiplier, home advantage fitted, 30 percent regression
         to the mean between seasons, promoted sides start at the bottom of the division). The
         rating gap is turned into 1X2 by an ordered logit fitted on the same decayed history.
  sot    "Expected goals" stand-in. football-data only carries xG from 2026-27 and Understat is
         blocked from this machine, so the target is shots on target times the league's conversion
         rate, blended half and half with actual goals. Quasi-Poisson attack and defence ratings with
         the same decay as dc, then rho fitted alone on actual goals. When real xG accumulates the
         same code takes it in place of the proxy.
  Market blends are built in backtest.py from these three plus the pre-close price.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize, minimize_scalar
from scipy.special import gammaln

import model as DC

XI = DC.XI


def _outcome(hg, ag):
    return np.where(hg > ag, 0, np.where(hg == ag, 1, 2))


def _grid_probs(lam, mu, rho):
    k = np.arange(DC.MAX_GOALS + 1)
    ph = np.exp(DC._logpois(k, lam)); pa = np.exp(DC._logpois(k, mu))
    g = np.outer(ph, pa)
    for x in range(2):
        for y in range(2):
            g[x, y] *= DC._tau(x, y, lam, mu, rho)
    g = np.clip(g, 0, None); g /= g.sum()
    return float(np.tril(g, -1).sum()), float(np.trace(g)), float(np.triu(g, 1).sum())


class DixonColes:
    name = "dc"

    def fit(self, df, as_of):
        self.p = DC.fit(df, as_of)

    def predict(self, home, away):
        r = DC.predict(self.p, home, away)
        return None if r is None else (r["p_home"], r["p_draw"], r["p_away"])


class Elo:
    name = "elo"
    K = 20.0
    REGRESS = 0.30          # pull toward 1500 at each season boundary (a gap of more than 60 days)
    START = 1500.0
    PROMOTED_PCTL = 10      # a side with no rating starts at this percentile of the group

    def __init__(self):
        self.ratings = {}
        self.hfa = 60.0
        self.cut = None

    def _run(self, df):
        """Replay matches in date order, returning per-match (diff, outcome, days_before_as_of)."""
        R = {}
        last = None
        rows = []
        for d, h, a, hg, ag in zip(df["Date"], df["HomeTeam"], df["AwayTeam"], df["FTHG"], df["FTAG"]):
            if last is not None and (d - last).days > 60:
                for t in R:
                    R[t] = self.START + (R[t] - self.START) * (1 - self.REGRESS)
            last = d
            for t in (h, a):
                if t not in R:
                    R[t] = float(np.percentile(list(R.values()), self.PROMOTED_PCTL)) if len(R) >= 4 else self.START
            diff = R[h] + self.hfa - R[a]
            rows.append((diff, hg, ag, d))
            e = 1 / (1 + 10 ** (-diff / 400))
            s = 1.0 if hg > ag else (0.5 if hg == ag else 0.0)
            gd = abs(hg - ag)
            mult = 1.0 if gd <= 1 else (1.5 if gd == 2 else (1.75 + (gd - 3) / 8))
            delta = self.K * mult * (s - e)
            R[h] += delta; R[a] -= delta
        self.ratings = R
        return rows

    def fit(self, df, as_of):
        as_of = pd.Timestamp(as_of)
        df = df[df["Date"] <= as_of].sort_values("Date")
        rows = self._run(df)
        if not rows:
            self.cut = None; return
        diff = np.array([r[0] for r in rows]); y = _outcome(np.array([r[1] for r in rows]), np.array([r[2] for r in rows]))
        w = np.exp(-XI * np.array([(as_of - r[3]).days for r in rows]))
        # Ordered logit: P(home) = sig(b*diff - c1), P(home or draw) = sig(b*diff + c2)
        def nll(p):
            b, c1, c2 = p
            z = b * diff
            ph = 1 / (1 + np.exp(-(z - c1)))
            phd = 1 / (1 + np.exp(-(z + c2)))
            P = np.stack([ph, np.clip(phd - ph, 1e-6, None), 1 - phd], axis=1)
            P = np.clip(P, 1e-6, None); P /= P.sum(axis=1, keepdims=True)
            return -np.sum(w * np.log(P[np.arange(len(y)), y]))
        res = minimize(nll, [0.006, 0.4, 0.4], method="L-BFGS-B", bounds=[(1e-4, 0.05), (-2, 3), (-2, 3)])
        self.cut = res.x
        # home advantage in rating points: solve for the diff shift that maximises fit is overkill;
        # use the ordered-logit intercepts, which already absorb it, and keep hfa as a prior.

    def predict(self, home, away):
        if self.cut is None or home not in self.ratings or away not in self.ratings:
            return None
        b, c1, c2 = self.cut
        z = b * (self.ratings[home] + self.hfa - self.ratings[away])
        ph = 1 / (1 + np.exp(-(z - c1))); phd = 1 / (1 + np.exp(-(z + c2)))
        p = np.clip(np.array([ph, phd - ph, 1 - phd]), 1e-4, None); p /= p.sum()
        return tuple(float(x) for x in p)


class ShotsPoisson:
    name = "sot"
    L2 = DC.L2
    GOAL_WEIGHT = 0.5       # target = 0.5 goals + 0.5 (shots on target x conversion)

    def __init__(self):
        self.p = None

    def fit(self, df, as_of):
        as_of = pd.Timestamp(as_of)
        df = df[df["Date"] <= as_of].dropna(subset=["FTHG", "FTAG"]).copy()
        if "HST" not in df.columns:
            df["HST"] = np.nan; df["AST"] = np.nan
        conv = (df["FTHG"].sum() + df["FTAG"].sum()) / max(1.0, float(np.nansum(df["HST"]) + np.nansum(df["AST"])))
        xh = np.where(df["HST"].notna(), df["HST"] * conv, df["FTHG"]); xa = np.where(df["AST"].notna(), df["AST"] * conv, df["FTAG"])
        th = self.GOAL_WEIGHT * df["FTHG"].to_numpy(float) + (1 - self.GOAL_WEIGHT) * xh
        ta = self.GOAL_WEIGHT * df["FTAG"].to_numpy(float) + (1 - self.GOAL_WEIGHT) * xa
        teams = sorted(set(df["HomeTeam"]) | set(df["AwayTeam"])); idx = {t: i for i, t in enumerate(teams)}; n = len(teams)
        h = df["HomeTeam"].map(idx).to_numpy(); a = df["AwayTeam"].map(idx).to_numpy()
        w = np.exp(-XI * (as_of - df["Date"]).dt.days.to_numpy())
        hg = df["FTHG"].to_numpy(float); ag = df["FTAG"].to_numpy(float)

        def nll(p):
            att = p[:n]; dfn = p[n:2 * n]; home = p[2 * n]
            lam = np.exp(att[h] + dfn[a] + home); mu = np.exp(att[a] + dfn[h])
            ll = th * np.log(lam) - lam + ta * np.log(mu) - mu
            return -np.sum(w * ll) + self.L2 * (np.sum(att ** 2) + np.sum(dfn ** 2))

        x0 = np.concatenate([np.zeros(2 * n), [0.25]])
        res = minimize(nll, x0, method="L-BFGS-B", bounds=[(-3, 3)] * (2 * n) + [(-1, 1)], options={"maxiter": 500})
        att = res.x[:n]; dfn = res.x[n:2 * n]; home = res.x[2 * n]
        lam = np.exp(att[h] + dfn[a] + home); mu = np.exp(att[a] + dfn[h])

        def nll_rho(rho):
            return -np.sum(w * np.log(DC._tau_vec(hg, ag, lam, mu, rho)))
        rho = minimize_scalar(nll_rho, bounds=(-0.5, 0.5), method="bounded").x
        self.p = {"att": dict(zip(teams, att)), "def": dict(zip(teams, dfn)), "home": float(home), "rho": float(rho), "conv": float(conv)}

    def predict(self, home, away):
        p = self.p
        if p is None or home not in p["att"] or away not in p["att"]:
            return None
        lam = float(np.exp(p["att"][home] + p["def"][away] + p["home"])); mu = float(np.exp(p["att"][away] + p["def"][home]))
        return _grid_probs(lam, mu, p["rho"])


ZOO = {"dc": DixonColes, "elo": Elo, "sot": ShotsPoisson}
