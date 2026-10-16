"""P-0167: how often does the harvest child break its own prompt's hard field rules?

Reads every state/agents/<date>/harvest.json and checks each item against rules stated in the
child prompt (bin/harvest.py). Writes violations.csv and summary.json next to this file.
Rules that came in later (the breakdown fields, 29 Sep) are only checked from their first appearance.
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS/state/agents")
OUT = Path(__file__).resolve().parent
LENS = {"mechanism", "vendor", "both"}
INTEREST = {"mechanism-hunting", "forecasting", "game-bots", "open-data", "tools-for-strangers", "cars", "tech",
            "desk:grinder", "desk:pitch", "none"}
IDEA = {"sound", "unsound", "needs-a-run"}
BASE = ["key", "keep", "skip_reason", "lens", "mechanism", "claim", "testable", "why_not_testable",
        "verdict_question", "needs", "intel", "interest", "one_line"]
KEPT_LATER = ["idea", "idea_why", "breakdown", "tools_have", "tools_fetch", "missing"]


def words(s):
    return len(re.findall(r"\S+", s or ""))


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def check(it, later):
    bad = []
    for f in BASE:
        if f not in it:
            bad.append(f"missing:{f}")
    if it.get("keep") and later:
        for f in KEPT_LATER:
            if f not in it:
                bad.append(f"missing:{f}")
    if words(it.get("one_line")) >= 30:
        bad.append("one_line>=30 words")
    if any("—" in s for s in strings(it)):
        bad.append("em dash")
    if it.get("testable"):
        if len(it.get("probe_title") or "") >= 140:
            bad.append("probe_title>=140")
        if not it.get("probe_title"):
            bad.append("testable without probe_title")
        e = it.get("est_minutes")
        if not isinstance(e, (int, float)) or not 10 <= e <= 30:
            bad.append("est_minutes outside 10-30")
    elif not it.get("why_not_testable"):
        bad.append("untestable without why_not_testable")
    if it.get("keep") is False and not it.get("skip_reason"):
        bad.append("skipped without skip_reason")
    if it.get("lens") not in LENS:
        bad.append("lens not in set")
    if it.get("interest") not in INTEREST:
        bad.append("interest not in set")
    if it.get("keep") and later and it.get("idea") not in IDEA:
        bad.append("idea not in set")
    return bad


def main():
    rows, per_file, rules = [], [], Counter()
    later = False
    for p in sorted(ROOT.glob("2026-*/harvest.json")):
        try:
            items = json.loads(p.read_text())
        except Exception as e:  # noqa: BLE001
            per_file.append({"date": p.parent.name, "items": 0, "error": str(e)[:80]})
            continue
        if not later and any("breakdown" in it for it in items if isinstance(it, dict)):
            later = True
        n_bad = 0
        for it in items:
            bad = check(it, later)
            if bad:
                n_bad += 1
                rules.update(bad)
                rows.append([p.parent.name, it.get("key"), "; ".join(bad)])
        per_file.append({"date": p.parent.name, "items": len(items), "items_breaking": n_bad})
    total = sum(f.get("items", 0) for f in per_file)
    breaking = sum(f.get("items_breaking", 0) for f in per_file)
    with open(OUT / "violations.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "key", "violations"])
        w.writerows(rows)
    summary = {"files": len(per_file), "items": total, "items_breaking_a_rule": breaking,
               "share": round(breaking / total, 4) if total else None, "by_rule": rules.most_common(),
               "per_file": per_file}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "per_file"}, indent=1))
    for f in per_file:
        print(f)


if __name__ == "__main__":
    main()
