#!/usr/bin/env python3
"""list-churn: diff two versions of an awesome list and check every "removed" repo before you count it.

A plain diff of GitHub links counts a renamed or transferred repo twice: once removed (the old name),
once added (the new one). This asks the GitHub API about each removed name (keyless, it follows the
redirect) and sorts it into: moved and re-listed, moved and not re-listed, archived, deleted or private,
or live and dropped by the curator. Only the last four are real removals.

Usage:
  list_churn.py OLD NEW [--out run.json] [--max 50] [--sleep 0.5]
  list_churn.py --from run.json            re-score a saved run, no network

OLD and NEW are each a path or an https URL to a README (markdown) or a .links file (one owner/repo a
line). Keyless GitHub allows 60 calls an hour; --max caps how many removed names are checked (the rest
are counted as unchecked, never guessed). Standard library only. From Proteus probes P-0576 and P-0585.
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.request

LINK = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?:[/#)\s\]]|$)")
NOT_REPOS = {"sponsors", "topics", "orgs", "features", "site", "apps", "marketplace", "settings"}
UA = {"User-Agent": "list-churn/1.0", "Accept": "application/vnd.github+json"}


def read(src):
    if src.startswith("https://"):
        with urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": UA["User-Agent"]}), timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    with open(src, encoding="utf-8") as fh:
        return fh.read()


def links(text):
    if "github.com/" in text:
        names = (m.group(1) for m in LINK.finditer(text))
    else:
        names = (l.strip() for l in text.split() if l.count("/") == 1)
    out = set()
    for n in names:
        n = n.lower()
        if n.endswith(".git"):
            n = n[:-4]
        if n.split("/")[0] not in NOT_REPOS:
            out.add(n)
    return out


def ask(name):
    req = urllib.request.Request("https://api.github.com/repos/" + name, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:  # network trouble is recorded, never guessed
        return "error:" + type(e).__name__, None


def classify(row, new):
    st = row["status"]
    if st == 404:
        return "deleted or private"
    if st != 200:
        return "unchecked"
    if row["full_name"].lower() != row["listed"]:
        return "moved, re-listed" if row["full_name"].lower() in new else "moved, not re-listed"
    if row["archived"]:
        return "archived"
    return "live, dropped"


CLASSES = ["moved, re-listed", "moved, not re-listed", "archived", "deleted or private", "live, dropped", "unchecked"]
REAL = ["moved, not re-listed", "archived", "deleted or private", "live, dropped"]


def summarise(run):
    new = set(run["new"])
    tally = {c: 0 for c in CLASSES}
    for r in run["rows"]:
        r["class"] = classify(r, new) if "status" in r else "unchecked"
        tally[r["class"]] += 1
    added = len(set(run["new"]) - set(run["old"]))
    removed = len(run["rows"])
    relisted = tally["moved, re-listed"]
    return {
        "old": len(run["old"]), "new": len(run["new"]), "added_raw": added, "removed_raw": removed,
        "tally": tally, "real_removals": sum(tally[c] for c in REAL), "unchecked": tally["unchecked"],
        "added_net": added - relisted, "renames_counted_twice": relisted,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("old", nargs="?")
    ap.add_argument("new", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--from", dest="frm")
    ap.add_argument("--max", type=int, default=50)
    ap.add_argument("--sleep", type=float, default=0.5)
    a = ap.parse_args()
    if a.frm:
        run = json.load(open(a.frm))
    else:
        if not (a.old and a.new):
            ap.error("give OLD and NEW, or --from")
        old, new = links(read(a.old)), links(read(a.new))
        rows = []
        for i, name in enumerate(sorted(old - new)):
            row = {"listed": name}
            if i < a.max:
                st, j = ask(name)
                row["status"] = st
                if j:
                    row.update(full_name=j["full_name"], archived=j["archived"], pushed=j["pushed_at"],
                               stars=j["stargazers_count"])
                time.sleep(a.sleep)
            rows.append(row)
        run = {"pulled_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
               "old_src": a.old, "new_src": a.new, "old": sorted(old), "new": sorted(new), "rows": rows}
    run["summary"] = summarise(run)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(run, fh, indent=1)
    s = run["summary"]
    print("old %d, new %d: added %d, removed %d by URL" % (s["old"], s["new"], s["added_raw"], s["removed_raw"]))
    for c in CLASSES:
        if s["tally"][c]:
            print("  %-22s %d" % (c, s["tally"][c]))
    print("real removals %d, net additions %d (%d renames counted twice by the plain diff)"
          % (s["real_removals"], s["added_net"], s["renames_counted_twice"]))
    for r in run["rows"]:
        if r["class"] != "unchecked":
            print("  %s -> %s (%s)" % (r["listed"], r.get("full_name", "-"), r["class"]))


if __name__ == "__main__":
    sys.exit(main())
