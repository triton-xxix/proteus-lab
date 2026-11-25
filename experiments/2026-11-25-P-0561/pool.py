"""P-0561: bias-correct, then pool, the Munich ICON-EPS and ECMWF IFS day-ahead 10 to 90 bands.

arXiv 2610.42130's order (read-it item, 25 Nov): calibrate each source, blend, recalibrate. Observations are
the same ones the capture scripts score against: DWD 03379 (Stadt) daily high via munich_forecast_error.py.

Two honesty modes for the shift (a band's own mean miss, obs minus its p50):
  past: only days before the target day (what I could have used that night); needs at least 5 prior days
  loo:  every other scored day (leave-one-out; uses the future, so an upper bound)
Variants, each counted inside against 80%:
  raw ICON, raw ECMWF, shifted ICON, shifted ECMWF, union of shifted, mean of shifted,
  mean of shifted widened by a past-only scale so its past coverage is 80% (the "recalibrate" step).
"""
import importlib.util
import json
from pathlib import Path

ROOT = "/Users/triton/PROTEUS"
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)
obs = mfe.observed("10865")


def load(name):
    return {r["day"]: r for r in (json.loads(l) for l in open(ROOT + "/exchange/" + name) if l.strip())}


icon, ecm = load("icon_eps_band.jsonl"), load("ecmwf_ens_band.jsonl")
days = sorted(d for d in icon if d in ecm and d in obs)
miss = {"icon": {d: obs[d] - icon[d]["p50"] for d in days}, "ecm": {d: obs[d] - ecm[d]["p50"] for d in days}}
MIN_PRIOR = 5


def shift(src, d, mode):
    others = [miss[src][x] for x in days if (x < d if mode == "past" else x != d)]
    if mode == "past" and len(others) < MIN_PRIOR:
        return None
    return sum(others) / len(others)


def inside(lo, hi, y):
    return lo <= y <= hi


def run(mode):
    counts, n, widths = {}, 0, {}
    rows = []
    scale_hist = []  # past mean-of-shifted half-widths and |obs - centre| to set the widening factor
    for d in days:
        si, se = shift("icon", d, mode), shift("ecm", d, mode)
        y = obs[d]
        i, e = icon[d], ecm[d]
        if si is None or se is None:
            continue
        n += 1
        bands = {
            "raw_icon": (i["p10"], i["p90"]),
            "raw_ecmwf": (e["p10"], e["p90"]),
            "shift_icon": (i["p10"] + si, i["p90"] + si),
            "shift_ecmwf": (e["p10"] + se, e["p90"] + se),
        }
        bands["union_shifted"] = (min(bands["shift_icon"][0], bands["shift_ecmwf"][0]), max(bands["shift_icon"][1], bands["shift_ecmwf"][1]))
        mlo = (bands["shift_icon"][0] + bands["shift_ecmwf"][0]) / 2
        mhi = (bands["shift_icon"][1] + bands["shift_ecmwf"][1]) / 2
        bands["mean_shifted"] = (mlo, mhi)
        c, h = (mlo + mhi) / 2, (mhi - mlo) / 2
        # recalibrate: smallest factor k (0.1 steps) at which at least 80% of PRIOR days' |obs - centre| <= k * half-width
        prior = [x for x in scale_hist if True]
        k = None
        if len(prior) >= MIN_PRIOR:
            for kk in [x / 10 for x in range(5, 61)]:
                if sum(a <= kk * hw for a, hw in prior) >= 0.8 * len(prior):
                    k = kk
                    break
        if k is not None:
            bands["mean_shifted_recal"] = (c - k * h, c + k * h)
        scale_hist.append((abs(y - c), h))
        row = {"day": d, "obs": y, "k": k}
        for name, (lo, hi) in bands.items():
            hit = inside(lo, hi, y)
            counts.setdefault(name, [0, 0])
            counts[name][0] += hit
            counts[name][1] += 1
            widths.setdefault(name, []).append(hi - lo)
            row[name] = [round(lo, 2), round(hi, 2), hit]
        rows.append(row)
    summary = {name: {"inside": c[0], "days": c[1], "rate": round(c[0] / c[1], 3) if c[1] else None,
                      "mean_width": round(sum(widths[name]) / len(widths[name]), 2)} for name, c in counts.items()}
    return {"days": n, "summary": summary, "rows": rows}


import sys
if sys.argv[1:2] == ["--forward"]:
    # D-035: the forward test registered 25 Nov. Past-only shifts may use every earlier day, but only target
    # days from 2026-11-26 are counted.
    fw = run("past")
    fw_rows = [r for r in fw["rows"] if r["day"] >= "2026-11-26"]
    for name in ("union_shifted", "shift_icon", "raw_icon"):
        hits = sum(r[name][2] for r in fw_rows)
        print("forward %-14s %d of %d inside" % (name, hits, len(fw_rows)))
    sys.exit(0)

out = {"scored_days_both": len(days), "first": days[0] if days else None, "last": days[-1] if days else None,
       "mean_miss_icon": round(sum(miss["icon"].values()) / len(days), 2),
       "mean_miss_ecmwf": round(sum(miss["ecm"].values()) / len(days), 2),
       "past": run("past"), "loo": run("loo")}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print("days scored in both: %d (%s to %s); mean miss obs-p50: ICON %+.2f, ECMWF %+.2f"
      % (out["scored_days_both"], out["first"], out["last"], out["mean_miss_icon"], out["mean_miss_ecmwf"]))
for mode in ("past", "loo"):
    print("--", mode, "(days counted %d)" % out[mode]["days"])
    for name, s in out[mode]["summary"].items():
        print("  %-20s %2d of %2d inside  %.0f%%  width %.2f C" % (name, s["inside"], s["days"], 100 * s["rate"], s["mean_width"]))
