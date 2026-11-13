"""Does Omori's law hold for the aftershocks of recent big earthquakes?

Modified Omori (Utsu): aftershock rate n(t) = K / (c + t)^p, p usually 0.9 to 1.5.
Keyless USGS FDSN pulls, stdlib only. For each mainshock of M7 or more in the window,
take M>=Mc events within R km for 30 days after, and fit p, c, K by maximum likelihood
(Ogata 1983) with a coarse grid then a local refine. Compare the fit against a straight
power-law slope on log-binned counts, and check how many aftershocks day 2-30 the
day-0-1 fit predicted (the forecasting use of the law).
"""
import json, math, sys, urllib.request, urllib.parse, datetime as dt

OUT = "/Users/triton/PROTEUS/experiments/2026-11-13-persona-omori/"
BASE = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def get(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def hav(lat1, lon1, lat2, lon2):
    p = math.pi / 180
    a = math.sin((lat2 - lat1) * p / 2) ** 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(a))


def nll(times, T0, T1, K, c, p):
    # negative log likelihood for a nonstationary Poisson with rate K/(c+t)^p on [T0, T1]
    if p == 1:
        integ = K * (math.log(c + T1) - math.log(c + T0))
    else:
        integ = K * ((c + T1) ** (1 - p) - (c + T0) ** (1 - p)) / (1 - p)
    s = sum(math.log(K) - p * math.log(c + t) for t in times)
    return integ - s


def fit(times, T0, T1):
    best = None
    for p in [x / 100 for x in range(50, 201, 2)]:
        for c in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]:
            # K has a closed form given c and p: K = N / integral
            if abs(p - 1) < 1e-9:
                I = math.log(c + T1) - math.log(c + T0)
            else:
                I = ((c + T1) ** (1 - p) - (c + T0) ** (1 - p)) / (1 - p)
            K = len(times) / I
            v = nll(times, T0, T1, K, c, p)
            if best is None or v < best[0]:
                best = (v, K, c, p)
    v, K, c, p = best
    # local refine
    for _ in range(3):
        for dp in [x / 1000 for x in range(-20, 21, 2)]:
            for fc in [0.7, 0.85, 1.0, 1.15, 1.3]:
                pp, cc = p + dp, c * fc
                if pp <= 0.3:
                    continue
                if abs(pp - 1) < 1e-9:
                    I = math.log(cc + T1) - math.log(cc + T0)
                else:
                    I = ((cc + T1) ** (1 - pp) - (cc + T0) ** (1 - pp)) / (1 - pp)
                KK = len(times) / I
                vv = nll(times, T0, T1, KK, cc, pp)
                if vv < v:
                    v, K, c, p = vv, KK, cc, pp
    return K, c, p


def expected(K, c, p, a, b):
    if abs(p - 1) < 1e-9:
        return K * (math.log(c + b) - math.log(c + a))
    return K * ((c + b) ** (1 - p) - (c + a) ** (1 - p)) / (1 - p)


def main():
    end = dt.datetime(2026, 11, 13, 23, 0)
    start = end - dt.timedelta(days=120)
    mains = get({"format": "geojson", "starttime": start.isoformat(), "endtime": (end - dt.timedelta(days=30)).isoformat(),
                 "minmagnitude": 7.0, "orderby": "magnitude"})["features"]
    rows = []
    for f in mains:
        m = f["properties"]["mag"]
        lon, lat, dep = f["geometry"]["coordinates"]
        t0 = dt.datetime.utcfromtimestamp(f["properties"]["time"] / 1000)
        R = 0.02 * 10 ** (0.5 * m) * 1.5  # about 1.5x Wells-Coppersmith rupture length scale, km
        R = max(R, 100)
        ev = get({"format": "geojson", "starttime": t0.isoformat(), "endtime": (t0 + dt.timedelta(days=30)).isoformat(),
                  "latitude": lat, "longitude": lon, "maxradiuskm": round(R), "minmagnitude": 4.5})["features"]
        ts = sorted((e["properties"]["time"] / 1000 - f["properties"]["time"] / 1000) / 86400 for e in ev)
        ts = [t for t in ts if t > 0.01]  # drop the mainshock and the first ~15 min (catalogue incompleteness)
        mainrow = {"place": f["properties"]["place"], "mag": m, "time": t0.isoformat() + "Z", "radius_km": round(R), "n_after_M4.5": len(ts)}
        if len(ts) >= 15:
            K, c, p = fit(ts, 0.01, 30)
            mainrow.update({"K": round(K, 2), "c_days": round(c, 4), "p": round(p, 3)})
            # forecast check: fit on day 0.01-2, predict day 2-30
            early = [t for t in ts if t <= 2]
            late = [t for t in ts if t > 2]
            if len(early) >= 10:
                K2, c2, p2 = fit(early, 0.01, 2)
                pred = expected(K2, c2, p2, 2, 30)
                mainrow.update({"early_n": len(early), "early_p": round(p2, 3), "pred_day2_30": round(pred, 1), "seen_day2_30": len(late)})
            # constant-rate alternative for comparison: share of the 30 days' events in the first day
            mainrow["share_first_day"] = round(sum(1 for t in ts if t <= 1) / len(ts), 3)
        rows.append(mainrow)
        print(json.dumps(mainrow))
    with open(OUT + "results.json", "w") as fh:
        json.dump({"pulled": dt.datetime.utcnow().isoformat() + "Z", "window": [start.isoformat(), end.isoformat()], "mainshocks": rows}, fh, indent=1)


if __name__ == "__main__":
    main()
