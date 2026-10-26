"""P-0225: does the 13 Oct Munich cold bias hold on the days after it was measured?

Reuses the 13 Oct script's fetchers unchanged (previous-runs API, hourly temperature issued one day
before, daily max per Berlin day; DWD recent daily KL, TXK). Splits the days into the original window
(15 Aug to 12 Oct, to check it reproduces) and the new window (13 Oct onward, out of sample).
"""
import importlib.util
import json

ROOT = "/Users/triton/PROTEUS"
spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)

WINDOWS = {"in_sample_15aug_12oct": ("2026-08-15", "2026-10-12"),
           "out_of_sample_from_13oct": ("2026-10-13", "2026-12-31")}


def stats(fc, obs, days, m):
    errs = [fc[d][m] - obs[d] for d in days]
    n = len(errs)
    if not n:
        return {"n": 0}
    mean = sum(errs) / n
    sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5 if n > 1 else None
    return {"n": n, "bias": round(mean, 2), "se": round(sd / n ** 0.5, 2) if sd else None,
            "mae": round(sum(abs(e) for e in errs) / n, 2),
            "right_degree": round(sum(mfe.rnd(fc[d][m]) == mfe.rnd(obs[d]) for d in days) / n, 2),
            "mae_after_plus1_correction": round(sum(abs(e + 1.0) for e in errs) / n, 2)}


def main():
    fc = mfe.forecasts(80)
    result = {}
    for sid, name in mfe.STATIONS.items():
        obs = mfe.observed(sid)
        result[name] = {}
        for wname, (lo, hi) in WINDOWS.items():
            days = sorted(d for d in fc if lo <= d <= hi and d in obs
                          and all(fc[d][m] is not None for m in mfe.MODELS))
            result[name][wname] = {"first": days[0] if days else None, "last": days[-1] if days else None,
                                   **{m: stats(fc, obs, days, m) for m in mfe.MODELS}}
            if wname.startswith("out"):
                result[name]["out_days"] = [{"day": d, "obs": obs[d], "icon": round(fc[d]["icon_seamless"], 1)}
                                            for d in days]
    print(json.dumps(result, indent=1))
    json.dump(result, open(ROOT + "/experiments/2026-10-26-P-0225/results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
