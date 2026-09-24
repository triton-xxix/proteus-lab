#!/usr/bin/env python3
"""P-0001: do rugcheck's insider flags mark the tokens the Grinder's gate lets through?

Reads the latest snapshot in grinder/SNAPSHOTS.csv, applies grinder/paper.py's passes() unchanged,
refetches the full rugcheck report for every gate-passer, every open ledger position and a sample
of non-passers, and reports graphInsidersDetected, insider-flagged top holders and insider-named
risks for each. Nothing here changes a rule. Output: REPORT.md next to this file.
"""
import csv, importlib.util, json, random, sys, time, urllib.request
ROOT = "/Users/triton/PROTEUS/"
spec = importlib.util.spec_from_file_location("paper", ROOT + "grinder/paper.py")
paper = importlib.util.module_from_spec(spec); spec.loader.exec_module(paper)

rows = list(csv.DictReader(open(ROOT + "grinder/SNAPSHOTS.csv")))
latest = max(r["ts"] for r in rows if r["ts"].startswith("20"))
snap = [r for r in rows if r["ts"] == latest]
passers = [r for r in snap if paper.passes(r)]
ledger = list(csv.DictReader(open(ROOT + "grinder/LEDGER.csv")))
open_pos = {r["mint"]: r["id"] for r in ledger if not r.get("exit_at")}
random.seed(1)
others = random.sample([r for r in snap if not paper.passes(r)], min(30, len(snap) - len(passers)))

def report(mint):
    req = urllib.request.Request("https://api.rugcheck.xyz/v1/tokens/%s/report" % mint,
                                 headers={"User-Agent": "proteus-probe/0.1"})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)
        except Exception as e:
            err = e
            time.sleep(2)
    return {"_error": str(err)[:80]}

out = []
for group, rs in (("gate-passers", passers), ("non-passers sample", others)):
    for r in rs:
        rep = report(r["mint"]); time.sleep(0.8)
        th = rep.get("topHolders") or []
        out.append({
            "group": group, "symbol": r["symbol"], "mint": r["mint"], "position": open_pos.get(r["mint"], ""),
            "graphInsidersDetected": rep.get("graphInsidersDetected"),
            "insider_holders": sum(1 for h in th if h.get("insider")),
            "insider_pct": round(sum(float(h.get("pct") or 0) for h in th if h.get("insider")), 2),
            "insider_risks": [x.get("name") for x in rep.get("risks") or [] if "insider" in (x.get("name") or "").lower()],
            "score": rep.get("score_normalised"), "error": rep.get("_error"),
        })
json.dump({"snapshot": latest, "rows": len(snap), "passers": len(passers), "results": out},
          open(ROOT + "experiments/2026-09-24-P-0001/results.json", "w"), indent=1)

def n(g, key): return sum(1 for o in out if o["group"] == g and (o[key] or 0) > 0)
lines = ["# P-0001: rugcheck insider flags on the Grinder's gate-passers", "",
         "Snapshot %s, %d rows, %d pass the v0.1 gate. Rugcheck report refetched %s." % (
             latest, len(snap), len(passers), time.strftime("%Y-%m-%d %H:%M")), ""]
for g in ("gate-passers", "non-passers sample"):
    tot = sum(1 for o in out if o["group"] == g and not o["error"])
    lines.append("- %s: %d fetched; graphInsidersDetected > 0 on %d; insider-flagged top holders on %d; insider-named risks on %d." % (
        g, tot, n(g, "graphInsidersDetected"), n(g, "insider_holders"), sum(1 for o in out if o["group"] == g and o["insider_risks"])))
lines += ["", "| group | symbol | position | graphInsidersDetected | insider holders | insider pct | insider risks | score |", "|---|---|---|---|---|---|---|---|"]
for o in out:
    lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
        o["group"], o["symbol"], o["position"], o["graphInsidersDetected"], o["insider_holders"],
        o["insider_pct"], ", ".join(o["insider_risks"]) or "", o["score"] if not o["error"] else "ERR " + o["error"]))
open(ROOT + "experiments/2026-09-24-P-0001/REPORT.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines[:8]))
