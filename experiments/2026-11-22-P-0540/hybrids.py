"""P-0540: are London's high-mileage MOT cars Toyota hybrids, and what is the gap without them?

P-0534's sample and method (P-0522's range-read helpers, three 2024 months, 40 MB heads, keyless;
class 4 NT tests, first use 2015 to 2019, London and Scotland, miles per year bins), plus the make
and fuel_type columns. Hybrid = fuel_type HY. Reports the hybrid and Toyota-hybrid share per bin and
region, and the London minus Scotland gap (incl PRS and P only) with all hybrids removed.
"""
import csv, io, json, os, types
from collections import defaultdict, Counter
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
tally = defaultdict(lambda: {"P": 0, "F": 0, "PRS": 0})  # (reg, bin, group)
fuels = defaultdict(Counter)
makes_hy = defaultdict(Counter)
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
            continue
        b = binof(mpy)
        fuel = r[ix["fuel_type"]].strip().upper()
        make = r[ix["make"]].strip().upper()
        hy = fuel == "HY"
        fuels[(reg, b)][fuel] += 1
        fuels[(reg, "ALL")][fuel] += 1
        if hy:
            makes_hy[(reg, b)][make] += 1
        for g in ("all", "no_hybrid" if not hy else "hybrid"):
            tally[(reg, b, g)][res] += 1
            tally[(reg, "ALL", g)][res] += 1

out = {"bins": [], "fuel_codes_seen": sorted(set().union(*[set(c) for c in fuels.values()]))}
for _, _, b in BINS + [(0, 0, "ALL")]:
    row = {"bin": b}
    for reg in ("London", "Scotland"):
        n = sum(fuels[(reg, b)].values())
        hy = fuels[(reg, b)]["HY"]
        toy = makes_hy[(reg, b)]["TOYOTA"]
        row[reg] = {"n": n, "hybrid_pct": round(100 * hy / n, 1) if n else None,
                    "toyota_hybrid_pct": round(100 * toy / n, 1) if n else None,
                    "top_hybrid_makes": makes_hy[(reg, b)].most_common(3)}
    for g in ("all", "no_hybrid", "hybrid"):
        L, S = tally[("London", b, g)], tally[("Scotland", b, g)]
        if sum(L.values()) >= 30 and sum(S.values()) >= 30:
            row["gap_" + g] = {"incl_PRS": round(rate(L, True) - rate(S, True), 2),
                               "P_only": round(rate(L, False) - rate(S, False), 2),
                               "london_n": sum(L.values()), "scotland_n": sum(S.values())}
        else:
            row["gap_" + g] = None
    out["bins"].append(row)
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
