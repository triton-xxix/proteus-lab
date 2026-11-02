"""Lints docs/bootgpt/index.html: tags balance, local links and the iframe exist, no unfilled braces or
format slots. Copied from the channel-digest lint on 2 Nov 2026.
python3 /Users/triton/PROTEUS/docs/bootgpt/lint.py [file]"""
import os
import re
import sys
from html.parser import HTMLParser

PATH = sys.argv[1] if len(sys.argv) > 1 else "/Users/triton/PROTEUS/docs/bootgpt/index.html"
VOID = {"meta", "link", "br", "img", "input", "hr", "line", "rect", "circle", "path"}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errs, self.links = [], [], []

    def handle_starttag(self, t, a):
        if t not in VOID:
            self.stack.append(t)
        self.links += [v for k, v in a if k in ("href", "src")]

    def handle_startendtag(self, t, a):
        pass

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
errs += ["unfilled slot: %s" % m for m in re.findall(r"%\(\w+\)|\bNone\b|\bundefined\b", body)]
for h in p.links:
    if not h.startswith(("http", "#", "mailto")):
        if not os.path.exists(os.path.join(os.path.dirname(PATH), h)):
            errs.append("missing local link %s" % h)
for e in errs:
    print("FAIL", e)
print("lint", PATH, "OK" if not errs else "%d problems" % len(errs), "| links", len(p.links), "| bytes", len(s))
sys.exit(1 if errs else 0)
