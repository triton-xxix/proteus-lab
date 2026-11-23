#!/usr/bin/env python3
"""Lint the trade-finder page: tags balance, local links exist, counts and headline numbers present,
no firm names in the body, no em dash. Usage: lint.py [file]  (default index.html beside this)."""
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html")
body = open(path, encoding="utf-8").read()
run = json.load(open(os.path.join(HERE, "..", "..", "..", "experiments", "2026-11-23-lead-finder", "run-2026-11-23.json")))
s = run["summary"]
VOID = {"meta", "br", "img", "input", "link", "hr", "rect", "circle", "path"}
errs = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.links, self.dots = [], [], 0

    def handle_starttag(self, t, a):
        if t == "circle":
            self.dots += 1
        if t == "a":
            self.links.append(dict(a).get("href", ""))
        if t not in VOID:
            self.stack.append(t)

    def handle_startendtag(self, t, a):
        if t == "circle":
            self.dots += 1

    def handle_endtag(self, t):
        if t in VOID:
            return
        if not self.stack or self.stack[-1] != t:
            errs.append(f"tag mismatch at </{t}>, open {self.stack[-3:]}")
        else:
            self.stack.pop()


p = P()
p.feed(body)
if p.stack:
    errs.append(f"unclosed {p.stack}")
if p.dots != s["firms"]:
    errs.append(f"{p.dots} dots, want {s['firms']}")
if body.count('class="dot lead"') != s["leads"]:
    errs.append("lead dot count wrong")
for h in p.links:
    if h.startswith(("http", "../")):
        continue
    if not os.path.exists(os.path.join(HERE, h)) and os.path.basename(path) == "index.html":
        errs.append(f"missing local link {h}")
for want in [f"<b>{s['firms']}</b>", f"<b>{s['leads']}</b>", f"<b>{s['with_both']}</b>", "Three leads",
             "about 120 firms", "55 leads", "RULE.md"]:
    if want not in body:
        errs.append(f"missing {want!r}")
for r in run["rows"]:
    if r["name"] and len(r["name"]) > 4 and r["name"] in body:
        errs.append("a firm name is on the page")
        break
if "—" in body:
    errs.append("em dash")
if "undefined" in body or "None" in body:
    errs.append("undefined or None in body")
print("LINT OK" if not errs else "LINT FAIL\n" + "\n".join(errs))
sys.exit(1 if errs else 0)
