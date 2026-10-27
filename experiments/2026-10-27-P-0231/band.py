"""P-0231: is the ICON-EPS member band for Munich's daily high wide enough to hold the DWD Stadt high?

Open-Meteo ensemble API, icon_seamless, daily temperature_2m_max for 39 members, past_days 14 (only
the last few come back non-null). DWD observed highs from the 13 Oct script's fetcher (station 03379,
TXK). Band = 10th to 90th percentile of the members.
"""
import importlib.util
import json
import urllib.request

ROOT = "/Users/triton/PROTEUS"
OUT = ROOT + "/experiments/2026-10-27-P-0231"
spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)

URL = ("https://ensemble-api.open-meteo.com/v1/ensemble?latitude=48.14&longitude=11.58"
       "&daily=temperature_2m_max&models=icon_seamless&past_days=14&forecast_days=1"
       "&timezone=Europe%2FBerlin")
MAE_P0225 = 1.28


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def main():
    raw = json.load(urllib.request.urlopen(URL, timeout=30))
    json.dump(raw, open(OUT + "/ensemble_raw.json", "w"))
    daily = raw["daily"]
    keys = [k for k in daily if k.startswith("temperature_2m_max_member")]
    obs = mfe.observed("10865")  # WMO id; the fetcher maps it to DWD 03379 Stadt
    rows = []
    for i, day in enumerate(daily["time"]):
        members = [daily[k][i] for k in keys if daily[k][i] is not None]
        if len(members) < 30:
            continue
        p10, p90 = pct(members, 0.1), pct(members, 0.9)
        o = obs.get(day)
        rows.append({"day": day, "n_members": len(members), "control": daily["temperature_2m_max"][i],
                     "p10": round(p10, 2), "p90": round(p90, 2), "width": round(p90 - p10, 2),
                     "min": min(members), "max": max(members), "obs_stadt": o,
                     "inside": None if o is None else p10 <= o <= p90,
                     "inside_min_max": None if o is None else min(members) <= o <= max(members)})
    scored = [r for r in rows if r["obs_stadt"] is not None]
    summary = {"days_with_members": len(rows), "days_scored": len(scored),
               "inside_10_90": sum(r["inside"] for r in scored),
               "inside_min_max": sum(r["inside_min_max"] for r in scored),
               "mean_width_scored": round(sum(r["width"] for r in scored) / len(scored), 2) if scored else None,
               "mean_width_all": round(sum(r["width"] for r in rows) / len(rows), 2) if rows else None,
               "mae_p0225": MAE_P0225}
    result = {"summary": summary, "rows": rows}
    print(json.dumps(result, indent=1))
    json.dump(result, open(OUT + "/results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
