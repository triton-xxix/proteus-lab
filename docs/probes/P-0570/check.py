"""Lint the P-0570 page: tags balance, links go to known places, chart marks counted, dot stacks stay
inside their panel, headline numbers (read from data.json) present in the body, no em dash, nothing undefined.

python3 /Users/triton/PROTEUS/docs/probes/P-0570/check.py [path-to-html]
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
    if not (h.startswith("https://github.com/triton-xxix/proteus-lab/") or h in ("data.json", "../", "../../")):
        bad.append(f"odd link {h}")

want = {r"<svg ": 2, r"<title>clip seed ": d["seeds"], r"<title>speaker seed ": d["seeds"],
        r"<title>P-05\d\d: ": len(d["chain"]), r"<tr><td>P-05": 4}
for pat, n in want.items():
    got = len(re.findall(pat, body))
    if got != n:
        bad.append(f"{pat!r}: {got} v {n}")
# dots: clip panel is y 40 to 152, speaker 190 to 302 (build.py)
for kind, top in (("clip", 34), ("speaker", 184)):
    ys = [float(m) for m in re.findall(r'cy="([\d.]+)" r="3.3"[^>]*><title>' + kind, body)]
    if not ys or min(ys) < top:
        bad.append(f"{kind} dots climb to y {min(ys) if ys else None}, above {top}")


def pc(x, n=1):
    return f"{x * 100:.{n}f}%"


heads = [pc(d["clip"]["median"]), pc(d["clip"]["p5"]), pc(d["clip"]["p95"]), pc(d["p0547"]),
         f"{d['p0547_rank']}th percentile", f"{d['clip_swing_pts']} points", pc(d["sear"], 2),
         f"{d['sear_rank_clip']}th percentile", pc(d["codec_mean"]), f"{d['seeds']} clip splits"]
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
print(f"check OK {path}: {len(body):,} bytes, {2 * d['seeds']} seed dots, {len(d['chain'])} chain rows, {len(heads)} headlines")
