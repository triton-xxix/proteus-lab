#!/usr/bin/env python3
"""P-0379: does an SGP4 pass search on CelesTrak's Sentinel-2A elements find the same passes as brute force?

Over Munich, 7 days back from now. Truth is a 1-second scan. Compared: a 60-second scan (the "one
minute brute force" the harvest item named) and a coarse search (300 s steps, refine the peak by
golden section). Then the found passes are checked against real scenes in Earth Search's keyless
STAC catalogue: does a real Sentinel-2A acquisition sit at a predicted pass, how far off in time.
Own code; sgp4 is Brandon Rhodes's library from PyPI in sandbox/sgp4-lib.
"""
import json
import math
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/sgp4-lib")
import numpy as np  # noqa: E402
from sgp4.api import Satrec, SatrecArray, jday  # noqa: E402

HERE = Path(__file__).resolve().parent
LAT, LON = 48.137, 11.575
DAYS = 7
RE = 6371.0
CAT = "40697"


def fetch_tle():
    u = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={CAT}&FORMAT=TLE"
    with urllib.request.urlopen(u, timeout=30) as r:
        t = r.read().decode().splitlines()
    return t[1].strip(), t[2].strip()


def gmst(jd):
    d = jd - 2451545.0
    return np.deg2rad((280.46061837 + 360.98564736629 * d) % 360)


def obs_eci(lat, lon, jd):
    th = gmst(jd) + math.radians(lon)
    la = math.radians(lat)
    # WGS84 geocentric point
    a, f = 6378.137, 1 / 298.257223563
    e2 = f * (2 - f)
    N = a / math.sqrt(1 - e2 * math.sin(la) ** 2)
    r = N * math.cos(la)
    z = N * (1 - e2) * math.sin(la)
    return np.stack([r * np.cos(th), r * np.sin(th), np.full_like(th, z)], axis=-1)


def geometry(sat, jd0, seconds):
    """Elevation (deg) and great-circle ground distance to nadir (km) at offsets in seconds."""
    jd = np.full_like(seconds, jd0, dtype=float)
    fr = seconds / 86400.0
    e, r, _ = SatrecArray([sat]).sgp4(jd, fr)
    assert not e.any(), "sgp4 error"
    r = r[0]
    full = jd + fr
    o = obs_eci(LAT, LON, full)
    rho = r - o
    up = o / np.linalg.norm(o, axis=1, keepdims=True)
    el = np.degrees(np.arcsin(np.sum(rho * up, axis=1) / np.linalg.norm(rho, axis=1)))
    cosg = np.sum(r * o, axis=1) / (np.linalg.norm(r, axis=1) * np.linalg.norm(o, axis=1))
    dist = RE * np.arccos(np.clip(cosg, -1, 1))
    return el, dist


def peaks_scan(sat, jd0, total, step, thresh):
    s = np.arange(0, total + step, step, dtype=float)
    el, dist = geometry(sat, jd0, s)
    out = []
    above = el > thresh
    i = 0
    while i < len(s):
        if above[i]:
            j = i
            while j + 1 < len(s) and above[j + 1]:
                j += 1
            k = i + int(np.argmax(el[i:j + 1]))
            out.append((float(s[k]), float(el[k]), float(dist[k])))
            i = j + 1
        else:
            i += 1
    return out


def golden(sat, jd0, a, b):
    g = (math.sqrt(5) - 1) / 2
    f = lambda x: float(geometry(sat, jd0, np.array([x], dtype=float))[0][0])
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(30):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
    m = (a + b) / 2
    return m, f(m)


def peaks_coarse(sat, jd0, total, step, thresh):
    s = np.arange(0, total + step, step, dtype=float)
    el, _ = geometry(sat, jd0, s)
    out = []
    for i in range(1, len(s) - 1):
        if el[i] >= el[i - 1] and el[i] >= el[i + 1] and el[i] > thresh - 30:
            m, v = golden(sat, jd0, s[i - 1], s[i + 1])
            if v > thresh:
                dist = float(geometry(sat, jd0, np.array([m], dtype=float))[1][0])
                out.append((m, v, dist))
    return out


