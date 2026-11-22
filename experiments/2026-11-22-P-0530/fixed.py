"""P-0530: the London minus Scotland MOT pass gap with make and model held fixed.

Same sample as P-0522 (three 2024 monthly members, first 40 MB of each, by S3 range reads, keyless):
class 4 normal tests (NT), first used 2015 to 2019. Tally by region and make-model; for the three
make-model pairs with the most tests across London plus Scotland, the pass rate both ways (P only,
and P plus PRS), and a mix-adjusted gap: Scotland's make-model mix reweighting London's rates.
"""
import csv, io, json, os, sys, types
from collections import defaultdict

SRC = "/Users/triton/PROTEUS/experiments/2026-11-21-P-0522/sample.py"
code = open(SRC).read().rsplit("\nmain()", 1)[0]  # P-0522's helpers without running its main
p22 = types.ModuleType("p22")
p22.__file__ = SRC
exec(compile(code, SRC, "exec"), p22.__dict__)
HERE = os.path.dirname(os.path.abspath(__file__))


def rate(t, prs):
    n = t["P"] + t["F"] + t["PRS"]
    return round(100 * (t["P"] + (t["PRS"] if prs else 0)) / n, 2) if n else None


def main():
    size, mems = p22.members()
    csvs = [m for m in mems if m["name"].lower().endswith((".csv", ".txt")) and "__MACOSX" not in m["name"]]
    picks = csvs[:: max(1, len(csvs) // 3)][:3]
    tally = defaultdict(lambda: {"P": 0, "F": 0, "PRS": 0})
    for m in picks:
        text = p22.stream(m, 40)
        lines = text.split("\n")[:-1]
        rdr = csv.reader(io.StringIO("\n".join(lines)), quoting=csv.QUOTE_NONE)
        hdr = next(rdr)
        idx = {h.strip().lower(): i for i, h in enumerate(hdr)}
        for r in rdr:
            if len(r) != len(hdr) or r[idx["test_type"]] != "NT" or r[idx["test_class_id"]] != "4":
                continue
            if not ("2015" <= r[idx["first_use_date"]][:4] <= "2019"):
                continue
            reg = p22.region(r[idx["postcode_area"]])
            if reg not in ("London", "Scotland"):
                continue
            res = r[idx["test_result"]]
            if res not in ("P", "F", "PRS"):
                continue
            mm = (r[idx["make"]].strip().upper(), r[idx["model"]].strip().upper())
            tally[(reg, mm)][res] += 1
            tally[(reg, ("ALL", "ALL"))][res] += 1
        print(m["name"], "done", flush=True)
    n = lambda t: t["P"] + t["F"] + t["PRS"]
    pairs = defaultdict(int)
    for (reg, mm), t in tally.items():
        if mm != ("ALL", "ALL"):
            pairs[mm] += n(t)
    both = [mm for mm in pairs if ("London", mm) in tally and ("Scotland", mm) in tally]
    top = sorted(both, key=lambda mm: -pairs[mm])[:3]
    rows = []
    for mm in [("ALL", "ALL")] + top:
        L, S = tally[("London", mm)], tally[("Scotland", mm)]
        rows.append({"make_model": " ".join(mm), "london_n": n(L), "scotland_n": n(S),
                     "london_P": rate(L, False), "scotland_P": rate(S, False),
                     "gap_P_only": round(rate(L, False) - rate(S, False), 2),
                     "london_incl_PRS": rate(L, True), "scotland_incl_PRS": rate(S, True),
                     "gap_incl_PRS": round(rate(L, True) - rate(S, True), 2),
                     "london_PRS_share": round(100 * L["PRS"] / n(L), 2), "scotland_PRS_share": round(100 * S["PRS"] / n(S), 2)})
    # mix adjustment over pairs with 30+ tests in both regions: London rates at Scotland's weights
    common = [mm for mm in both if n(tally[("London", mm)]) >= 30 and n(tally[("Scotland", mm)]) >= 30]
    ws = sum(n(tally[("Scotland", mm)]) for mm in common)
    adj = {}
    for prs in (False, True):
        lon = sum(n(tally[("Scotland", mm)]) * rate(tally[("London", mm)], prs) for mm in common) / ws
        sco = sum(n(tally[("Scotland", mm)]) * rate(tally[("Scotland", mm)], prs) for mm in common) / ws
        adj["incl_PRS" if prs else "P_only"] = round(lon - sco, 2)
    out = {"sampled": [m["name"] for m in picks], "mb_per_member": 40, "rows": rows,
           "mix_adjusted": {"pairs": len(common), "scotland_tests_covered": ws, "gap": adj},
           "mean_gap_top3_incl_PRS": round(sum(r["gap_incl_PRS"] for r in rows[1:]) / len(rows[1:]), 2),
           "mean_gap_top3_P_only": round(sum(r["gap_P_only"] for r in rows[1:]) / len(rows[1:]), 2)}
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


main()
