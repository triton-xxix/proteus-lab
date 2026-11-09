"""Which way did the page and the single endpoint differ, and did it track age or read gap? Reads results.json only."""
import json
import pathlib
from datetime import datetime, timezone

rows = json.loads((pathlib.Path(__file__).parent / "results.json").read_text())
r0 = [p for p in rows[0]["pools"] if p.get("on_page")]
t0 = rows[0]["at"]
for p in r0:
    created = datetime.fromisoformat(p["page"]["created"].replace("Z", "+00:00")).timestamp()
    print(f"{p['page']['name'][:18]:18s} age_min {(t0 - created) / 60:6.1f} read_gap_s {p['secs_after_page']:6.1f} "
          f"page_h1 {p['page']['h1']:12.2f} single_h1 {p['single']['h1']:12.2f} ratio {p['single']['h1'] / p['page']['h1']:7.2f} "
          f"reserve {p['page']['reserve']:10.0f} {p['single']['reserve']:10.0f}")
print("single above page", sum(p["single"]["h1"] > p["page"]["h1"] for p in r0), "of", len(r0))
