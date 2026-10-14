#!/usr/bin/env python3
"""P-0148: does the analytic-gradient fit (P-0136) give the same backtest as the desk's finite-difference fit?

Uses pitch/backtest.py's own run_group (weekly walk-forward, refit on everything before the week) for
the dc model, season 2025-26, every group, twice: once as the desk is, once with model.fit replaced by
dc_grad.fit_grad. Writes nothing in pitch/; rows and scores go to this folder.
Usage: compare.py OUTDIR
"""
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-13-P-0136")
import backtest as B  # noqa: E402
import data as D  # noqa: E402
import model as M  # noqa: E402

SEASONS = ["2526"]


def job(args):
    variant, group = args
    if variant == "grad":
        import dc_grad
        M.fit = dc_grad.fit_grad
    t0 = time.time()
    rows = B.run_group((group, D.GROUPS[group], SEASONS, ["dc"]))
    for r in rows:
        r["variant"] = variant
    return rows, group, variant, time.time() - t0


def brier(df, cols):
    y = np.stack([(df.hg > df.ag), (df.hg == df.ag), (df.hg < df.ag)], 1).astype(float)
    return float(((df[cols].to_numpy() - y) ** 2).sum(1).mean())


def main():
    out = sys.argv[1]
    jobs = [(v, g) for v in ("fd", "grad") for g in D.GROUPS]
    with Pool(max(1, os.cpu_count() - 2)) as pool:
        res = pool.map(job, jobs)
    rows = [r for part, *_ in res for r in part]
    secs = {}
    for _, g, v, s in res:
        secs.setdefault(v, {})[g] = round(s, 1)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(out, "predictions.csv"), index=False)
    fd = df[df.variant == "fd"].set_index(["date", "home", "away"])
    gr = df[df.variant == "grad"].set_index(["date", "home", "away"])
    both = fd.join(gr[["ph", "pd", "pa"]], rsuffix="_g", how="inner")
    close = both.dropna(subset=["AvgCH", "AvgCD", "AvgCA"])
    mk = B.devig(close[["AvgCH", "AvgCD", "AvgCA"]].to_numpy(float))
    close = close.assign(mh=mk[:, 0], md=mk[:, 1], ma=mk[:, 2])
    summ = {
        "matches": len(both), "with_close": len(close),
        "brier_fd": round(brier(both, ["ph", "pd", "pa"]), 5), "brier_grad": round(brier(both, ["ph_g", "pd_g", "pa_g"]), 5),
        "max_abs_dp_home": round(float((both.ph - both.ph_g).abs().max()), 4),
        "mean_abs_dp_home": round(float((both.ph - both.ph_g).abs().mean()), 5),
        "close_rows": {"fd": round(brier(close, ["ph", "pd", "pa"]), 5), "grad": round(brier(close, ["ph_g", "pd_g", "pa_g"]), 5),
                       "market": round(brier(close, ["mh", "md", "ma"]), 5)},
        # in-sample log-opinion-pool weight on the model against the closing price, as backtest.py reports it
        "pool_weight_model": {v: round(B.best_weight(close[c].to_numpy(float), close[["mh", "md", "ma"]].to_numpy(float),
                                                     np.where(close.hg > close.ag, 0, np.where(close.hg == close.ag, 1, 2))), 2)
                              for v, c in (("fd", ["ph", "pd", "pa"]), ("grad", ["ph_g", "pd_g", "pa_g"]))},
        "seconds": secs,
    }
    json.dump(summ, open(os.path.join(out, "result.json"), "w"), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
