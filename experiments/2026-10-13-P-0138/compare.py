#!/usr/bin/env python3
"""P-0138: agent-standup (server.js 364-366, v from npm 13 Oct 2026) keeps one usage per message.id, the
LAST record seen. bin/usage.py's rule keeps the LARGEST record per requestId. Both applied to the main
transcript of the 20 most recent Proteus sessions; tokens compared per session.

    python3 compare.py
"""
import glob, json, os

DIR = os.path.expanduser("~/.claude/projects/-Users-triton-PROTEUS/")
OUT = "/Users/triton/PROTEUS/experiments/2026-10-13-P-0138/"
files = sorted(glob.glob(DIR + "*.jsonl"), key=os.path.getmtime)[-21:-1]   # skip the live session


def tot(u):
    return {"i": u.get("input_tokens") or 0, "o": u.get("output_tokens") or 0,
            "r": u.get("cache_read_input_tokens") or 0, "w": u.get("cache_creation_input_tokens") or 0}


rows = []
for f in files:
    last, big, first = {}, {}, {}
    for line in open(f, errors="replace"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        m = r.get("message") if isinstance(r.get("message"), dict) else None
        if not m or not m.get("usage"):
            continue
        u = tot(m["usage"])
        if m.get("id"):
            last[m["id"]] = u
            first.setdefault(m["id"], u)
        key = r.get("requestId") or m.get("id")
        if key and (key not in big or sum(u.values()) > sum(big[key].values())):
            big[key] = u
    s = lambda d, k: sum(x[k] for x in d.values())
    row = {"file": os.path.basename(f), "messages": len(last), "requests": len(big)}
    for k in "iorw":
        row["tool_" + k] = s(last, k); row["mine_" + k] = s(big, k); row["first_" + k] = s(first, k)
    rows.append(row)

agg = {k: sum(r[k] for r in rows) for k in rows[0] if k.startswith(("tool_", "mine_", "first_"))}
worst = max(rows, key=lambda r: abs(r["tool_o"] - r["mine_o"]) / max(r["mine_o"], 1))
within = sum(1 for r in rows if all(abs(r["tool_" + k] - r["mine_" + k]) <= 0.05 * max(r["mine_" + k], 1) for k in "iorw"))
res = {"sessions": len(rows), "within_5pct_all_four": within, "aggregate": agg,
       "worst_output_gap_pct": round(100 * (worst["tool_o"] - worst["mine_o"]) / max(worst["mine_o"], 1), 2),
       "first_record_output_gap_pct": round(100 * (agg["first_o"] - agg["mine_o"]) / max(agg["mine_o"], 1), 2),
       "rows": rows}
json.dump(res, open(OUT + "result.json", "w"), indent=1)
print("sessions", len(rows), "within 5 pct on all four counts", within)
print("output tokens: tool", agg["tool_o"], "mine", agg["mine_o"], "first-record", agg["first_o"])
print("input+cache: tool", agg["tool_i"] + agg["tool_r"] + agg["tool_w"], "mine", agg["mine_i"] + agg["mine_r"] + agg["mine_w"])
print("worst session output gap pct", res["worst_output_gap_pct"], "| first-record rule gap pct", res["first_record_output_gap_pct"])
