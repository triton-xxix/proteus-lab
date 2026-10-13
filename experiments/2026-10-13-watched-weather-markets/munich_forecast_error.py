#!/usr/bin/env python3
"""How wrong is tomorrow's Munich high? Day-ahead forecasts v DWD station observations.

Forecasts: Open-Meteo previous-runs API, temperature_2m_max as issued one day before
(ICON, ECMWF IFS 0.25, GFS). Observations: Meteostat bulk daily CSV (DWD stations, keyless):
10865 Muenchen-Stadt, 10870 Muenchen-Flughafen. Prints per-model error stats for each station,
and the share of days the whole-degree forecast equals the whole-degree observed max.
Usage: munich_forecast_error.py [--days 60] [--out result.json]
"""
import csv
import gzip
import io
import json
import math
import sys
import urllib.request

LAT, LON = 48.137, 11.575
STATIONS = {"10865": "Muenchen-Stadt", "10870": "Muenchen-Flughafen"}
MODELS = ["icon_seamless", "ecmwf_ifs025", "gfs_seamless"]
UA = {"User-Agent": "proteus-nightly/1.0 (research; contact via github triton-xxix)"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def forecasts(days):
    # The previous-runs API only serves hourly variables, so take the daily max of the hourly
    # temperature as issued one day earlier (local days, Europe/Berlin).
    url = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s"
           "&hourly=temperature_2m_previous_day1&models=%s&past_days=%d&forecast_days=1"
           "&timezone=Europe%%2FBerlin" % (LAT, LON, ",".join(MODELS), days))
    h = json.loads(get(url))["hourly"]
    out = {}
    for i, ts in enumerate(h["time"]):
        day = ts[:10]
        row = out.setdefault(day, {m: None for m in MODELS})
        for m in MODELS:
            v = h.get("temperature_2m_previous_day1_" + m, [None] * len(h["time"]))[i]
            if v is not None and (row[m] is None or v > row[m]):
                row[m] = v
    return out


def observed_meteostat(station):
    url = "https://bulk.meteostat.net/v2/daily/%s.csv.gz" % station
    raw = gzip.decompress(get(url, binary=True)).decode("utf-8")
    # meteostat daily columns: date,tavg,tmin,tmax,prcp,snow,wdir,wspd,wpgt,pres,tsun
    out = {}
    for row in csv.reader(io.StringIO(raw)):
        if len(row) > 3 and row[3] not in ("", None):
            out[row[0]] = float(row[3])
    return out


DWD_IDS = {"10865": "03379", "10870": "01262"}  # WMO id -> DWD station id


def observed_dwd(station):
    """DWD open data, recent daily climate file (last ~500 days), TXK = daily max in C."""
    import zipfile
    sid = DWD_IDS[station]
    url = ("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/"
           "recent/tageswerte_KL_%s_akt.zip" % sid)
    blob = get(url, binary=True)
    out = {}
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        name = [n for n in z.namelist() if n.startswith("produkt_klima_tag")][0]
        text = z.read(name).decode("latin-1")
    header = None
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(";")]
        if header is None:
            header = parts
            continue
        if len(parts) < len(header):
            continue
        row = dict(zip(header, parts))
        txk = row.get("TXK")
        if txk in (None, "", "-999"):
            continue
        d = row["MESS_DATUM"]
        out["%s-%s-%s" % (d[:4], d[4:6], d[6:8])] = float(txk)
    return out


def observed(station):
    try:
        obs = observed_dwd(station)
        src = "dwd"
    except Exception as e:  # noqa: BLE001
        print("  dwd fetch failed for %s (%s), using meteostat" % (station, type(e).__name__))
        obs = observed_meteostat(station)
        src = "meteostat"
    print("  observations for %s from %s, %d days, last %s" % (station, src, len(obs),
          sorted(obs)[-1] if obs else "?"))
    return obs


def rnd(x):
    return int(math.floor(x + 0.5))


def main():
    args = sys.argv[1:]
    days = 60
    outpath = None
    if "--days" in args:
        days = int(args[args.index("--days") + 1])
    if "--out" in args:
        outpath = args[args.index("--out") + 1]
    fc = forecasts(days)
    result = {"days_requested": days, "stations": {}}
    for sid, name in STATIONS.items():
        obs = observed(sid)
        common = sorted(d for d in fc if d in obs and all(fc[d][m] is not None for m in MODELS))
        stats = {}
        for m in MODELS:
            errs = [fc[d][m] - obs[d] for d in common]
            hit = sum(1 for d in common if rnd(fc[d][m]) == rnd(obs[d]))
            within1 = sum(1 for d in common if abs(rnd(fc[d][m]) - rnd(obs[d])) <= 1)
            n = len(common)
            stats[m] = {
                "n": n,
                "mae": round(sum(abs(e) for e in errs) / n, 2) if n else None,
                "bias": round(sum(errs) / n, 2) if n else None,
                "right_degree": round(hit / n, 2) if n else None,
                "within_1": round(within1 / n, 2) if n else None,
            }
        # three-model mean
        errs = [sum(fc[d][m] for m in MODELS) / 3 - obs[d] for d in common]
        hit = sum(1 for d in common if rnd(sum(fc[d][m] for m in MODELS) / 3) == rnd(obs[d]))
        within1 = sum(1 for d in common if abs(rnd(sum(fc[d][m] for m in MODELS) / 3) - rnd(obs[d])) <= 1)
        n = len(common)
        stats["mean_of_3"] = {
            "n": n,
            "mae": round(sum(abs(e) for e in errs) / n, 2) if n else None,
            "bias": round(sum(errs) / n, 2) if n else None,
            "right_degree": round(hit / n, 2) if n else None,
            "within_1": round(within1 / n, 2) if n else None,
        }
        last_obs = sorted(obs)[-1]
        result["stations"][sid] = {"name": name, "first": common[0] if common else None,
                                   "last": common[-1] if common else None,
                                   "last_observed_day": last_obs, "stats": stats,
                                   "recent": [{"day": d, "obs": obs[d],
                                               **{m: fc[d][m] for m in MODELS}} for d in common[-7:]]}
        print("%s %s: %d days %s to %s (station data to %s)" % (sid, name, n,
              common[0] if common else "?", common[-1] if common else "?", last_obs))
        for m, s in stats.items():
            if not n:
                break
            print("  %-13s mae %.2f bias %+.2f right degree %.0f%% within 1 %.0f%%" % (
                m, s["mae"], s["bias"], 100 * s["right_degree"], 100 * s["within_1"]))
    if outpath:
        with open(outpath, "w") as f:
            json.dump(result, f, indent=1)


if __name__ == "__main__":
    main()
