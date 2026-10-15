#!/usr/bin/env python3
"""Split a saved oversized javascript_tool result into files under field-notes/skool/.

The page returns "SKDUMP" + JSON.stringify({files: {relpath: text}, links: {prefix: [[slug, url], ...]}}).
The harness saves a result over its limit as a JSON array of {type, text} under the session's
tool-results folder; this finds the SKDUMP string in it, writes each file (relative paths only, no
"..") and one <prefix>-videos.tsv per prefix for sandbox/skool_batch_transcribe.py.
Usage: skool_dump_split.py SAVED_RESULT [SAVED_RESULT ...]     (14 Oct 2026)
"""
import json, os, re, sys

OUT = "/Users/triton/PROTEUS/field-notes/skool/"

for src in sys.argv[1:]:
    raw = open(src).read()
    try:
        raw = "".join(i.get("text", "") for i in json.loads(raw))
    except Exception:
        pass
    m = re.search(r'("SKDUMP(?:[^"\\]|\\.)*")', raw, re.S)
    d = json.loads(json.loads(m.group(1))[len("SKDUMP"):])
    n = 0
    for rel, text in d.get("files", {}).items():
        if rel.startswith("/") or ".." in rel.split("/"):
            sys.exit("refused path: " + rel)
        os.makedirs(os.path.dirname(OUT + rel) or OUT, exist_ok=True)
        open(OUT + rel, "w").write(text)
        n += 1
    for prefix, rows in d.get("links", {}).items():
        if rows:
            with open(OUT + prefix + "-videos.tsv", "w") as fh:
                fh.write("".join("%s\t%s\n" % (s, u.replace("?share=copy", "")) for s, u in rows))
    print("%s: %d files, links %s" % (os.path.basename(src), n, {k: len(v) for k, v in d.get("links", {}).items()}))