def match(truth, found, tol=120):
    hit, used = 0, set()
    errs = []
    for t in truth:
        best = None
        for j, f in enumerate(found):
            if j in used:
                continue
            d = abs(f[0] - t[0])
            if d <= tol and (best is None or d < best[0]):
                best = (d, j)
        if best:
            hit += 1
            used.add(best[1])
            errs.append(best[0])
    return hit, len(found) - len(used), errs


def stac(start, end):
    body = {"collections": ["sentinel-2-l2a"], "intersects": {"type": "Point", "coordinates": [LON, LAT]},
            "datetime": f"{start}/{end}", "limit": 100}
    req = urllib.request.Request("https://earth-search.aws.element84.com/v1/search",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["features"]


def main():
    l1, l2 = fetch_tle()
    sat = Satrec.twoline2rv(l1, l2)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    start = now - timedelta(days=DAYS)
    jd, fr = jday(start.year, start.month, start.day, start.hour, start.minute, start.second)
    jd0 = jd + fr
    total = DAYS * 86400
    res = {"tle": [l1, l2], "start": start.isoformat(), "end": now.isoformat(), "point": [LAT, LON], "thresholds": {}}

    for thresh in (0, 10, 45):
        t0 = time.perf_counter()
        truth = peaks_scan(sat, jd0, total, 1, thresh)
        t1 = time.perf_counter()
        minute = peaks_scan(sat, jd0, total, 60, thresh)
        t2 = time.perf_counter()
        coarse = peaks_coarse(sat, jd0, total, 300, thresh)
        t3 = time.perf_counter()
        hm, xm, em = match(truth, minute)
        hc, xc, ec = match(truth, coarse)
        res["thresholds"][thresh] = {
            "truth_passes": len(truth), "minute_passes": len(minute), "minute_hit": hm, "minute_extra": xm,
            "coarse_passes": len(coarse), "coarse_hit": hc, "coarse_extra": xc,
            "coarse_peak_err_s_max": round(max(ec), 2) if ec else None,
            "truth_secs": round(t1 - t0, 3), "minute_secs": round(t2 - t1, 3), "coarse_secs": round(t3 - t2, 3)}
        print(thresh, res["thresholds"][thresh])

    # Real scenes
    feats = stac(start.strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ"))
    a = [f for f in feats if "2a" in str(f["properties"].get("platform", "")).lower()]
    truth = peaks_scan(sat, jd0, total, 1, 0)
    rows = []
    for f in a:
        dt = datetime.fromisoformat(f["properties"]["datetime"].replace("Z", "+00:00"))
        sec = (dt - start).total_seconds()
        n = min(truth, key=lambda t: abs(t[0] - sec))
        rows.append({"scene": f["id"], "time": f["properties"]["datetime"],
                     "offset_s": round(sec - n[0], 1), "peak_el": round(n[1], 1), "nadir_km": round(n[2], 0)})
    rows.sort(key=lambda r: r["time"])
    res["stac_total_features"] = len(feats)
    res["sentinel_2a_scenes"] = rows
    if rows:
        o = [abs(r["offset_s"]) for r in rows]
        res["scene_offset_abs_s"] = {"n": len(o), "median": float(np.median(o)), "max": float(max(o))}
        d = [r["nadir_km"] for r in rows]
        res["scene_nadir_km"] = {"max": max(d), "swath_half_km": 145}
    # Passes the swath should have covered with no scene: nadir within 145 km
    swath = [t for t in truth if t[2] <= 145]
    res["model_swath_passes"] = len(swath)
    secs = []
    for r in rows:
        dt = datetime.fromisoformat(r["time"].replace("Z", "+00:00"))
        secs.append((dt - start).total_seconds())
    res["model_swath_passes_with_scene"] = sum(1 for t in swath if any(abs(t[0] - s) < 900 for s in secs))
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    print("stac", len(feats), "s2a", len(rows), res.get("scene_offset_abs_s"), res.get("scene_nadir_km"))
    print("swath passes", res["model_swath_passes"], "with scene", res["model_swath_passes_with_scene"])
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
