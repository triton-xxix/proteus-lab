"""P-0385 (number from the GO line): predicted swath passes against real Sentinel-2 scenes, 12 cities, 7 days.

For each of Sentinel-2A, 2B and 2C (CelesTrak elements), at 5 s steps, a pass is a local minimum of ground distance to nadir within 145 km.
Direction from the sign of the satellite's z velocity at that moment. Scenes from Earth Search over the same point; a pass counts as imaged if a
scene of that platform has a datetime within 15 minutes of it. Own code, the sgp4 library in sandbox/sgp4-lib.
"""
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/sgp4-lib")
import numpy as np  # noqa: E402
from sgp4.api import Satrec, SatrecArray, jday  # noqa: E402

HERE = pathlib.Path(__file__).parent
SATS = {"sentinel-2a": 40697, "sentinel-2b": 42063, "sentinel-2c": 60989}
CITIES = {"Munich": (48.137, 11.575), "London": (51.507, -0.128), "Madrid": (40.417, -3.704), "Oslo": (59.914, 10.752),
          "Cairo": (30.044, 31.236), "Nairobi": (-1.292, 36.822), "Delhi": (28.614, 77.209), "Tokyo": (35.676, 139.650),
          "Sydney": (-33.869, 151.209), "Sao Paulo": (-23.551, -46.633), "Mexico City": (19.433, -99.133), "Chicago": (41.878, -87.630)}
RE = 6371.0
UA = {"User-Agent": "proteus-research/1.0"}


def tle(cat):
    u = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={cat}&FORMAT=TLE"
    t = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode().splitlines()
    return t[1].strip(), t[2].strip()


def gmst(jd):
    d = jd - 2451545.0
    return np.deg2rad((280.46061837 + 360.98564736629 * d) % 360)


def obs_unit(lat, lon, jd):
    th = gmst(jd) + np.radians(lon)
    la = np.radians(lat)
    return np.stack([np.cos(la) * np.cos(th), np.cos(la) * np.sin(th), np.full_like(th, np.sin(la))], axis=-1)


def passes(sat, jd0, total, lat, lon):
    s = np.arange(0, total, 5.0)
    e, r, v = SatrecArray([sat]).sgp4(np.full_like(s, jd0), s / 86400)
    assert not e.any()
    r, v = r[0], v[0]
    o = obs_unit(lat, lon, jd0 + s / 86400)
    ru = r / np.linalg.norm(r, axis=1, keepdims=True)
    dist = RE * np.arccos(np.clip(np.sum(ru * o, axis=1), -1, 1))
    out = []
    i = np.where((dist[1:-1] <= dist[:-2]) & (dist[1:-1] <= dist[2:]) & (dist[1:-1] <= 145))[0] + 1
    for k in i:
        out.append({"t": float(s[k]), "nadir_km": round(float(dist[k]), 1), "dir": "desc" if v[k, 2] < 0 else "asc"})
    return out


def stac(lat, lon, a, b):
    body = {"collections": ["sentinel-2-l2a"], "intersects": {"type": "Point", "coordinates": [lon, lat]}, "datetime": f"{a}/{b}", "limit": 200}
    req = urllib.request.Request("https://earth-search.aws.element84.com/v1/search", data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **UA})
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=60))["features"]
        except urllib.error.HTTPError:
            time.sleep(5 * (i + 1))
    return None


now = datetime.now(timezone.utc).replace(microsecond=0)
start = now - timedelta(days=7)
j, fr = jday(start.year, start.month, start.day, start.hour, start.minute, start.second)
jd0 = j + fr
sats = {k: Satrec.twoline2rv(*tle(v)) for k, v in SATS.items()}
a, b = start.strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ")
rows, tally = [], Counter()
for city, (lat, lon) in CITIES.items():
    feats = stac(lat, lon, a, b)
    if feats is None:
        rows.append({"city": city, "error": "stac"})
        continue
    scenes = [(f["properties"]["platform"].lower(), (datetime.fromisoformat(f["properties"]["datetime"].replace("Z", "+00:00")) - start).total_seconds()) for f in feats]
    n = 0
    for name, sat in sats.items():
        for p in passes(sat, jd0, 7 * 86400, lat, lon):
            hit = any(pl == name and abs(sc - p["t"]) <= 900 for pl, sc in scenes)
            rows.append({"city": city, "sat": name, **p, "imaged": hit})
            tally[(p["dir"], hit)] += 1
            tally[(name, p["dir"], hit)] += 1
            n += 1
    print(city, "passes", n, "scenes", len(scenes))
    time.sleep(0.5)

(HERE / "results.json").write_text(json.dumps({"start": a, "end": b, "rows": rows}, indent=1))
for d in ("desc", "asc"):
    y, m = tally[(d, True)], tally[(d, False)]
    print(d, "imaged", y, "not", m, "share", round(y / (y + m), 3) if y + m else None)
for name in SATS:
    for d in ("desc", "asc"):
        y, m = tally[(name, d, True)], tally[(name, d, False)]
        print(name, d, y, m)
