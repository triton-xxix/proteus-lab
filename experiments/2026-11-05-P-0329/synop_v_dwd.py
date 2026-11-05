"""P-0329: Munich-Stadt (WMO 10865, DWD 03379) 12 h SYNOP max v DWD daily TX, October 2026.

SYNOP: the 18 UTC AAXX report's section 3 group 1snTxTxTx (maximum 06 to 18 UTC), from Ogimet.
DWD: the daily maximum the exchange scoring already uses (munich_forecast_error.observed).
Usage: python3 -I synop_v_dwd.py OGIMET.txt OUT.json
"""
import importlib.util
import json
import statistics
import sys

ROOT = "/Users/triton/PROTEUS"
src, out = sys.argv[1], sys.argv[2]

synop = {}
for line in open(src):
    parts = line.strip().split(",")
    if len(parts) < 7 or parts[4] != "18" or parts[5] != "00" or not parts[6].startswith("AAXX"):
        continue
    groups = parts[6].replace("==", "").split()
    if "333" not in groups:
        continue
    for g in groups[groups.index("333") + 1:]:
        if len(g) == 5 and g[0] == "1" and g[1] in "01" and g[2:].isdigit():
            v = int(g[2:]) / 10.0
            synop["%s-%s-%s" % (parts[1], parts[2], parts[3])] = -v if g[1] == "1" else v
            break

# Fallback, found 5 Nov: from 3 Oct the 18 UTC report carries no 1snTxTxTx group. So also take the
# highest section-1 air temperature (1sTTT) of every AAXX report in the UTC day (10-minute reports).
inst = {}
for line in open(src):
    parts = line.strip().split(",")
    if len(parts) < 7 or not parts[6].startswith("AAXX"):
        continue
    groups = parts[6].replace("==", "").split()
    if "555" in groups:
        continue  # a second report stream under 10865 (same shape as the OOXX lines), up to 6 C off DWD
    sec1 = groups[5:groups.index("333")] if "333" in groups else groups[5:]
    for g in sec1:
        if len(g) == 5 and g[0] == "1" and g[1] in "01" and g[2:].isdigit():
            v = int(g[2:]) / 10.0 * (-1 if g[1] == "1" else 1)
            day = "%s-%s-%s" % (parts[1], parts[2], parts[3])
            inst[day] = max(inst.get(day, -99), v)
            break

spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)
dwd = mfe.observed("10865")

days = sorted(d for d in synop if d in dwd)
gaps = [dwd[d] - synop[d] for d in days]


def deg(x):
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


same = sum(deg(dwd[d]) == deg(synop[d]) for d in days)
res = {
    "synop_days": len(synop), "dwd_days_matched": len(days),
    "first": days[0] if days else None, "last": days[-1] if days else None,
    "mean_dwd_minus_synop": round(statistics.mean(gaps), 3) if gaps else None,
    "sd": round(statistics.pstdev(gaps), 3) if gaps else None,
    "max_gap": round(max(gaps), 2) if gaps else None, "min_gap": round(min(gaps), 2) if gaps else None,
    "days_dwd_higher_by_0.5_plus": sum(g >= 0.5 for g in gaps),
    "same_whole_degree": same,
    "rows": [{"day": d, "dwd": dwd[d], "synop_06_18": synop[d]} for d in days],
}
idays = sorted(d for d in inst if d in dwd)
ig = [dwd[d] - inst[d] for d in idays]
res["ten_minute_max"] = {
    "days": len(idays),
    "mean_dwd_minus_10min_max": round(statistics.mean(ig), 3) if ig else None,
    "sd": round(statistics.pstdev(ig), 3) if ig else None,
    "min_gap": round(min(ig), 2) if ig else None, "max_gap": round(max(ig), 2) if ig else None,
    "same_whole_degree": sum(deg(dwd[d]) == deg(inst[d]) for d in idays),
    "rows": [{"day": d, "dwd": dwd[d], "max_10min": inst[d]} for d in idays],
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1)[:1500])
print({k: v for k, v in res["ten_minute_max"].items() if k != "rows"})
