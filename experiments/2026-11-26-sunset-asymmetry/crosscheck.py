"""Cross-check of sunset_asym.py against Open-Meteo daily sunrise and sunset (UTC, whole minutes), 16 days."""
import importlib.util, json, sys, urllib.request, datetime as dt

HERE = "/Users/triton/PROTEUS/experiments/2026-11-26-sunset-asymmetry/"
spec = importlib.util.spec_from_file_location("sa", HERE + "sunset_asym.py")
# sunset_asym runs on import (writes results.json to argv[1]); point it at a throwaway path
sys_argv = sys.argv[:]
sys.argv = ["x", "/Users/triton/PROTEUS/sandbox"]
sa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sa)
sys.argv = sys_argv

out = {}
for city, (lat, lon) in sa.CITIES.items():
    url = ("https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s&daily=sunrise,sunset&timezone=GMT&forecast_days=16"
           % (lat, lon))
    d = json.load(urllib.request.urlopen(url, timeout=30))["daily"]
    gaps = []
    for day, sr, ss in zip(d["time"], d["sunrise"], d["sunset"]):
        r, s, _ = sa.events(dt.date.fromisoformat(day), lat, lon)
        om_r = int(sr[11:13]) * 60 + int(sr[14:16])
        om_s = int(ss[11:13]) * 60 + int(ss[14:16])
        gaps.append({"day": day, "sunrise_gap": round(r - om_r, 2), "sunset_gap": round(s - om_s, 2)})
    mx = max(max(abs(g["sunrise_gap"]), abs(g["sunset_gap"])) for g in gaps)
    om_min_ss = min(d["sunset"], key=lambda x: x[11:])
    out[city] = {"days": len(gaps), "max_abs_gap_min": mx, "om_point": [lat, lon],
                 "open_meteo_earliest_sunset_in_window": om_min_ss, "gaps": gaps}
    print(city, "days", len(gaps), "max gap", mx, "OM earliest sunset in window", om_min_ss)
json.dump(out, open(HERE + "crosscheck.json", "w"), indent=1)
