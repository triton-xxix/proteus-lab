"""Refill row 161: NOAA SWPC's own solar-cycle files, to check the figures the 12 Nov wildcard item
quoted from memory (2019 panel: smoothed peak 115, range 95 to 130, July 2025 plus or minus 8 months).

Pulls the predicted and observed solar-cycle JSON (keyless), saves both, and prints the shape, the
predicted peak, and the observed smoothed peak. SILSO's numbers come from tonight's
experiments/2026-11-12-sunspot-peak/results.json.
"""
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://services.swpc.noaa.gov/json/solar-cycle/"
out = {}
data = {}
for name in ("predicted-solar-cycle.json", "observed-solar-cycle-indices.json"):
    try:
        raw = urllib.request.urlopen(urllib.request.Request(BASE + name, headers={"User-Agent": "research-script/1.0"}), timeout=40).read()
        open(os.path.join(HERE, name), "wb").write(raw)
        data[name] = json.loads(raw)
        out[name] = {"rows": len(data[name]), "keys": sorted(data[name][0].keys()), "first": data[name][0], "last": data[name][-1]}
    except Exception as e:  # a refusal is a result
        out[name] = {"error": "%s: %s" % (type(e).__name__, e)}
    print(name, json.dumps(out[name])[:700])

p = data.get("predicted-solar-cycle.json") or []
o = data.get("observed-solar-cycle-indices.json") or []
if p:
    pk = max(p, key=lambda r: r.get("predicted_ssn") or 0)
    out["predicted_peak_in_file"] = pk
    out["predicted_span"] = [p[0]["time-tag"], p[-1]["time-tag"]]
    print("predicted peak row in file:", pk)
if o:
    c25 = [r for r in o if r["time-tag"] >= "2019-12" and (r.get("smoothed_ssn") or -1) > 0]
    pk = max(c25, key=lambda r: r["smoothed_ssn"])
    out["observed_smoothed_peak"] = pk
    out["observed_last_smoothed"] = c25[-1]
    out["observed_last_monthly"] = {"time-tag": o[-1]["time-tag"], "ssn": o[-1].get("ssn")}
    print("observed smoothed peak:", pk)
    print("last smoothed:", c25[-1])
    print("last monthly:", out["observed_last_monthly"])
    # where the file's forecast and the observation overlap, if they do
    pm = {r["time-tag"]: r for r in p}
    both = [(r["time-tag"], r["smoothed_ssn"], pm[r["time-tag"]].get("predicted_ssn")) for r in c25 if r["time-tag"] in pm]
    out["overlap_months"] = len(both)
    print("overlap months between predicted file and observed smoothed:", len(both), both[:6])
silso = json.load(open("/Users/triton/PROTEUS/experiments/2026-11-12-sunspot-peak/results.json"))
out["silso"] = {"smoothed_peak": silso["c25_smoothed_peak"], "last_smoothed": silso["last_smoothed"], "last_monthly": silso["last_monthly"]}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
