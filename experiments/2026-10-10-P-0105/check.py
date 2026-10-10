"""P-0105: call scan.rug() (edited) on tonight's five entries and the grinder picks; show the insider fields.
Writes only to this folder; does not run snapshot(), so SNAPSHOTS.csv is untouched."""
import json
import sys
import time

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import scan  # noqa: E402

MINTS = ["BQAeeSowpwEx8Km8GcporcbuLKq4a7EQceH3F2qZpump", "CgU6mugt2HXkjaunbaYrauJRRW9kSKbQXcBRzT7Vpump",
         "B5uNPxEWB6WU3Rej33iDuX7yobZ5N4kXXckoj8KSpump", "Gyk9Z93Ri2JUjqES9HTpc7pxCJTLD7vhBhEjBhyApump",
         "8ZCmwpW3MtC5UpNcZf7U4HMvRNTo71syU11BDiAFpump"]
out = []
for m in MINTS:
    r = scan.rug(m)
    ins = r.get("insiders")
    out.append({"mint": m, "score": r["score"], "insiders": ins})
    if ins is None:
        print(m[:8], "no full report (summary fallback)")
    else:
        print(m[:8], "creator", (ins["creator"] or "")[:8], "bal", ins["creator_balance"],
              "creator_tokens", ins["creator_tokens_n"], "graph_insiders", ins["graph_insiders"],
              "networks", ins["insider_networks_n"])
    time.sleep(1)
json.dump(out, open("/Users/triton/PROTEUS/experiments/2026-10-10-P-0105/check.json", "w"), indent=1)
