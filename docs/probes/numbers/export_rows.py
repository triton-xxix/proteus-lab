#!/usr/bin/env python3
"""Export the scored called shots for number scoring (Workshop, 6 Nov 2026).

One JSON line per shot: id, title, expect, verdict, p, the number written before the run, the verdict
note and the artefact folder. A reader then scores each line under RULE.md. Writes to the path given.
"""
import json
import sys

STATE = "/Users/triton/PROTEUS/state/probes.json"


def main():
    out = sys.argv[1]
    st = json.load(open(STATE))
    n = 0
    with open(out, "w") as f:
        for i in st["items"]:
            s = i.get("shot")
            if not s or i.get("status") != "done" or not i.get("verdict"):
                continue
            row = {"id": i["id"], "title": (i.get("title") or "")[:120], "expect": s["expect"],
                   "verdict": i["verdict"], "p": s["p"], "number": s.get("number", ""), "at": s["at"]}
            for k, v in i.items():
                if k not in ("id", "title", "shot", "status", "verdict") and isinstance(v, str) and len(v) < 1500:
                    row[k] = v
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    print("export_rows: %d shots written to %s" % (n, out))


if __name__ == "__main__":
    main()
