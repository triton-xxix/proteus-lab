"""P-0403: the Grinder books' bankrolls recomputed from their ledgers, and when each first fell below
one stake. Read-only; imports the desk's RULES and gate. Prints and writes results.json."""
import csv, json, sys
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper  # noqa: E402

HERE = Path(__file__).resolve().parent
R, fnum = paper.RULES, paper.fnum
out = {}
for name, path, version in (("v0.2", "/Users/triton/PROTEUS/grinder/LEDGER.csv", R["version"]),
                            ("R01", "/Users/triton/PROTEUS/grinder/LEDGER-R01.csv", None)):
    rows = list(csv.DictReader(open(path)))
    book = [r for r in rows if version is None or r.get("rule_version") == version]
    closed = sorted((r for r in book if r.get("exit_at") and r.get("pnl_gbp")), key=lambda r: r["exit_at"])
    bank, first_below = R["bankroll_gbp"], None
    for r in closed:
        bank += fnum(r["pnl_gbp"]) or 0
        if first_below is None and bank < R["size_gbp"]:
            first_below = r["exit_at"]
    still = [r for r in book if not r.get("exit_at")]
    bank -= R["size_gbp"] * len(still)
    entries = sorted(r["entered_at"] for r in book)
    out[name] = {"rows": len(book), "closed": len(closed), "open": len(still), "start": R["bankroll_gbp"],
                 "realised": round(bank - R["bankroll_gbp"] + R["size_gbp"] * len(still), 2),
                 "bankroll_now": round(bank, 2), "stake": R["size_gbp"], "first_below_stake_at": first_below,
                 "last_entry": entries[-1] if entries else None,
                 "entries_after_first_below": sum(1 for e in entries if first_below and e > first_below)}

snap = paper.latest_snapshot() or []
held = {r["mint"] for r in csv.DictReader(open("/Users/triton/PROTEUS/grinder/LEDGER.csv"))}
passers = [s for s in snap if paper.passes(s)]
out["tonight"] = {"snapshot_rows": len(snap), "pass_every_gate": len(passers),
                  "of_those_never_held": sum(1 for s in passers if s["mint"] not in held)}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
