"""D-019 and D-021: the three stock rules on the sessions the forward week actually registered.

Usage: /Users/triton/PROTEUS/.venv/bin/python3 rescore.py OUT.json

The 7 Nov scan's W1 is 30 Oct, 2, 3, 4 and 6 Nov: 5 Nov fell below prepare()'s 70-bar floor, so the
block reached back to 30 Oct, a day FORWARD.md excluded on purpose. This reads the rules with scan.py's
own functions, unchanged, on:

  A  2, 3, 4, 6 Nov   the four registered sessions the scanner kept
  B  2, 3, 4, 5, 6 Nov  the registered week, with the 70-bar floor lowered to 50 so 5 Nov counts

Days after the 1 Nov clock change are labelled correctly by yahoo_5m, and neither set touches an
earlier day. Nothing here is the registered figure; that is W1 in results.json. Same seed and same
permutation count as the scanner, so the control mean is drawn the same way.
"""
import inspect
import json
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/edges/scan")
import scan  # noqa: E402

WANT = {"VWAP cross after 11:00, hold to close": "E-013",
        "ORB 15m fade (failed break)": "E-014",
        "Opening drive: first bar direction to 11:00": "E-016"}
A = {"2026-11-02", "2026-11-03", "2026-11-04", "2026-11-06"}
B = A | {"2026-11-05"}

raw = {s: scan.yahoo_5m(s) for s in scan.STOCKS}
strict = {s: scan.prepare(raw[s], "stock") for s in scan.STOCKS}
source = inspect.getsource(scan.prepare).replace("b - a < 70", "b - a < 50")
assert "b - a < 50" in source
exec(source, scan.__dict__)
loose = {s: scan.prepare(raw[s], "stock") for s in scan.STOCKS}
out = {"bars_5_nov": {s: sum(1 for r in raw[s] if r[1] == "2026-11-05") for s in scan.STOCKS}}
cost = scan.COST["stock"]


def read(days, dates, fn):
    trades = []
    for s in scan.STOCKS:
        for D in days[s]:
            if D["date"] not in dates:
                continue
            for e, side, j, en, ex in fn(D):
                hold = j - e + 1
                trades.append({"sym": s, "date": D["date"], "side": side, "hold": hold,
                               "net": side * (ex / en - 1) - cost,
                               "pool": scan.control_pool(D, side, hold, cost)})
    w = scan.score(trades, cost)
    w["per_day"] = {d: round(sum(t["net"] for t in trades if t["date"] == d) * 100, 3) for d in sorted(dates)}
    w["passes"] = bool(w["n"] and w["total_pct"] > 0 and w["mean_pct"] > w["control_mean_pct"])
    return w


for kind, name, fn in scan.RULES:
    if kind == "stock" and name in WANT:
        out[WANT[name]] = {"rule": name, "A_four_sessions": read(strict, A, fn), "B_five_with_5_nov": read(loose, B, fn)}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps(out, indent=1))
