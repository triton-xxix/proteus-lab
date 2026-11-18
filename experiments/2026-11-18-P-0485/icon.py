"""P-0485: ICON's lead-1 day-high error at the two stations Polymarket's London and Paris markets
settle on (EGLC, LFPB), 1 to 17 Nov 2026, split by P-0446's low-cloud flag, beside the market's own
error on the same days from P-0484.

Truth = the degree bucket the market resolved to (P-0484 results.json), so model and market are
scored against one number. The METAR day high (UTC, tenths) is kept as a cross-check. Forecast =
Open-Meteo previous-runs icon_seamless lead-1 hourly maximum at the airport point, UTC day, 23+ hours.
Error = truth minus forecast (negative = forecast warm). Keyless.

    python3 -I experiments/2026-11-18-P-0485/icon.py
"""
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
MARKET = json.loads(pathlib.Path("/Users/triton/PROTEUS/experiments/2026-11-18-P-0484/results.json").read_text())
STATIONS = {"london": ("EGLC", 51.5053, 0.0553), "paris": ("LFPB", 48.9694, 2.4414)}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=240).read()


def metar_high(st):
    u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=%s&data=tmpc"
         "&year1=2026&month1=11&day1=1&year2=2026&month2=11&day2=18&tz=UTC&format=onlycomma&latlon=no"
         "&missing=empty&trace=empty&report_type=3&report_type=4" % st)
    lines = get(u).decode("latin-1").splitlines()
    hdr = lines[0].split(",")
    temps = defaultdict(list)
    for line in lines[1:]:
        p = dict(zip(hdr, line.split(",")))
        if p.get("tmpc") and len(p.get("valid", "")) >= 13:
            try:
                temps[p["valid"][:10]].append(float(p["tmpc"]))
            except ValueError:
                pass
    return {d: (max(v), len(v)) for d, v in temps.items()}


def lead1(lat, lon):
    h = json.loads(get("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=%.4f&longitude=%.4f"
                       "&hourly=temperature_2m_previous_day1&start_date=2026-11-01&end_date=2026-11-17"
                       "&timezone=UTC&models=icon_seamless" % (lat, lon)))["hourly"]
    key = next(k for k in h if k.startswith("temperature_2m_previous_day1"))
    m = defaultdict(list)
    for t, v in zip(h["time"], h[key]):
        if v is not None:
            m[t[:10]].append(v)
    return {k: max(v) for k, v in m.items() if len(v) >= 23}


def mean(x):
    return round(sum(x) / len(x), 3) if x else None


out = {}
for city, (st, lat, lon) in STATIONS.items():
    mh = metar_high(st)
    time.sleep(2)
    fc = lead1(lat, lon)
    time.sleep(2)
    rows = []
    for r in MARKET[city]["rows"]:
        d = r["date"]
        if "err" not in r or d not in fc:
            continue
        hi, n = mh.get(d, (None, 0))
        rows.append({"date": d, "low": r["low"], "truth_bucket": r["truth"], "metar_high": hi, "metars": n,
                     "icon_lead1": round(fc[d], 2), "icon_err": round(r["truth"] - fc[d], 2),
                     "market_err": r["err"], "icon_degree_hit": round(fc[d] + 1e-9) == r["truth"],
                     "market_fav_hit": r["fav_hit"]})
    a = [r for r in rows if r["low"]]
    b = [r for r in rows if not r["low"]]
    out[city] = {
        "station": st, "days": len(rows), "low_n": len(a),
        "icon": {"mean_err": mean([r["icon_err"] for r in rows]), "mean_abs_err": mean([abs(r["icon_err"]) for r in rows]),
                 "low_mean_err": mean([r["icon_err"] for r in a]), "other_mean_err": mean([r["icon_err"] for r in b]),
                 "gap": round(mean([r["icon_err"] for r in a]) - mean([r["icon_err"] for r in b]), 3) if a and b else None,
                 "rounded_degree_hit": sum(r["icon_degree_hit"] for r in rows)},
        "market_09z": {"mean_err": mean([r["market_err"] for r in rows]), "mean_abs_err": mean([abs(r["market_err"]) for r in rows]),
                       "low_mean_err": mean([r["market_err"] for r in a]), "other_mean_err": mean([r["market_err"] for r in b]),
                       "gap": round(mean([r["market_err"] for r in a]) - mean([r["market_err"] for r in b]), 3) if a and b else None,
                       "fav_hit": sum(r["market_fav_hit"] for r in rows)},
        "bucket_v_metar_high_max_diff": max((abs(r["truth_bucket"] - r["metar_high"]) for r in rows if r["metar_high"] is not None), default=None),
        "rows": rows,
    }
    print(json.dumps({k: v for k, v in out[city].items() if k != "rows"}, indent=1))
(HERE / "results.json").write_text(json.dumps(out, indent=1))
