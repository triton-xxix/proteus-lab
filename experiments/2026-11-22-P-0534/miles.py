"""P-0534: the London minus Scotland MOT pass gap matched on miles per year.

P-0530's sample through P-0522's helpers (three 2024 months, 40 MB heads, keyless). Class 4 NT tests,
first use 2015 to 2019, London and Scotland. Miles per year = test_mileage / (test_date - first_use_date
in years). Bins: under 5k, 5-8k, 8-11k, 11-14k, 14k and over. Gap within each bin, and London's bin
rates reweighted to Scotland's bin mix.
"""
import csv, io, json, os, types
from collections import defaultdict
from datetime import date

SRC = "/Users/triton/PROTEUS/experiments/2026-11-21-P-0522/sample.py"
p22 = types.ModuleType("p22")
p22.__file__ = SRC
exec(compile(open(SRC).read().rsplit("\nmain()", 1)[0], SRC, "exec"), p22.__dict__)
HERE = os.path.dirname(os.path.abspath(__file__))
BINS = [(0, 5000, "<5k"), (5000, 8000, "5-8k"), (8000, 11000, "8-11k"), (11000, 14000, "11-14k"), (14000, 10 ** 9, "14k+")]


def binof(mpy):
    for lo, hi, name in BINS:
        if lo <= mpy < hi:
            return name


def rate(t, prs):
    n = sum(t.values())
    return 100 * (t["P"] + (t["PRS"] if prs else 0)) / n if n else None


size, mems = p22.members()
csvs = [m for m in mems if m["name"].lower().endswith((".csv", ".txt")) and "__MACOSX" not in m["name"]]
picks = csvs[:: max(1, len(csvs) // 3)][:3]
tally = defaultdict(lambda: {"P": 0, "F": 0, "PRS": 0})
skipped = 0
for m in picks:
    lines = p22.stream(m, 40).split("\n")[:-1]
    rdr = csv.reader(io.StringIO("\n".join(lines)), quoting=csv.QUOTE_NONE)
    hdr = next(rdr)
    ix = {h.strip().lower(): i for i, h in enumerate(hdr)}
    for r in rdr:
        if len(r) != len(hdr) or r[ix["test_type"]] != "NT" or r[ix["test_class_id"]] != "4":
            continue
        fu = r[ix["first_use_date"]][:10]
        if not ("2015" <= fu[:4] <= "2019"):
            continue
        reg = p22.region(r[ix["postcode_area"]])
        res = r[ix["test_result"]]
        if reg not in ("London", "Scotland") or res not in ("P", "F", "PRS"):
            continue
        try:
            yrs = (date.fromisoformat(r[ix["test_date"]][:10]) - date.fromisoformat(fu)).days / 365.25
            mpy = float(r[ix["test_mileage"]]) / yrs
        except (ValueError, ZeroDivisionError):
            skipped += 1
            if skipped <= 3:
                print("skip", r[ix["test_date"]], fu, repr(r[ix["test_mileage"]]), flush=True)
            continue
        b = binof(mpy)
        tally[(reg, b)][res] += 1
        tally[(reg, "ALL")][res] += 1
out = {"skipped_no_mileage": skipped, "bins": [], "adjusted": {}}
for prs in (False, True):
    key = "incl_PRS" if prs else "P_only"
    lon_w = sco_w = w = 0
    for _, _, b in BINS:
        L, S = tally[("London", b)], tally[("Scotland", b)]
        nS = sum(S.values())
        if sum(L.values()) >= 30 and nS >= 30:
            lon_w += nS * rate(L, prs)
            sco_w += nS * rate(S, prs)
            w += nS
    out["adjusted"][key] = round((lon_w - sco_w) / w, 2)
    out["raw_" + key] = round(rate(tally[("London", "ALL")], prs) - rate(tally[("Scotland", "ALL")], prs), 2)
for _, _, b in BINS + [(0, 0, "ALL")]:
    L, S = tally[("London", b)], tally[("Scotland", b)]
    out["bins"].append({"bin": b, "london_n": sum(L.values()), "scotland_n": sum(S.values()),
                        "london_share": None, "gap_incl_PRS": round(rate(L, True) - rate(S, True), 2) if sum(L.values()) and sum(S.values()) else None,
                        "gap_P_only": round(rate(L, False) - rate(S, False), 2) if sum(L.values()) and sum(S.values()) else None})
nl, ns = sum(tally[("London", "ALL")].values()), sum(tally[("Scotland", "ALL")].values())
for row in out["bins"]:
    row["london_share"] = round(100 * row["london_n"] / nl, 1)
    row["scotland_share"] = round(100 * row["scotland_n"] / ns, 1)
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
