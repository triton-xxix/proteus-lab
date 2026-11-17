"""P-0462: USGS's own aftershock-forecast parameters against what happened on days 2 to 30.

For each M7+ event since 1 Nov 2025 with an `oaf` product: every oaf version (includesuperseded), the
latest one issued within 2 days of the mainshock is the "day-2 forecast" (genuinely before days 2 to 30);
the current one is also scored, but it was refitted on the sequence so far and is in sample. Expected count
above Mc in the region for days 2 to 30 from the Reasenberg-Jones rate
    n(t) = 10^(a + b(Mmain - Mc)) (t + c)^-p   per day
against the ComCat count in the same circle and magnitude. Within a factor of 2 = ratio in [0.5, 2].

    python3 -I experiments/2026-11-17-P-0462/oaf.py
"""
import json
import math
import pathlib
import time
import urllib.request

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
Q = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read())


def iso(ms):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(ms / 1000))


def expected(par, t1=2.0, t2=30.0):
    k = 10 ** (par["a"] + par["b"] * (par["magMain"] - par["Mc"]))
    p, c = par["p"], par["c"]
    if abs(p - 1) < 1e-9:
        integ = math.log((t2 + c) / (t1 + c))
    else:
        integ = ((t2 + c) ** (1 - p) - (t1 + c) ** (1 - p)) / (1 - p)
    return k * integ


def observed(par, t0):
    u = (f"{Q}?format=geojson&starttime={iso(t0 + 2 * 86400000)}&endtime={iso(t0 + 30 * 86400000)}"
         f"&latitude={par['regionCenterLat']}&longitude={par['regionCenterLon']}&maxradiuskm={par['regionRadius']}"
         f"&minmagnitude={par['Mc']}")
    return len(get(u)["features"])


events = get(f"{Q}?format=geojson&starttime=2025-11-01&endtime=2026-11-17&minmagnitude=7&producttype=oaf")["features"]
rows = []
for f in events:
    eid, t0 = f["id"], f["properties"]["time"]
    det = get(f"{Q}?eventid={eid}&format=geojson&includesuperseded=true")
    versions = []
    for pr in det["properties"]["products"].get("oaf", []):
        url = pr["contents"].get("forecast.json", {}).get("url")
        if url:
            versions.append((pr["updateTime"], url))
    versions.sort()
    day2 = [v for v in versions if v[0] <= t0 + 2 * 86400000]
    row = {"id": eid, "place": f["properties"]["place"], "mag": f["properties"]["mag"], "time": iso(t0),
           "oaf_versions": len(versions)}
    picks = {"day2": day2[-1] if day2 else None, "current": versions[-1] if versions else None}
    for name, v in picks.items():
        if v is None:
            row[name] = None
            continue
        par = get(v[1])["model"]["parameters"]
        need = ("a", "b", "p", "c", "Mc", "magMain", "regionRadius", "regionCenterLat", "regionCenterLon")
        if any(k not in par for k in need):
            row[name] = {"issued": iso(v[0]), "skipped": "params lack " + ",".join(k for k in need if k not in par),
                         "keys": sorted(par)}
            continue
        exp = expected(par)
        row[name] = {"issued": iso(v[0]), "hours_after": round((v[0] - t0) / 3600000, 1),
                     "params": {k: par[k] for k in ("a", "b", "p", "c", "Mc", "magMain", "regionRadius")},
                     "expected_d2_30": round(exp, 1)}
        time.sleep(0.3)
    usable = [n for n in ("day2", "current") if row.get(n) and "expected_d2_30" in row[n]]
    if not usable:
        rows.append(row)
        print(eid, row["place"], "skipped", row)
        continue
    par = get(picks[usable[0]][1])["model"]["parameters"]
    obs = observed(par, t0)
    row["observed_d2_30"] = obs
    for name in usable:
        if row.get(name):
            e = row[name]["expected_d2_30"]
            row[name]["ratio_obs_exp"] = round(obs / e, 2) if e else None
            row[name]["within_2x"] = bool(e) and 0.5 <= obs / e <= 2
    rows.append(row)
    print(eid, row["place"], row["mag"], "obs", obs,
          "day2", row["day2"] and (row["day2"]["hours_after"], row["day2"]["expected_d2_30"]),
          "current", row["current"] and row["current"]["expected_d2_30"])
    time.sleep(0.5)

summary = {"events": len(rows),
           "day2_scored": sum(1 for r in rows if r["day2"] and "within_2x" in r["day2"]),
           "day2_within_2x": sum(1 for r in rows if r["day2"] and r["day2"].get("within_2x")),
           "current_scored": sum(1 for r in rows if r["current"] and "within_2x" in r["current"]),
           "current_within_2x": sum(1 for r in rows if r["current"] and r["current"].get("within_2x"))}
print(json.dumps(summary))
(HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
