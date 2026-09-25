"""Wildcard 2026-09-24: how good is National Grid ESO's own carbon-intensity forecast?

Keyless API, api.carbonintensity.org.uk. Pulls the last 48 half-hours, each carrying the
forecast published for it and the 'actual' (their estimate from metered generation), and
scores the forecast. Also pulls today's generation mix. Prints a summary; writes the raw JSON
to sandbox/carbon/.
"""
import json
import statistics
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT = Path("/Users/triton/PROTEUS/sandbox/carbon")
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://api.carbonintensity.org.uk"


def get(path):
    t0 = time.time()
    req = urllib.request.Request(BASE + path, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    return body, time.time() - t0


now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
start = (now - timedelta(hours=48)).strftime("%Y-%m-%dT%H:%MZ")
end = now.strftime("%Y-%m-%dT%H:%MZ")
data, secs = get(f"/intensity/{start}/{end}")
(OUT / "intensity.json").write_text(json.dumps(data, indent=1))
rows = [d for d in data["data"] if d["intensity"]["actual"] is not None]
err = [d["intensity"]["forecast"] - d["intensity"]["actual"] for d in rows]
act = [d["intensity"]["actual"] for d in rows]
ape = [abs(e) / a for e, a in zip(err, act) if a]
print(f"window {start} to {end}, {len(data['data'])} periods, {len(rows)} with actual, {secs:.2f}s")
print(f"actual gCO2/kWh: min {min(act)} median {statistics.median(act)} max {max(act)}")
print(f"forecast minus actual: mean {statistics.mean(err):+.1f}, MAE {statistics.mean(abs(e) for e in err):.1f}, "
      f"MAPE {100*statistics.mean(ape):.1f}%, worst {max(err, key=abs):+d}")
over = sum(1 for e in err if e > 0)
print(f"forecast too high in {over} of {len(err)} periods")
lo = min(rows, key=lambda d: d["intensity"]["actual"])
hi = max(rows, key=lambda d: d["intensity"]["actual"])
print(f"cleanest half-hour {lo['from']} {lo['intensity']['actual']}; dirtiest {hi['from']} {hi['intensity']['actual']}")

mix, secs = get("/generation")
(OUT / "generation.json").write_text(json.dumps(mix, indent=1))
parts = sorted(mix["data"]["generationmix"], key=lambda g: -g["perc"])
print(f"mix now ({mix['data']['from']}): " + ", ".join(f"{g['fuel']} {g['perc']}%" for g in parts if g["perc"] > 0))
