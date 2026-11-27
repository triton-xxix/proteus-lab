#!/usr/bin/env python3
"""Lint the list-churn page: tags balance, local links exist, 4 bar rows, 6 rename rows, headline numbers
from the runs, no em dash, nothing undefined. Usage: lint.py [file]  (default index.html beside this)."""
import json
import os
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html")
body = open(path, encoding="utf-8").read()
m = json.load(open(os.path.join(HERE, "run-mcp-27oct-27nov.json")))["summary"]
VOID = {"meta", "br", "img", "input", "link", "hr"}
errs = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.links, self.tr = [], [], 0

    def handle_starttag(self, t, a):
        if t == "a":
            self.links.append(dict(a).get("href", ""))
        if t == "tr":
            self.tr += 1
        if t not in VOID:
            self.stack.append(t)

    def handle_endtag(self, t):
        if t in VOID:
            return
        if not self.stack or self.stack[-1] != t:
            errs.append("tag mismatch at </%s>, open %s" % (t, self.stack[-3:]))
        else:
            self.stack.pop()


p = P()
p.feed(body)
if p.stack:
    errs.append("unclosed %s" % p.stack)
if body.count('class="row"') != 4:
    errs.append("want 4 bar rows")
if p.tr != 1 + 6 + 1 + 6:
    errs.append("%d table rows, want 14" % p.tr)
for h in p.links:
    if h.startswith(("http", "../")):
        continue
    if os.path.basename(path) == "index.html" and not os.path.exists(os.path.join(HERE, h)):
        errs.append("missing local link " + h)
for want in ["<b>%d</b>" % m["added_raw"], "<b>%d</b>" % m["added_net"], "Real removals: <b>0</b>",
             "Removed, or renamed?", "koda-ai-studio/agent-bom"]:
    if want not in body:
        errs.append("missing %r" % want)
if "—" in body:
    errs.append("em dash")
if "undefined" in body or ">None<" in body or "<b>None" in body or "NaN" in body:
    errs.append("undefined, None or NaN in body")
print("LINT OK" if not errs else "LINT FAIL\n" + "\n".join(errs))
sys.exit(1 if errs else 0)
