"""P-0420: Munich ICON town bias by the FORECAST sky.

P-0226 split the day-ahead error by observed sunshine, which is not known when the forecast is read.
Here the predictor is ICON's own day-ahead cloud cover (Open-Meteo previous-runs API,
cloud_cover_previous_day1, mean over 08:00 to 17:00 Berlin time) and, if served, its day-ahead sunshine
duration. A linear correction is fitted on 15 Aug to 12 Oct only and scored on 13 Oct to 11 Nov, beside
raw, flat +0.5, flat +1.0 and a two-bin rule fitted the same way. Town station only (DWD 03379).
"""
import importlib.util
import json

ROOT = "/Users/triton/PROTEUS"
OUT = ROOT + "/experiments/2026-11-12-P-0420/results.json"
spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)

IN = ("2026-08-15", "2026-10-12")
OUTW = ("2026-10-13", "2026-11-11")
VARS = ["temperature_2m", "cloud_cover", "sunshine_duration"]


def fetch(var):
    url = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s"
           "&hourly=%s_previous_day1&models=icon_seamless&past_days=92&forecast_days=1"
           "&timezone=Europe%%2FBerlin" % (mfe.LAT, mfe.LON, var))
    h = json.loads(mfe.get(url))["hourly"]
    key = [k for k in h if k.startswith(var + "_previous_day1")][0]
    return h["time"], h[key]


def daily(var, how):
    times, vals = fetch(var)
    out = {}
    for ts, v in zip(times, vals):
        if v is None:
            continue
        day, hour = ts[:10], int(ts[11:13])
        if how == "max":
            out[day] = max(out.get(day, -99), v)
        elif how == "daymean" and 8 <= hour <= 17:
            out.setdefault(day, []).append(v)
        elif how == "sum":
            out[day] = out.get(day, 0.0) + v
    if how == "daymean":
        out = {d: sum(v) / len(v) for d, v in out.items() if len(v) == 10}
    return out


def linfit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    syy = sum((y - my) ** 2 for y in ys)
    return a, b, (b * sxx / (sxx * syy) ** 0.5 if syy else None)


def mae(errs):
    return round(sum(abs(e) for e in errs) / len(errs), 3)


def main():
    tmax = daily("temperature_2m", "max")
    obs = mfe.observed_dwd("10865")
    preds, notes = {}, {}
    try:
        preds["cloud_cover_pct"] = daily("cloud_cover", "daymean")
    except Exception as e:  # noqa: BLE001
        notes["cloud_cover"] = "not served: %s" % str(e)[:80]
    try:
        sun = daily("sunshine_duration", "sum")
        preds["sunshine_hours"] = {d: v / 3600.0 for d, v in sun.items()}
    except Exception as e:  # noqa: BLE001
        notes["sunshine_duration"] = "not served: %s" % str(e)[:80]
    days_in = sorted(d for d in tmax if IN[0] <= d <= IN[1] and d in obs)
    days_out = sorted(d for d in tmax if OUTW[0] <= d <= OUTW[1] and d in obs)
    err = {d: tmax[d] - obs[d] for d in days_in + days_out}
    res = {"notes": notes, "n_in": len(days_in), "n_out": len(days_out),
           "in_sample": {"bias": round(sum(err[d] for d in days_in) / len(days_in), 2),
                         "mae_raw": mae([err[d] for d in days_in])},
           "out_of_sample": {"bias": round(sum(err[d] for d in days_out) / len(days_out), 2),
                             "mae_raw": mae([err[d] for d in days_out]),
                             "mae_flat_plus_0.5": mae([err[d] + 0.5 for d in days_out]),
                             "mae_flat_plus_1.0": mae([err[d] + 1.0 for d in days_out]),
                             "p0226_observed_sun_bound": 0.984},
           "predictors": {}}
    for name, p in preds.items():
        di = [d for d in days_in if d in p]
        do = [d for d in days_out if d in p]
        if len(di) < 20 or len(do) < 20:
            res["predictors"][name] = {"skipped": "too few days", "n_in": len(di), "n_out": len(do)}
            continue
        a, b, r = linfit([p[d] for d in di], [err[d] for d in di])
        ao, bo, ro = linfit([p[d] for d in do], [err[d] for d in do])
        # two-bin rule, cut at the in-sample median of the predictor
        cut = sorted(p[d] for d in di)[len(di) // 2]
        lo_in = [err[d] for d in di if p[d] < cut]
        hi_in = [err[d] for d in di if p[d] >= cut]
        m_lo, m_hi = sum(lo_in) / len(lo_in), sum(hi_in) / len(hi_in)
        lo_out = [err[d] for d in do if p[d] < cut]
        hi_out = [err[d] for d in do if p[d] >= cut]
        res["predictors"][name] = {
            "n_in": len(di), "n_out": len(do),
            "in_sample_fit": {"intercept": round(a, 3), "slope": round(b, 4), "r": round(r, 2)},
            "out_of_sample_own_fit_for_reference": {"intercept": round(ao, 3), "slope": round(bo, 4),
                                                    "r": round(ro, 2)},
            "mae_out_linear_from_in_sample": mae([err[d] - (a + b * p[d]) for d in do]),
            "mae_out_linear_refit_out_of_sample_cheating": mae([err[d] - (ao + bo * p[d]) for d in do]),
            "two_bin": {"cut": round(cut, 2), "in_bias_below": round(m_lo, 2), "in_bias_at_or_above": round(m_hi, 2),
                        "out_n_below": len(lo_out), "out_n_at_or_above": len(hi_out),
                        "out_bias_below": round(sum(lo_out) / len(lo_out), 2) if lo_out else None,
                        "out_bias_at_or_above": round(sum(hi_out) / len(hi_out), 2) if hi_out else None,
                        "mae_out": mae([err[d] - (m_lo if p[d] < cut else m_hi) for d in do])},
            "out_mean": round(sum(p[d] for d in do) / len(do), 2),
            "in_mean": round(sum(p[d] for d in di) / len(di), 2),
        }
    print(json.dumps(res, indent=1))
    json.dump(res, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
