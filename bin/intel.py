#!/usr/bin/env python3
"""Feed for the intelligence lane (3 Oct 2026): it sat empty for twelve days because nothing fed it.

    intel.py queue    every candidate subject not yet covered by a write-up in intel/
    intel.py next     the oldest one, with what the harvest or the vault already knows about it

Candidates come from two places: harvest items judged `intel: true` (field-notes/harvest.jsonl) and
vault verdict lines in field-notes/SEEN.md that name grey-market mechanisms. A candidate is covered
once its harvest id, key or title words appear in any intel/*.md. Read-only.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS")
TERMS = re.compile(r"antidetect|phone farm|device farm|copy-trading|copy trading|drainer|fake review|"
                   r"deepfake|engagement farm|bot farm|cloud phone|account farm|signal group|pump group|"
                   r"inauthentic|posing as a consumer|undetectable", re.I)


def written():
    return " ".join(p.read_text() for p in (ROOT / "intel").glob("*.md") if p.name != "README.md").lower()


def candidates():
    done = written()
    out = []
    for line in open(ROOT / "field-notes/harvest.jsonl"):
        r = json.loads(line)
        if not r.get("intel"):
            continue
        hid = r.get("hid") or r.get("id") or ""
        if hid.lower() in done or r.get("key", "").lower() in done:
            continue
        out.append({"from": "harvest " + hid, "when": r.get("date") or r.get("judged") or "",
                    "subject": r.get("one_line") or r.get("title") or r.get("key"), "mechanism": r.get("mechanism") or ""})
    for i, line in enumerate(open(ROOT / "field-notes/SEEN.md"), 1):
        m = re.match(r"- \*\*(\d{4}-\d\d-\d\d) · (.+?)\*\*", line)
        if m and TERMS.search(line) and m.group(2).lower()[:30] not in done:
            out.append({"from": f"SEEN.md:{i}", "when": m.group(1), "subject": m.group(2), "mechanism": line.strip()[:400]})
    return sorted(out, key=lambda c: c["when"] or "9")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "queue"
    cs = candidates()
    if cmd == "queue":
        print(f"{len(cs)} subjects without a write-up")
        for c in cs:
            print(f"  {c['when'] or '?':10}  {c['from']:14}  {c['subject'][:110]}")
    elif cmd == "next":
        if not cs:
            print("STOP: nothing in the intel queue")
            return
        c = cs[0]
        print(f"NEXT {c['from']} ({c['when']}): {c['subject']}\n\n{c['mechanism']}\n\n"
              "Template and the line that does not move: intel/README.md. Detection is the point.")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
