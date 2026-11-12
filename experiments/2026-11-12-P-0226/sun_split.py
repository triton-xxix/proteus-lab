"""P-0226: Munich ICON day-ahead bias, 30 days out of sample, split by sunshine.

Same fetchers as the 13 Oct script (Open-Meteo previous-runs, hourly temperature issued one day
before, daily max per Berlin day; DWD recent daily KL, TXK). Adds SDK (sunshine hours) from the same
DWD file. Thresholds fixed before the data was looked at: sunny = SDK >= 5 h, dull = SDK <= 1 h.
Writes results.json beside this file; does not touch the P-0225 folder.
"""
import importlib.util
import io
import json
import zipfile

ROOT = "/Users/triton/PROTEUS"
OUT = ROOT + "/experiments/2026-11-12-P-0226/results.json"
spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)

WINDOWS = {"in_sample_15aug_12oct": ("2026-08-15", "2026-10-12"),
           "p0225_13_25oct": ("2026-10-13", "2026-10-25"),
           "new_26oct_11nov": ("2026-10-26", "2026-11-11"),
           "out_of_sample_13oct_11nov": ("2026-10-13", "2026-11-11")}
SUNNY, DULL = 5.0, 1.0
CORRECTIONS = [0.0, 0.25, 0.5, 0.75, 1.0]


def dwd_daily(station):
    """TXK and SDK per day from the DWD recent daily KL file."""
    sid = mfe.DWD_IDS[station]
    url = ("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/"
           "recent/tageswerte_KL_%s_akt.zip" % sid)
    blob = mfe.get(url, binary=True)
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        name = [n for n in z.namelist() if n.startswith("produkt_klima_tag")][0]
        text = z.read(name).decode("latin-1")
    header, txk, sdk = None, {}, {}
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(";")]
        if header is None:
            header = parts
            continue
        if len(parts) < len(header):
            continue
        row = dict(zip(header, parts))
        d = row["MESS_DATUM"]
        day = "%s-%s-%s" % (d[:4], d[4:6], d[6:8])
        if row.get("TXK") not in (None, "", "-999"):
            txk[day] = float(row["TXK"])
        if row.get("SDK") not in (None, "", "-999"):
            sdk[day] = float(row["SDK"])
    return txk, sdk


def stats(errs):
    n = len(errs)
    if not n:
        return {"n": 0}
    mean = sum(errs) / n
    sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5 if n > 1 else None
    out = {"n": n, "bias": round(mean, 2), "se": round(sd / n ** 0.5, 2) if sd else None}
    for c in CORRECTIONS:
        out["mae_plus_%s" % c] = round(sum(abs(e + c) for e in errs) / n, 3)
    return out


def slope(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if not sxx:
        return None
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    res = [y - a - b * x for x, y in zip(xs, ys)]
    se = (sum(r * r for r in res) / (n - 2) / sxx) ** 0.5
    syy = sum((y - my) ** 2 for y in ys)
    r = (b * sxx / (sxx * syy) ** 0.5) if syy else None
    return {"per_sun_hour": round(b, 3), "se": round(se, 3), "intercept": round(a, 2),
            "r": round(r, 2) if r is not None else None, "n": n}


def main():
    fc = mfe.forecasts(92)
    data = {sid: dwd_daily(sid) for sid in mfe.STATIONS}
    sun_src = {}
    result = {"thresholds": {"sunny_sdk_ge": SUNNY, "dull_sdk_le": DULL}, "stations": {}}
    for sid, name in mfe.STATIONS.items():
        txk, sdk = data[sid]
        if len([d for d in sdk if d >= "2026-08-15"]) < 30:
            other = [s for s in mfe.STATIONS if s != sid][0]
            sdk = data[other][1]
            sun_src[name] = "SDK borrowed from " + mfe.STATIONS[other]
        else:
            sun_src[name] = "own SDK"
        st = {"sunshine_source": sun_src[name], "last_observed_day": sorted(txk)[-1]}
        for wname, (lo, hi) in WINDOWS.items():
            days = sorted(d for d in fc if lo <= d <= hi and d in txk
                          and fc[d]["icon_seamless"] is not None)
            err = {d: fc[d]["icon_seamless"] - txk[d] for d in days}
            w = {"first": days[0] if days else None, "last": days[-1] if days else None,
                 "all": stats([err[d] for d in days])}
            have = [d for d in days if d in sdk]
            w["sunny"] = stats([err[d] for d in have if sdk[d] >= SUNNY])
            w["middle"] = stats([err[d] for d in have if DULL < sdk[d] < SUNNY])
            w["dull"] = stats([err[d] for d in have if sdk[d] <= DULL])
            w["error_on_sunshine"] = slope([sdk[d] for d in have], [err[d] for d in have])
            # sunshine-aware correction, fitted on the in-sample window only (set below)
            st[wname] = w
            if wname.startswith("out"):
                st["out_days"] = [{"day": d, "obs": txk[d], "icon": round(fc[d]["icon_seamless"], 1),
                                   "err": round(err[d], 1), "sdk": sdk.get(d)} for d in days]
        # in-sample fit applied out of sample: correction = -(a + b * sdk)
        fit = st["in_sample_15aug_12oct"]["error_on_sunshine"]
        if fit:
            lo, hi = WINDOWS["out_of_sample_13oct_11nov"]
            days = [d for d in sorted(fc) if lo <= d <= hi and d in txk and d in sdk
                    and fc[d]["icon_seamless"] is not None]
            e2 = [fc[d]["icon_seamless"] - txk[d] - (fit["intercept"] + fit["per_sun_hour"] * sdk[d])
                  for d in days]
            st["out_of_sample_with_in_sample_sun_fit"] = {
                "n": len(e2), "mae": round(sum(abs(e) for e in e2) / len(e2), 3) if e2 else None,
                "note": "needs the day's sunshine, which is not known at forecast time; an upper bound"}
        result["stations"][name] = st
    print(json.dumps(result, indent=1))
    json.dump(result, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
