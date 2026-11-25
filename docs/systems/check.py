"""Lint docs/systems/index.html (local file, or a body saved from the live page) against data.json.

python3 /Users/triton/PROTEUS/docs/systems/check.py [path-to-html]
Checks tags balance, links are relative or https, three charts, one bar per closed trade, nine
holding pairs, the luck histogram, the three-question table, and the headline numbers.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html")
html = open(path).read()
d = json.load(open(os.path.join(HERE, "data.json")))
b2, b1 = d["book2"], d["book1"]
bad = []

VOID = {"meta", "br", "img", "input", "link", "hr", "circle", "line", "rect", "polyline", "path"}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []

    def handle_starttag(self, t, a):
        if t not in VOID:
            self.stack.append(t)
        for k, v in a:
            if k == "href" and v and not (v.startswith("https://") or v.startswith("#") or not re.match(r"^[a-z]+:", v)):
                bad.append(f"odd link {v}")

    def handle_startendtag(self, t, a):
        pass

    def handle_endtag(self, t):
        if t in VOID:
            return
        if not self.stack or self.stack[-1] != t:
            bad.append(f"tag mismatch at </{t}>, open {self.stack[-3:]}")
            return
        self.stack.pop()


p = P()
p.feed(html)
if p.stack:
    bad.append(f"unclosed {p.stack}")


def count(pat, want, what):
    n = len(re.findall(pat, html))
    if n != want:
        bad.append(f"{what}: {n} v {want}")


count(r"<svg ", 4, "charts")
count(r'class="bar"', b2["closed"], "trade bars")
count(r'class="rm"', b2["closed"], "running-mean dots")
HIST = os.path.join(HERE, "history")
snaps = sorted(f for f in os.listdir(HIST) if f.endswith(".json"))
count(r'class="snap"', len(snaps), "page-build circles")
for f in snaps:
    if f"page of {f[:-5]}" not in html:
        bad.append(f"missing snapshot label {f[:-5]}")
count(r'class="hold"', 9, "hold dots")
count(r'class="mark"', 9, "book dots")
count(r'class="bin"', 48, "luck bins")
count(r'<td class="v ', 6, "three-question cells")
count(r"still open</td>", b2["open"], "open rows")


def pc(v, n=2):
    return f"{v*100:+.{n}f}%"


for s in [f"{b2['closed']} closed", pc(b2["mean_after_cost"]), f"{b2['win']:.0%} winners", f"t {b2['t']:.2f}",
          f"{b2['week_t']:.2f}", pc(b2["sleeves_marked"]), pc(b2["hold"]), pc(b2["random_median"]),
          f"{b2['open_down']} of {b2['open']}", b2["word"], b1["word"], pc(b1["mean"]), f"t {b1['t']:.2f}", d["last_session"]]:
    if s not in html:
        bad.append(f"missing {s!r}")
for bad_word in ("undefined", "nan%", "NaN", ">None<", " None%"):
    if bad_word in html:
        bad.append(f"found {bad_word}")
if "—" in html:
    bad.append("em dash")

if bad:
    for b in bad:
        print("FAIL", b)
    sys.exit(1)
print(f"ok {path}: 4 charts, {len(snaps)} page builds, {b2['closed']} bars, 9+9 dots, 48 bins, 6 cells, {b2['open']} open rows, headline numbers present")
