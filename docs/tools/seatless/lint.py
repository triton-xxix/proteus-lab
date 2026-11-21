"""Lints docs/tools/seatless/index.html: tags balance, local links exist, no unfilled braces, one bar per
opening month in the run, 4 table rows, and any extra arguments must appear in the body.
python3 /Users/triton/PROTEUS/docs/tools/seatless/lint.py [file] [needle ...]"""
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = "/Users/triton/PROTEUS/docs/tools/seatless/"
PATH = sys.argv[1] if len(sys.argv) > 1 else HERE + "index.html"
VOID = {"meta", "link", "br", "img", "input", "hr"}
WANT = len(json.load(open(HERE + "run-2026-11-21.json"))["summary"]["by_month"])


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errs, self.links = [], [], []

    def handle_starttag(self, t, a):
        if t not in VOID:
            self.stack.append(t)
        self.links += [v for k, v in a if k == "href"]

    def handle_endtag(self, t):
        if t in VOID:
            return
        if not self.stack or self.stack[-1] != t:
            self.errs.append("unexpected </%s> at %s, open %s" % (t, self.getpos(), self.stack[-3:]))
        else:
            self.stack.pop()


s = open(PATH).read()
p = P()
p.feed(s)
errs = p.errs + (["unclosed %s" % p.stack] if p.stack else [])
body = re.sub(r"<style>.*?</style>", "", s, flags=re.S)
errs += ["unfilled brace: %s" % m for m in re.findall(r"\{[^}]{0,40}\}", body)]
for h in p.links:
    if not h.startswith(("http", "#", "mailto")) and not os.path.exists(os.path.join(HERE, h)):
        errs.append("missing local link %s" % h)
bars = len(re.findall(r'<div class="mb (?:pre|post)" style="height:', s))
rows = body.count("<tr><td>") + body.count("<tr class=tot>")
if bars != WANT:
    errs.append("%d month bars, want %d" % (bars, WANT))
if rows != 4:
    errs.append("%d table rows, want 4" % rows)
if "—" in body:
    errs.append("em dash in body")
for needle in sys.argv[2:]:
    if needle not in body:
        errs.append("not in body: %s" % needle)
for bad in ("None", "nan", "undefined"):
    if re.search(r"\b%s\b" % bad, re.sub(r"<pre>.*?</pre>", "", body, flags=re.S)):
        errs.append("stray %s in body" % bad)
for e in errs:
    print("FAIL", e)
print("lint", PATH, "OK" if not errs else "%d problems" % len(errs), "| links", len(p.links), "| bars", bars,
      "| rows", rows, "| bytes", len(s))
sys.exit(1 if errs else 0)
