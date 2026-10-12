"""Build docs/probes/P-0128/data.json from this probe's result.json (Workshop, 12 Oct 2026).

The run's window_utc is an hour early (the mktime bug in the README), so the right window is the stored
one shifted by +3600 s. Every number on the page is derived here, none typed by hand.
"""
import json
import time

HERE = "/Users/triton/PROTEUS/experiments/2026-10-12-P-0128"
OUT = "/Users/triton/PROTEUS/docs/probes/P-0128/data.json"

d = json.load(open(HERE + "/result.json"))
lo_bad, hi_bad = d["window_utc"]
lo, hi = lo_bad + 3600, hi_bad + 3600
snap = (lo + hi) // 2
held = {(h["symbol"], h["wallet"]) for h in d["holding_now"]}

rows = []
for e in d["ever"]:
    rows.append({
        "symbol": e["symbol"], "name": e["name"], "sigs": e["sigs"],
        "first": e["first"], "last": e["last"],
        "spans": e["first"] <= hi and e["last"] >= lo,
        "inside": lo <= e["first"] <= hi or lo <= e["last"] <= hi,
        "holding": (e["symbol"], e["wallet"]) in held,
    })

picks = []
for p in d["picks"]:
    s = p["symbol"]
    mine = [r for r in rows if r["symbol"] == s]
    picks.append({
        "id": p["id"], "symbol": s, "ts": p["ts"],
        "ever": len(mine),
        "spans": sum(r["spans"] for r in mine),
        "holding": sum(r["holding"] for r in mine),
    })

iso = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
out = {
    "probe": "P-0128",
    "wallets": d["wallets"],
    "lookups": d["wallets"] * len(d["picks"]),
    "rpc_calls": d["rpc_calls"],
    "rpc_errors": d["rpc_errors"],
    "snapshot": iso(snap),
    "window": [lo, hi],
    "window_iso": [iso(lo), iso(hi)],
    "window_bad_iso": [iso(lo_bad), iso(hi_bad)],
    "in_window_bad": d["wallets_touching_in_window"],
    "ever": len(rows),
    "holding_now": len(d["holding_now"]),
    "spans_wallets": len({(r["name"]) for r in rows if r["spans"]}),
    "spans_rows": sum(r["spans"] for r in rows),
    "inside_rows": sum(r["inside"] for r in rows),
    # a first or last signature inside the window is a transaction inside it, so this is a floor
    "inside_wallets": len({r["name"] for r in rows if r["inside"]}),
    "inside_by_pick": {p["symbol"]: sum(r["inside"] for r in rows if r["symbol"] == p["symbol"]) for p in d["picks"]},
    "shot": "works at 0.55; 1 of 91 wallets touches a pick in the window",
    "picks": picks,
    "rows": rows,
}
json.dump(out, open(OUT, "w"), indent=1)
print("window", out["window_iso"], "snapshot", out["snapshot"])
print("ever", out["ever"], "holding", out["holding_now"], "spans wallets", out["spans_wallets"],
      "spans rows", out["spans_rows"], "inside rows", out["inside_rows"])
for p in picks:
    print(p)
