"""P-0217: score the findings cycle against the SRE postmortem standard.

For each row of state/loop/findings.jsonl: has it a fix commit, a check (verify_note), and a stated cause
(a causal word in fix_note or verify_note)? Did it recur (reopened_at set, or status reopened)?
The cause test is a keyword match, so it is printed per row for a hand check.
Run: python3 -I score.py <findings.jsonl> <out.json>
"""
import collections
import json
import re
import sys

CAUSE = re.compile(r"\b(because|cause[ds]?|root|since|why|due to|came from|was (?:the|that|caused)|so the|meant)\b", re.I)


def main():
    rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    status = collections.Counter(r.get("status") for r in rows)
    fixed = [r for r in rows if r.get("fix_commit") or r.get("fixed_at")]
    out_rows = []
    for r in fixed:
        text = (r.get("fix_note") or "") + " " + (r.get("verify_note") or "")
        m = CAUSE.search(text)
        out_rows.append({
            "id": r["id"],
            "status": r.get("status"),
            "severity": r.get("severity"),
            "seen": r.get("seen"),
            "commit": bool(r.get("fix_commit")),
            "check": bool(r.get("verify_note")),
            "cause": bool(m),
            "cause_word": m.group(0) if m else "",
            "recurred": bool(r.get("reopened_at")) or r.get("status") == "reopened",
        })
    full = [x for x in out_rows if x["commit"] and x["check"] and x["cause"]]

    def rate(xs):
        return [sum(x["recurred"] for x in xs), len(xs)]

    with_cause = [x for x in out_rows if x["cause"]]
    without = [x for x in out_rows if not x["cause"]]
    seen_c = [x["seen"] or 0 for x in with_cause]
    seen_n = [x["seen"] or 0 for x in without]
    out = {
        "rows": len(rows),
        "status": dict(status),
        "fixed": len(fixed),
        "with_commit": sum(x["commit"] for x in out_rows),
        "with_check": sum(x["check"] for x in out_rows),
        "with_cause": len(with_cause),
        "all_three": len(full),
        "share_all_three": round(len(full) / len(fixed), 3) if fixed else None,
        "recurred_with_cause": rate(with_cause),
        "recurred_without_cause": rate(without),
        "mean_seen_with_cause": round(sum(seen_c) / len(seen_c), 2) if seen_c else None,
        "mean_seen_without_cause": round(sum(seen_n) / len(seen_n), 2) if seen_n else None,
        "per_row": out_rows,
    }
    with open(sys.argv[2], "w") as f:
        json.dump(out, f, indent=1)
    for k, v in out.items():
        if k != "per_row":
            print(k, v)
    for x in out_rows:
        print(x["id"], x["status"], "seen", x["seen"], "commit" if x["commit"] else "-",
              "check" if x["check"] else "-", ("cause:" + x["cause_word"]) if x["cause"] else "-",
              "RECURRED" if x["recurred"] else "")


main()
