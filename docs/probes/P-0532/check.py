"""Lint the P-0532 page: tags balance, links resolve to known places, chart marks counted, headline
numbers (read from data.json) present in the body, no em dash, nothing undefined.

python3 /Users/triton/PROTEUS/docs/probes/P-0532/check.py [path-to-html]
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html")
with open(path, encoding="utf-8") as f:
    body = f.read()
with open(os.path.join(HERE, "data.json")) as f:
    d = json.load(f)

VOID = {"meta", "br", "img", "link", "input", "hr", "circle", "line", "rect", "polyline", "path"}
bad = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.hrefs = [], []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.append(dict(attrs).get("href", ""))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            bad.append(f"tag mismatch at </{tag}>, open {self.stack[-3:]}")
            return
        self.stack.pop()


p = P()
p.feed(body)
if p.stack:
    bad.append(f"unclosed tags {p.stack}")
for h in p.hrefs:
    if not (h.startswith("https://") or h in ("data.json", "../", "../../")):
        bad.append(f"odd link {h}")


def count(pat):
    return len(re.findall(pat, body))


want = {
    r"<svg ": 3,
    r"<title>spike ": d["spike_days"],
    r"<title>storm ": d["storm_rows"],
    r"<title>detector ": 6,
    r"<tr><td>P-053": 4,
}
for pat, n in want.items():
    got = count(pat)
    if got != n:
        bad.append(f"{pat!r}: {got} v {n}")
hint_rows = count(r"<tr><td>\d{1,2} \w{3} 20\d\d</td>")
if hint_rows != d["named_calm"]:
    bad.append(f"hint rows {hint_rows} v {d['named_calm']}")

heads = [
    f"{d['kp7_caught_aurora']} of {d['kp7_days']}",
    f"{d['kp5_caught']} of {d['kp5_days']}",
    f"{d['spikes_near_kp5']} of {d['spike_days']}",
    f"{d['geomagnetic']['caught']} of {d['kp7_days']}",
    f"{d['geomagnetic']['calm']} calm-day spikes",
    f"{d['top_views']:,}",
    str(d["corr_next_day"]),
    f"{d['tails_within_5_days']} of {d['named_calm']}",
    f"{d['days']:,} days",
]
for h in heads:
    if h not in body:
        bad.append(f"headline missing: {h}")
for word in ("undefined", "NaN", "None", "—"):
    if word in re.sub(r"<[^>]+>", " ", body):
        bad.append(f"found {word!r}")

if bad:
    for b in bad:
        print("FAIL", b)
    sys.exit(1)
print(f"check OK {path}: {len(body):,} bytes, {d['spike_days']} spike dots, {d['storm_rows']} storm rows, {len(heads)} headlines")
