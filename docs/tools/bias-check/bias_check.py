#!/usr/bin/env python3
"""Does a weather model's bias hold after you measured it? Day-ahead daily highs v observations.

Forecasts: Open-Meteo previous-runs API (keyless), hourly temperature_2m as issued one day before,
daily max per local day, for each model asked for. Observations, pick one:
  --dwd 03379        DWD open data, recent daily climate file (TXK), German stations
  --meteostat 10865  Meteostat bulk daily CSV (tmax), stations worldwide
  --csv obs.csv      your own file with a date column and a tmax column
The days are split at --split. Before the split the bias is learned; after it the script reports
the bias again, and the MAE raw, after subtracting the learned bias, and after any --correct value.
Standard library only.

  python3 bias_check.py --lat 48.137 --lon 11.575 --dwd 03379 --start 2026-08-15 --split 2026-10-13
  python3 bias_check.py --lat 51.48 --lon -0.45 --meteostat 03772 --split 2026-10-01 --json out.json
"""
import argparse
import csv
import gzip
import io
import json
import math
import sys
import urllib.parse
import urllib.request
import zipfile

UA = {"User-Agent": "proteus-bias-check/1.0 (github triton-xxix)"}
MODELS = "icon_seamless,ecmwf_ifs025,gfs_seamless"


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def forecasts(lat, lon, models, days, tz):
    q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "hourly": "temperature_2m_previous_day1",
                                "models": ",".join(models), "past_days": days, "forecast_days": 1,
                                "timezone": tz})
    h = json.loads(get("https://previous-runs-api.open-meteo.com/v1/forecast?" + q))["hourly"]
    out = {}
    for i, ts in enumerate(h["time"]):
        row = out.setdefault(ts[:10], {m: None for m in models})
        for m in models:
            key = "temperature_2m_previous_day1" + ("_" + m if len(models) > 1 else "")
            v = h.get(key, [None] * len(h["time"]))[i]
            if v is not None and (row[m] is None or v > row[m]):
                row[m] = v
    return out


def obs_dwd(sid):
    url = ("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/"
           "recent/tageswerte_KL_%s_akt.zip" % sid)
    with zipfile.ZipFile(io.BytesIO(get(url))) as z:
        name = [n for n in z.namelist() if n.startswith("produkt_klima_tag")][0]
        text = z.read(name).decode("latin-1")
    out, header = {}, None
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(";")]
        if header is None:
            header = parts
            continue
        row = dict(zip(header, parts))
        if row.get("TXK") not in (None, "", "-999"):
            d = row["MESS_DATUM"]
            out["%s-%s-%s" % (d[:4], d[4:6], d[6:8])] = float(row["TXK"])
    return out


def obs_meteostat(wmo):
    raw = gzip.decompress(get("https://bulk.meteostat.net/v2/daily/%s.csv.gz" % wmo)).decode("utf-8")
    return {r[0]: float(r[3]) for r in csv.reader(io.StringIO(raw)) if len(r) > 3 and r[3]}


def obs_csv(path):
    rows = list(csv.DictReader(open(path, newline="")))
    keys = {k.lower(): k for k in rows[0]}
    dk, tk = keys.get("date"), keys.get("tmax")
    if not dk or not tk:
        sys.exit("csv needs a date column and a tmax column")
    return {r[dk][:10]: float(r[tk]) for r in rows if r[tk] not in ("", None)}


def stats(errs, shift=0.0):
    n = len(errs)
    if not n:
        return {"n": 0}
    mean = sum(errs) / n
    sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return {"n": n, "bias": round(mean, 2), "se": round(sd / math.sqrt(n), 2),
            "mae": round(sum(abs(e + shift) for e in errs) / n, 2)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--tz", default="auto")
    ap.add_argument("--models", default=MODELS)
    ap.add_argument("--days", type=int, default=80, help="past days of forecasts to fetch (Open-Meteo caps it)")
    ap.add_argument("--start", help="first day to use, YYYY-MM-DD")
    ap.add_argument("--split", required=True, help="first day after the bias was learned, YYYY-MM-DD")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--dwd")
    src.add_argument("--meteostat")
    src.add_argument("--csv")
    ap.add_argument("--correct", type=float, help="a fixed correction to test too, in degrees added")
    ap.add_argument("--json", help="write the result here")
    a = ap.parse_args()
    models = a.models.split(",")
    fc = forecasts(a.lat, a.lon, models, a.days, a.tz)
    obs = obs_dwd(a.dwd) if a.dwd else obs_meteostat(a.meteostat) if a.meteostat else obs_csv(a.csv)
    days = sorted(d for d in fc if d in obs and (not a.start or d >= a.start)
                  and all(fc[d][m] is not None for m in models))
    before = [d for d in days if d < a.split]
    after = [d for d in days if d >= a.split]
    if not before or not after:
        sys.exit("need days on both sides of the split: %d before, %d after" % (len(before), len(after)))
    res = {"lat": a.lat, "lon": a.lon, "source": "dwd %s" % a.dwd if a.dwd else "meteostat %s" % a.meteostat
           if a.meteostat else "csv", "split": a.split, "before": [before[0], before[-1]],
           "after": [after[0], after[-1]], "models": {},
           "days": [{"day": d, "obs": obs[d], **{m: round(fc[d][m], 1) for m in models}} for d in days]}
    print("%s, %d days before %s (%s to %s), %d after (to %s)" % (res["source"], len(before), a.split,
          before[0], before[-1], len(after), after[-1]))
    for m in models:
        eb = [fc[d][m] - obs[d] for d in before]
        ea = [fc[d][m] - obs[d] for d in after]
        sb, sa = stats(eb), stats(ea)
        learned = -sb["bias"]
        r = {"before": sb, "after": sa, "learned_correction": round(learned, 2),
             "after_mae_learned": stats(ea, learned)["mae"]}
        if a.correct is not None:
            r["after_mae_fixed"] = stats(ea, a.correct)["mae"]
        verdict = "helps" if r["after_mae_learned"] < sa["mae"] else "hurts"
        r["verdict"] = verdict
        res["models"][m] = r
        print("  %-14s bias before %+.2f (se %.2f), after %+.2f (se %.2f); MAE after raw %.2f, "
              "learned %+.2f %s it: %.2f%s" % (m, sb["bias"], sb["se"], sa["bias"], sa["se"], sa["mae"],
              learned, verdict, r["after_mae_learned"],
              ", fixed %+.2f: %.2f" % (a.correct, r["after_mae_fixed"]) if a.correct is not None else ""))
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
