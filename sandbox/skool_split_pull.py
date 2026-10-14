#!/usr/bin/env python3
"""Split a saved browser_batch result (JSON array of {type, text}) from the Matt Ryder Skool pull into
per-course files under field-notes/skool/. Each text item starts "TEXT MODULES n LEN m\nCOURSE <id>
modules k" followed by "### <module title>\n<text>" sections. Appends a "## Module text" section to
the course's file, creating a stub if the file does not exist.
Usage: skool_split_pull.py RESULTS.json [RESULTS2.json ...]"""
import json, os, re, sys

OUT = "/Users/triton/PROTEUS/field-notes/skool/"
NAMES = {"6a043627": "01-start-here", "80c6d0e7": "02-sales-fundamentals", "21b89d83": "03-objection-handling",
         "e025b868": "04-scripting", "3425e97d": "08-b2b-index-locked", "e9f2d43a": "09-selling-with-stories",
         "8c1f1c70": "11-sales-management", "eec9e4a4": "12-business-mastery"}

for path in sys.argv[1:]:
    items = json.load(open(path))
    for it in items:
        raw = it.get("text", "")
        # the JS result arrives as a JSON string literal after the tool tag; unwrap it
        q = re.search(r'\[javascript_tool:javascript_exec\] ("(?:[^"\\]|\\.)*")', raw, re.S)
        t = json.loads(q.group(1)) if q else raw
        m = re.search(r"COURSE (\w+) modules (\d+)", t)
        if not m:
            continue
        cid, nmod = m.group(1), m.group(2)
        head = re.search(r"TEXT MODULES (\d+) LEN (\d+)", t)
        ntext = head.group(1) if head else "?"
        body = t[m.end():].strip("\n")
        name = NAMES.get(cid, cid)
        fp = OUT + "mattryder-%s.md" % name
        if not os.path.exists(fp):
            open(fp, "w").write("# mattryder/%s\n\nPulled from Skool on 2026-10-14 through the built-in browser pane (luke-boyd-4592).\n" % cid)
        with open(fp, "a") as fh:
            fh.write("\n\n## Module text (fetched per module through the page data route, %s of %s modules carry text)\n\n" % (ntext, nmod))
            fh.write(body.strip() + "\n")
        print("%s: %s text modules of %s -> %s (+%d chars)" % (cid, ntext, nmod, fp, len(body)))
