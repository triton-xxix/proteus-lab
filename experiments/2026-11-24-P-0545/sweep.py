"""P-0545: mayhem sweep clock, part two. Reads every P-0528 mint with P-0507's burn check and scores the
P-0528 pre-registered rule: hourly at :04 holds if >= 80% of mints with a known birth show a burn as
their newest transaction, each within 3 min of its forecast slot, none more than an hour early.

Keyless public RPC, read only.

    python3 sweep.py
"""
import importlib.util, json, statistics, sys, time, calendar
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = Path("/Users/triton/PROTEUS/experiments")
spec = importlib.util.spec_from_file_location("burns", EXP / "2026-11-20-P-0507/burns.py")
burns = importlib.util.module_from_spec(spec)
spec.loader.exec_module(burns)


def newest_burn(mint):
    """Newest signature, and the newest burn among the last 20 signatures if the newest is not one."""
    sigs = burns.rpc("getSignaturesForAddress", [mint, {"limit": 20}]).get("result") or []
    out = {"n_recent": len(sigs)}
    if not sigs:
        return out
    out["newest_blockTime"] = sigs[0].get("blockTime")
    for i, s in enumerate(sigs[:6]):
        t = burns.rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]).get("result")
        time.sleep(0.4)
        if t and burns.is_burn(t, mint):
            out["burn_blockTime"] = s.get("blockTime")
            out["burn_index"] = i
            return out
    return out


def main():
    if Path("/Users/triton/PROTEUS/HALT").exists():
        print("HALT")
        return 1
    src = json.loads((EXP / "2026-11-22-P-0528/results.json").read_text())
    now = time.time()
    rows = []
    for r in src["rows"]:
        row = {"mint": r["mint"], "birth_utc": r.get("birth_utc"), "forecast": r.get("forecast_burn_utc")}
        row.update(newest_burn(r["mint"]))
        if row.get("burn_blockTime") and row["forecast"]:
            slot = calendar.timegm(time.strptime(row["forecast"], "%Y-%m-%dT%H:%M:%SZ"))
            row["burn_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(row["burn_blockTime"]))
            row["off_slot_min"] = round((row["burn_blockTime"] - slot) / 60, 2)
            if r.get("birth"):
                row["burn_age_h"] = round((row["burn_blockTime"] - r["birth"]) / 3600, 3)
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.5)
    known = [x for x in rows if x["birth_utc"] and x["forecast"]]
    burned = [x for x in known if "off_slot_min" in x]
    newest_is_burn = [x for x in burned if x.get("burn_index") == 0]
    within3 = [x for x in burned if abs(x["off_slot_min"]) <= 3]
    early60 = [x for x in burned if x["off_slot_min"] < -60]
    offs = sorted(x["off_slot_min"] for x in burned)
    ages = sorted(x["burn_age_h"] for x in burned if "burn_age_h" in x)
    rule_pass = len(known) > 0 and len([x for x in within3 if x.get("burn_index") == 0]) / len(known) >= 0.8 and not early60
    summary = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)), "mints": len(rows), "births_known": len(known),
               "burned_any_of_last6": len(burned), "newest_is_burn": len(newest_is_burn), "within_3min": len(within3),
               "share_within_3min_of_known": round(len(within3) / len(known), 3) if known else None,
               "over_1h_early": len(early60), "off_slot_min_sorted": offs,
               "off_slot_min_median": statistics.median(offs) if offs else None,
               "burn_age_h_min": ages[0] if ages else None, "burn_age_h_median": statistics.median(ages) if ages else None,
               "burn_age_h_max": ages[-1] if ages else None,
               "burn_times_utc": sorted(x["burn_utc"] for x in burned), "rule_pass": rule_pass}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
