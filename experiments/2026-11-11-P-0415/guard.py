"""P-0415: what a stale-entry guard would have skipped in the v0.2 Grinder book.

Reads experiments/2026-11-11-P-0405/results.json (89 rows, each with the ledger entry's gap to the first
candle open, the snapshot's age, and the P and L at 100 pounds a trade walked two ways). No fetch, no
re-walk. A guard skips a trade; the totals are what is left.
"""
import json
import sys

rows = json.load(open("/Users/triton/PROTEUS/experiments/2026-11-11-P-0405/results.json"))["rows"]
rows = [r for r in rows if r.get("ledger_pnl_100") is not None and r.get("candle_pnl_100") is not None]


def line(name, skip):
    gone = [r for r in rows if skip(r)]
    kept = [r for r in rows if not skip(r)]
    return {"guard": name, "skipped": len(gone), "kept": len(kept),
            "skipped_ledger_total": round(sum(r["ledger_pnl_100"] for r in gone), 2),
            "skipped_candle_total": round(sum(r["candle_pnl_100"] for r in gone), 2),
            "skipped_winners_ledger": sum(1 for r in gone if r["ledger_pnl_100"] > 0),
            "kept_ledger_total": round(sum(r["ledger_pnl_100"] for r in kept), 2),
            "kept_candle_total": round(sum(r["candle_pnl_100"] for r in kept), 2),
            "kept_ledger_mean": round(sum(r["ledger_pnl_100"] for r in kept) / len(kept), 2) if kept else None,
            "skipped_ledger_mean": round(sum(r["ledger_pnl_100"] for r in gone) / len(gone), 2) if gone else None,
            "skipped_ids": [r["id"] for r in gone] if len(gone) <= 20 else None}


out = {"rows": len(rows), "lines": [line("none", lambda r: False)]}
for g in (5, 10, 20):
    out["lines"].append(line("gap over %d%% either way" % g, lambda r, g=g: abs(r["gap_pct"]) > g))
    out["lines"].append(line("entry over %d%% above the candle" % g, lambda r, g=g: r["gap_pct"] > g))
for a in (6, 10, 15):
    out["lines"].append(line("snapshot over %d min old" % a, lambda r, a=a: r["snapshot_age_min"] is not None and r["snapshot_age_min"] > a))
# sign check: which way does gap_pct run? Print G-0078, known to have been bought far above the market.
out["sign_check_G-0078"] = next(({"gap_pct": r["gap_pct"], "entry_ledger": r["entry_ledger"], "entry_candle": r["entry_candle"]} for r in rows if r["id"] == "G-0078"), None)
json.dump(out, open(sys.argv[1], "w"), indent=1)
print("rows", len(rows), "sign check", out["sign_check_G-0078"])
for l in out["lines"]:
    print("%-34s skipped %2d (winners %d, ledger %+9.2f, mean %s) | left: ledger %+9.2f candle %+9.2f mean %s" % (
        l["guard"], l["skipped"], l["skipped_winners_ledger"], l["skipped_ledger_total"], l["skipped_ledger_mean"],
        l["kept_ledger_total"], l["kept_candle_total"], l["kept_ledger_mean"]))
