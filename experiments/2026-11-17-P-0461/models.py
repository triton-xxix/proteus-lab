"""P-0461: is P-0446/P-0447's EDDM low-cloud warm miss the model (icon_seamless) or the weather?

Same flag, same days, same error and permutation as experiments/2026-11-14-P-0447/stations.py (EDDM, city
point 48.1370, 11.5750, as P-0446 and P-0447), run for icon_seamless, ecmwf_ifs025 and gfs_seamless, scored
on the days all three have, so the gaps are compared like for like.

    python3 -I experiments/2026-11-17-P-0461/models.py
"""
import importlib.util
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
HERE = pathlib.Path(__file__).parent
# load metar() and test() from P-0447 without running its main loop: exec only the defs
src = open(ROOT + "/experiments/2026-11-14-P-0447/stations.py").read().split("\nout = {}")[0]
ns = {"__file__": ROOT + "/experiments/2026-11-14-P-0447/stations.py"}
exec(compile(src, "stations.py", "exec"), ns)
metar, test, get = ns["metar"], ns["test"], ns["get"]
LAT, LON = 48.1370, 11.5750
MODELS = ("icon_seamless", "ecmwf_ifs025", "gfs_seamless")


def lead1_all():
    out = {m: {} for m in MODELS}
    for a, b in (("2025-11-01", "2026-04-30"), ("2026-05-01", "2026-10-31")):
        h = json.loads(get(f"https://previous-runs-api.open-meteo.com/v1/forecast?latitude={LAT:.4f}&longitude={LON:.4f}"
                           f"&hourly=temperature_2m_previous_day1&start_date={a}&end_date={b}&timezone=UTC"
                           f"&models={','.join(MODELS)}"))["hourly"]
        for m in MODELS:
            vals = h.get("temperature_2m_previous_day1_" + m, [])
            days = defaultdict(list)
            for t, v in zip(h["time"], vals):
                if v is not None:
                    days[t[:10]].append(v)
            out[m].update({k: max(v) for k, v in days.items() if len(v) >= 23})
        time.sleep(2)
    return out


mh, low = metar("EDDM")
time.sleep(2)
fc = lead1_all()
common = sorted(set(mh).intersection(*[set(fc[m]) for m in MODELS]))
common = [d for d in common if "2025-11-01" <= d <= "2026-10-31"]
res = {"days_common": len(common), "models": {}}
for m in MODELS:
    rows = [{"date": d, "low": low.get(d, False), "err": mh[d] - fc[m][d]} for d in common]
    r = test(rows)
    r["mean_err_all"] = round(sum(x["err"] for x in rows) / len(rows), 3)
    res["models"][m] = r
    print(m, r)
# the three-model mean as a fourth forecast
rows = [{"date": d, "low": low.get(d, False), "err": mh[d] - sum(fc[m][d] for m in MODELS) / 3} for d in common]
res["models"]["mean_of_three"] = test(rows)
print("mean_of_three", res["models"]["mean_of_three"])
(HERE / "results.json").write_text(json.dumps(res, indent=1))
