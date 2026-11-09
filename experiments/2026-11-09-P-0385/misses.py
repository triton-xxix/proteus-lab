"""List the descending passes with no scene, with how long ago they were and how close to the swath edge."""
import json
import pathlib
from datetime import datetime

d = json.loads((pathlib.Path(__file__).parent / "results.json").read_text())
end = datetime.fromisoformat(d["end"].replace("Z", "+00:00"))
start = datetime.fromisoformat(d["start"].replace("Z", "+00:00"))
span = (end - start).total_seconds()
for r in d["rows"]:
    if r.get("dir") == "desc" and not r["imaged"]:
        print(r["city"], r["sat"], f"age_days {(span - r['t']) / 86400:.2f}", f"nadir_km {r['nadir_km']}")
hit = [r["nadir_km"] for r in d["rows"] if r.get("dir") == "desc" and r["imaged"]]
print("imaged descending nadir_km: min", min(hit), "max", max(hit))
