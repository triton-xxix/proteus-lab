#!/usr/bin/env python3
"""Ran-it, 12 Oct 2026: pyinstrument on the Pitch desk's Dixon-Coles refit.
Read-only: loads the cached results, fits each country group as predict.py does, writes nothing to pitch/.
Counts objective calls by wrapping scipy.optimize.minimize, and saves pyinstrument's text and HTML report here."""
import sys, time, json
sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/pyinstrument-lib")
sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
from pyinstrument import Profiler
import scipy.optimize as so
import data as D
import model as M

OUT = "/Users/triton/PROTEUS/experiments/2026-10-12-pyinstrument-pitch"
calls = {"n": 0}
_orig = so.minimize


def counting_minimize(fun, x0, *a, **k):
    def f(p):
        calls["n"] += 1
        return fun(p)
    res = _orig(f, x0, *a, **k)
    calls["nit"] = int(res.nit); calls["nfev"] = int(res.nfev); calls["dim"] = len(x0)
    return res


M.minimize = counting_minimize
res = D.load_results(D.LEAGUES)
rows = []
prof = Profiler(interval=0.001)
prof.start()
for g, divs in D.GROUPS.items():
    calls.clear(); calls["n"] = 0
    t = time.perf_counter()
    p = M.fit(res[res["Div"].isin(divs)])
    dt = time.perf_counter() - t
    rows.append({"group": g, "matches": p["n_matches"], "teams": len(p["teams"]), "params": calls["dim"],
                 "iterations": calls["nit"], "objective_calls": calls["n"], "seconds": round(dt, 2),
                 "calls_per_iteration": round(calls["n"] / max(calls["nit"], 1), 1), "converged": p["converged"]})
prof.stop()
open(f"{OUT}/profile.txt", "w").write(prof.output_text(unicode=False, color=False))
open(f"{OUT}/profile.html", "w").write(prof.output_html())
json.dump(rows, open(f"{OUT}/result.json", "w"), indent=1)
for r in rows:
    print(r)
print("total seconds", round(sum(r["seconds"] for r in rows), 2))
