"""P-0063: can Open-Meteo hourly cloud cover alone give tonight's longest clear dark run for a UK site?

Keyless. Darkness is computed here (sun below -18 deg, astronomical night) because Open-Meteo gives
only sunrise/sunset. Clear means total cloud cover at or below 20 percent. Run once per site.
"""
import json, math, sys, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
SITES = {"Kielder": (55.233, -2.583), "Exmoor": (51.14, -3.64), "Galloway": (55.05, -4.45)}
CLEAR = 20


def sun_alt(dt, lat, lon):
    # NOAA low-precision solar position, good to about 0.1 deg: plenty for a -18 deg threshold.
    d = (dt - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds() / 86400
    g = math.radians((357.529 + 0.98560028 * d) % 360)
    q = (280.459 + 0.98564736 * d) % 360
    L = math.radians((q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360)
    e = math.radians(23.439 - 0.00000036 * d)
    ra = math.atan2(math.cos(e) * math.sin(L), math.cos(L))
    dec = math.asin(math.sin(e) * math.sin(L))
    gmst = (18.697374558 + 24.06570982441908 * d) % 24
    ha = math.radians(gmst * 15 + lon) - ra
    la = math.radians(lat)
    return math.degrees(math.asin(math.sin(la) * math.sin(dec) + math.cos(la) * math.cos(dec) * math.cos(ha)))


def run(name, lat, lon):
    url = ("https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s"
           "&hourly=cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility"
           "&timezone=UTC&forecast_days=2" % (lat, lon))
    data = json.load(urllib.request.urlopen(url, timeout=30))
    h = data["hourly"]
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    rows = []
    for i, t in enumerate(h["time"]):
        dt = datetime.fromisoformat(t).replace(tzinfo=timezone.utc)
        if not (now <= dt <= now + timedelta(hours=20)):
            continue
        # judge the hour by the sun at its midpoint
        alt = sun_alt(dt + timedelta(minutes=30), lat, lon)
        rows.append({"utc": t, "sun_alt": round(alt, 1), "cloud": h["cloud_cover"][i],
                     "low": h["cloud_cover_low"][i], "mid": h["cloud_cover_mid"][i],
                     "high": h["cloud_cover_high"][i], "vis_m": h["visibility"][i],
                     "dark": alt < -18, "clear": h["cloud_cover"][i] is not None and h["cloud_cover"][i] <= CLEAR})
    best, cur = [], []
    for r in rows:
        if r["dark"] and r["clear"]:
            cur.append(r)
            if len(cur) > len(best):
                best = list(cur)
        else:
            cur = []
    dark_hours = sum(r["dark"] for r in rows)
    out = {"site": name, "lat": lat, "lon": lon, "dark_hours_ahead": dark_hours,
           "clear_dark_hours": sum(r["dark"] and r["clear"] for r in rows),
           "longest_run_hours": len(best),
           "longest_run": [best[0]["utc"], best[-1]["utc"]] if best else None,
           "model_reported": data.get("generationtime_ms"), "rows": rows}
    return out


results = [run(n, *ll) for n, ll in SITES.items()]
(HERE / "result.json").write_text(json.dumps(results, indent=1))
for r in results:
    print(r["site"], "dark h", r["dark_hours_ahead"], "clear+dark h", r["clear_dark_hours"],
          "longest run", r["longest_run_hours"], r["longest_run"])
    print("  ", " ".join("%s:%s/%s" % (x["utc"][11:13], int(x["cloud"]), "D" if x["dark"] else "-") for x in r["rows"]))
