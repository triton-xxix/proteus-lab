"""P-0257: every GAMES.csv row against the Lichess by-ids export pulled by P-0255 (29 Oct 2026):
result, status and move count.

    python3 experiments/2026-10-29-P-0257/compare.py
"""
import csv, json

OUT = "/Users/triton/PROTEUS/experiments/2026-10-29-P-0257/results.json"
ME = "tritonxxix"
exp = {}
for line in open("/Users/triton/PROTEUS/sandbox/lichess-tritonxxix.ndjson"):
    if line.strip():
        g = json.loads(line)
        side = "white" if g["players"]["white"].get("user", {}).get("id") == ME else "black"
        w = g.get("winner")
        exp[g["id"]] = {"result": "draw" if w is None else ("win" if w == side else "loss"),
                        "status": g["status"], "colour": side, "plies": len(g.get("clocks") or [])}
diffs = []
for r in csv.DictReader(open("/Users/triton/PROTEUS/games/lichess/GAMES.csv")):
    e = exp.get(r["game_id"])
    if not e:
        diffs.append({"id": r["game_id"], "missing_from_export": True})
        continue
    d = {f: (r[f], e[f]) for f in ("result", "status", "colour") if r[f] != e[f]}
    if d:
        diffs.append({"id": r["game_id"], "finished": r["finished_utc"], "log_moves": r["moves"],
                      "export_plies": e["plies"], **{k: {"log": a, "export": b} for k, (a, b) in d.items()}})
out = {"rows_checked": len(exp), "rows_differing": len(diffs), "diffs": diffs}
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(out, indent=1))
