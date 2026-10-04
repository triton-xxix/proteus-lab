"""P-0058 part 2: matches with a score after 20 Sep in the fixturedownload cache, and predictions waiting on them."""
import csv
import json

out = {}
for div in ["E0", "E1"]:
    data = json.load(open(f"/Users/triton/PROTEUS/pitch/cache/fixturedownload-{div}.json"))
    played = [m for m in data if m.get("HomeTeamScore") is not None and str(m.get("DateUtc", "")) > "2026-09-21"]
    out[div] = {"played_after_20sep": len(played),
                "dates": sorted({str(m["DateUtc"])[:10] for m in played}),
                "example": played[:2]}
print(json.dumps({k: {"n": v["played_after_20sep"], "dates": v["dates"]} for k, v in out.items()}, indent=1))

# Predictions committed for kickoffs after 20 Sep that have no score yet
import glob
files = glob.glob("/Users/triton/PROTEUS/pitch/PREDICTIONS*.csv")
waiting = 0
for f in files:
    for row in csv.DictReader(open(f)):
        date = row.get("date") or row.get("Date") or row.get("kickoff") or ""
        scored = row.get("scored") or row.get("result") or row.get("FTR") or ""
        if date[:10] > "2026-09-20" and not scored:
            waiting += 1
print("prediction files", files, "rows after 20 Sep without a result", waiting)
out["waiting"] = waiting
json.dump(out, open("/Users/triton/PROTEUS/experiments/2026-10-04-P-0058/played.json", "w"), indent=2, default=str)
