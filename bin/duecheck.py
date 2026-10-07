#!/usr/bin/env python3
"""Every pre-registered test in DUE.md, judged against its due date, one line each.

Written 8 Oct 2026, the night Luke asked why the round-2 Grinder replay (pre-registered 30 Sep)
had never been run. killcheck.py says KILL or KEEP for books; this says DUE or WAITING for tests.
Read-only unless asked:
  --log     append the summary line to today's run log
  --queue   add a desk probe for every overdue row that has none, and write its id into DUE.md
  --scored D-00N "date, artefact"   close a row

A row is overdue when `scored` is blank and today is at or past the backstop date in `due`
(the last YYYY-MM-DD in that cell). A data condition without a backstop never fires; write one.
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS")
DUE = ROOT / "DUE.md"
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def rows():
    out = []
    for line in DUE.read_text().splitlines():
        if not line.startswith("| D-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7:
            continue
        out.append(dict(zip(["id", "registered", "what", "where", "due", "scored", "probe"], cells), raw=line))
    return out


def backstop(due):
    ds = DATE.findall(due)
    return date.fromisoformat(ds[-1]) if ds else None


def judge(today):
    lines = []
    overdue = []
    for r in rows():
        if r["scored"]:
            continue
        b = backstop(r["due"])
        if b is None:
            word = "NO BACKSTOP"
        elif today >= b:
            word = "DUE (%d days past %s)" % ((today - b).days, b) if today > b else "DUE today"
            overdue.append(r)
        else:
            word = "waiting (%s, %d days)" % (b, (b - today).days)
        lines.append("%s: %s. %s%s" % (r["id"], word, r["what"][:90], (" [%s]" % r["probe"]) if r["probe"] else ""))
    return lines, overdue


def queue(overdue):
    text = DUE.read_text()
    for r in overdue:
        if r["probe"]:
            continue
        title = "%s (DUE.md %s): %s" % (r["what"][:110], r["id"], r["where"])
        p = subprocess.run([sys.executable, str(ROOT / "bin/probe.py"), "add", title, "--source", "desk", "--est", "40",
                            "--repeat-ok", "pre-registered test from DUE.md, never scored"], capture_output=True, text=True)
        m = re.search(r"added (P-\d+)", p.stdout)
        if m:
            cells = r["raw"].strip("|").split("|")
            cells[6] = " %s " % m.group(1)
            text = text.replace(r["raw"], "|" + "|".join(cells) + "|")
            print("queued", r["id"], "as", m.group(1))
        else:
            print("could not queue", r["id"], (p.stdout + p.stderr).strip()[-300:])
    DUE.write_text(text)


def mark_scored(rid, note):
    text = DUE.read_text()
    for r in rows():
        if r["id"] == rid:
            cells = r["raw"].strip("|").split("|")
            cells[5] = " %s " % note
            text = text.replace(r["raw"], "|" + "|".join(cells) + "|")
            DUE.write_text(text)
            print("scored", rid)
            return
    print("no row", rid)


def main():
    today = date.today()
    if "--scored" in sys.argv:
        i = sys.argv.index("--scored")
        return mark_scored(sys.argv[i + 1], sys.argv[i + 2])
    lines, overdue = judge(today)
    summary = "Due check: %d open, %d DUE%s" % (len(lines), len(overdue), (": " + ", ".join(r["id"] for r in overdue)) if overdue else "")
    print("\n".join(lines))
    print(summary)
    if "--queue" in sys.argv and overdue:
        queue(overdue)
    if "--log" in sys.argv:
        log = ROOT / "state/runs" / (today.isoformat() + ".md")
        with open(log, "a") as fh:
            fh.write("- %s\n" % summary)


if __name__ == "__main__":
    main()
