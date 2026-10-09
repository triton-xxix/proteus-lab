#!/usr/bin/env python3
"""The daytime loop's shared register of things found wrong, and what became of each.

Written 9 Oct 2026. The Inspector adds findings, Smith fixes them, the next Inspector checks the fix
held. Until then a problem lived in one night's run log and was found again by hand (BACKLOG.md
says so twice). One JSON object a line in state/loop/findings.jsonl:

  add    --source S --desk D --severity high|med|low --title T --evidence E
         An open finding with the same desk and title is not duplicated; its `seen` count goes up.
  list   [--status open|fixed|verified|wontfix|all]        newest last, open by default
  top    [--n 3]       open findings for Smith: severity, then most seen, at most one per desk
  fix    F-0001 --commit HASH --note "what changed"         Smith, after committing the fix
  verify F-0001 --held yes|no --note "what was checked"     the next Inspector; "no" reopens it
  wontfix F-0001 --note "why"

Statuses: open -> fixed -> verified, or back to open when a fix did not hold.
"""
import argparse
import json
import os
import sys
from datetime import datetime

ROOT = "/Users/triton/PROTEUS/"
PATH = os.environ.get("PROTEUS_FINDINGS") or ROOT + "state/loop/findings.jsonl"   # override: tests only
SEV = {"high": 0, "med": 1, "low": 2}


def now():
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M%z")


def load():
    try:
        with open(PATH) as fh:
            return [json.loads(l) for l in fh if l.strip()]
    except FileNotFoundError:
        return []


def save(rows):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    tmp = PATH + ".tmp"
    with open(tmp, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    os.replace(tmp, PATH)


def find(rows, fid):
    for r in rows:
        if r["id"] == fid:
            return r
    sys.exit("no finding %s" % fid)


def show(r):
    return "%s [%s %s] %s: %s (seen %d)%s" % (
        r["id"], r["status"], r["severity"], r["desk"], r["title"], r.get("seen", 1),
        (" fix " + r["fix_commit"]) if r.get("fix_commit") else "")


def cmd_add(a):
    rows = load()
    for r in rows:
        if r["status"] == "open" and r["desk"] == a.desk and r["title"] == a.title:
            r["seen"] = r.get("seen", 1) + 1
            r["last_seen"] = now()
            r["evidence"] = a.evidence
            save(rows)
            print("SEEN AGAIN " + show(r))
            return
    n = max([int(r["id"][2:]) for r in rows] or [0]) + 1
    r = {"id": "F-%04d" % n, "at": now(), "source": a.source, "desk": a.desk, "severity": a.severity,
         "title": a.title, "evidence": a.evidence, "status": "open", "seen": 1}
    rows.append(r)
    save(rows)
    print("ADDED " + show(r))


def cmd_list(a):
    for r in load():
        if a.status == "all" or r["status"] == a.status:
            print(show(r))


def cmd_top(a):
    opened = [r for r in load() if r["status"] == "open"]
    opened.sort(key=lambda r: (SEV.get(r["severity"], 9), -r.get("seen", 1), r["id"]))
    out, desks = [], set()
    for r in opened:
        if r["desk"] in desks:
            continue
        desks.add(r["desk"])
        out.append(r)
        if len(out) >= a.n:
            break
    for r in out:
        print(show(r))
        print("    evidence: " + r["evidence"])
    if not out:
        print("NONE open")


def cmd_fix(a):
    rows = load()
    r = find(rows, a.id)
    r.update(status="fixed", fix_commit=a.commit, fix_note=a.note, fixed_at=now())
    save(rows)
    print("FIXED " + show(r))


def cmd_verify(a):
    rows = load()
    r = find(rows, a.id)
    if r["status"] != "fixed":
        sys.exit("%s is %s, not fixed" % (r["id"], r["status"]))
    if a.held == "yes":
        r.update(status="verified", verified_at=now(), verify_note=a.note)
    else:
        r.update(status="open", reopened_at=now(), verify_note=a.note, seen=r.get("seen", 1) + 1)
    save(rows)
    print(("VERIFIED " if a.held == "yes" else "REOPENED ") + show(r))


def cmd_wontfix(a):
    rows = load()
    r = find(rows, a.id)
    r.update(status="wontfix", note=a.note, closed_at=now())
    save(rows)
    print("WONTFIX " + show(r))


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add")
    s.add_argument("--source", required=True)
    s.add_argument("--desk", required=True)
    s.add_argument("--severity", required=True, choices=sorted(SEV))
    s.add_argument("--title", required=True)
    s.add_argument("--evidence", required=True)
    s.set_defaults(fn=cmd_add)
    s = sub.add_parser("list")
    s.add_argument("--status", default="open", choices=("open", "fixed", "verified", "wontfix", "all"))
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("top")
    s.add_argument("--n", type=int, default=3)
    s.set_defaults(fn=cmd_top)
    s = sub.add_parser("fix")
    s.add_argument("id")
    s.add_argument("--commit", required=True)
    s.add_argument("--note", required=True)
    s.set_defaults(fn=cmd_fix)
    s = sub.add_parser("verify")
    s.add_argument("id")
    s.add_argument("--held", required=True, choices=("yes", "no"))
    s.add_argument("--note", required=True)
    s.set_defaults(fn=cmd_verify)
    s = sub.add_parser("wontfix")
    s.add_argument("id")
    s.add_argument("--note", required=True)
    s.set_defaults(fn=cmd_wontfix)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
