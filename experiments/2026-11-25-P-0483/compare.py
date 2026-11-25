"""P-0483: compare this week's ONAA path check with P-0482's (18 Nov) and ask the six vanished paths directly."""
import json, time, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
old = json.loads((HERE.parent / "2026-11-18-P-0482" / "results.json").read_text())
new = json.loads((HERE / "results.json").read_text())
op = {r["path"]: r["status"] for r in old["rows"]}
np_ = {r["path"]: r["status"] for r in new["rows"]}
out = {"spec_version_then": old.get("spec_version"), "spec_version_now": new.get("spec_version"),
       "paths_in_spec_then": old["paths_in_spec"], "paths_in_spec_now": new["paths_in_spec"],
       "gone_from_asked": sorted(set(op) - set(np_)), "new_in_asked": sorted(set(np_) - set(op)),
       "status_changed": {p: [op[p], np_[p]] for p in sorted(set(op) & set(np_)) if op[p] != np_[p]}}
direct = {}
for p in old["not_found"]:
    try:
        r = urllib.request.urlopen(urllib.request.Request("https://api.onaa.net" + p, headers={"User-Agent": "path-check/1.0"}), timeout=20)
        direct[p] = r.status
    except urllib.error.HTTPError as e:
        direct[p] = e.code
    except Exception as e:
        direct[p] = type(e).__name__
    time.sleep(1.5)
out["last_weeks_404s_asked_directly"] = direct
(HERE / "compare.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
