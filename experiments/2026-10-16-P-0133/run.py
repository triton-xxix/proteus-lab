#!/usr/bin/env python3
"""P-0133: one /injuries?date=2026-10-17 call, count rows in the nine Pitch leagues."""
import importlib.util
import json
import sys
from collections import Counter

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
spec = importlib.util.spec_from_file_location("apisports", "/Users/triton/PROTEUS/pitch/apisports.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)

h = A.headers()
errs, resp, remaining = A.get("/injuries", h, date="2026-10-17")
out = {"errors": errs, "rows_all": len(resp), "remaining": remaining}
keep = [r for r in resp if r.get("league", {}).get("id") in A.LEAGUE_DIV]
out["rows_pitch"] = len(keep)
out["by_div"] = dict(Counter(A.LEAGUE_DIV[r["league"]["id"]] for r in keep))
out["other_leagues"] = dict(Counter(r["league"]["name"] for r in resp if r["league"]["id"] not in A.LEAGUE_DIV).most_common(8))
fx = {}
for r in keep:
    fx.setdefault(r["fixture"]["id"], []).append(
        "%s: %s (%s, %s)" % (r["team"]["name"], r["player"]["name"], r["player"].get("type"), r["player"].get("reason")))
out["fixtures_with_injuries"] = len(fx)
out["sample"] = list(fx.values())[:5]
json.dump(out, open("/Users/triton/PROTEUS/experiments/2026-10-16-P-0133/results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "sample"}, indent=1))
