"""P-0164: recompute cc-stretch's published replay numbers from its own results.csv, independently of report.ts."""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

SRC = Path("/Users/triton/PROTEUS/sandbox/p0164/cc-stretch-HEAD/bench/results.csv")
rows = list(csv.DictReader(open(SRC)))
by = defaultdict(list)
for r in rows:
    by[r["project"]].append(r)
by["all"] = rows
out = {}
for p, rs in by.items():
    o = sum(int(r["original_words"]) for r in rs)
    s = sum(int(r["skim_words"]) for r in rs)
    f = sum(int(r["full_words"]) for r in rs)
    per = [int(r["skim_words"]) / int(r["original_words"]) for r in rs if int(r["original_words"])]
    long_ = [r for r in rs if int(r["original_words"]) >= 40]
    per_long = [int(r["skim_words"]) / int(r["original_words"]) for r in long_]
    recall = [float(r["content_recall"]) for r in rs if r["content_recall"]]
    out[p] = {"replies": len(rs), "original": o, "skim": s, "skim_share": round(s / o, 4),
              "median_per_reply": round(statistics.median(per), 4), "full_share": round(f / o, 4),
              "replies_40plus": len(long_), "median_per_reply_40plus": round(statistics.median(per_long), 4),
              "skim_share_max_reply_40plus": round(max(per_long), 4), "recall_mean": round(statistics.mean(recall), 4),
              "recall_min": min(recall)}
print(json.dumps(out, indent=1))
(Path(__file__).resolve().parent / "recompute.json").write_text(json.dumps(out, indent=1))
