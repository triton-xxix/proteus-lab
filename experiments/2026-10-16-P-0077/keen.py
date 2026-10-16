#!/usr/bin/env python3
"""P-0077: Keen's Goodwin-Minsky model (private debt, no government, no prices), rebuilt from the
equations as set out in Keen 1995 / Grasselli and Costa Lima 2012. Parameters are from memory of the
latter, not copied from the paper, so this is a rebuild test, not a replication.

omega = wage share, lam = employment rate, d = debt / output.
profit share pi = 1 - omega - r d. Growth g = kappa(pi)/v - delta.
omega' = omega (Phi(lam) - alpha), lam' = lam (g - alpha - beta), d' = kappa(pi) - pi - d g.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

alpha, beta, delta, v, r = 0.025, 0.02, 0.01, 3.0, 0.03
p0 = 0.04
phi0 = p0 / (1 - p0 ** 2)
phi1 = p0 ** 3 / (1 - p0 ** 2)
k0, k1, k2 = -0.0065, np.exp(-5), 20.0


def Phi(l):
    return phi1 / (1 - l) ** 2 - phi0


def kappa(pi):
    return k0 + k1 * np.exp(k2 * pi)


def rhs(t, y):
    w, l, d = y
    pi = 1 - w - r * d
    g = kappa(pi) / v - delta
    return [w * (Phi(l) - alpha), l * (g - alpha - beta), kappa(pi) - pi - d * (g + 0)]


def crash(t, y):
    return y[2] - 50 if y[2] < 50 else 0


crash.terminal = True


def run(y0, T=200):
    ev = lambda t, y: y[2] - 50
    ev.terminal = True
    ev2 = lambda t, y: y[1] - 0.02
    ev2.terminal = True
    s = solve_ivp(rhs, [0, T], y0, events=[ev, ev2], max_step=0.1, rtol=1e-8, atol=1e-10)
    return {"start": y0, "t_end": float(s.t[-1]), "end": [float(x) for x in s.y[:, -1]],
            "max_d": float(s.y[2].max()), "min_lam": float(s.y[1].min()),
            "ended_early": bool(s.t[-1] < T - 1e-6)}


out = {"params": dict(alpha=alpha, beta=beta, delta=delta, v=v, r=r, phi0=phi0, phi1=phi1, k0=k0, k1=float(k1), k2=k2)}
out["runs"] = [run(y0) for y in [0] for y0 in ([0.85, 0.95, 0.1], [0.85, 0.95, 1.0], [0.85, 0.95, 2.0],
                                                [0.75, 0.9, 0.3], [0.9, 0.97, 1.5],
                                                [0.85, 0.95, 4.0], [0.85, 0.95, 6.0], [0.85, 0.95, 10.0])]
# no-debt control: same start but r = 0 and kappa fixed at profit share (Goodwin cycle), no crash expected
json.dump(out, open("/Users/triton/PROTEUS/experiments/2026-10-16-P-0077/results.json", "w"), indent=1)
for x in out["runs"]:
    print(x["start"], "-> end", [round(a, 3) for a in x["end"]], "t", round(x["t_end"], 1), "max_d", round(x["max_d"], 2),
          "min_lam", round(x["min_lam"], 3), "early" if x["ended_early"] else "")
