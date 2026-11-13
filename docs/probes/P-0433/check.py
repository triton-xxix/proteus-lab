"""Lint docs/probes/P-0433/index.html, or a saved copy of the live body given as the first argument.

Fails on unbalanced tags, a missing local link, undefined or NaN, a chart with the wrong number of marks,
or a headline number from data.json missing from the body.
python3 /Users/triton/PROTEUS/docs/probes/P-0433/check.py [body.html]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html")
html = open(path).read()
d = json.load(open(os.path.join(HERE, "data.json")))
errs = []

body = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
VOID = {"meta", "link", "br", "img", "input", "hr", "line", "circle", "rect", "polyline"}
stack = []
for close, tag, self_ in re.findall(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>", body):
    t = tag.lower()
    if self_ or t in ("meta", "link", "br", "img", "input", "hr"):
        continue
    if not close:
        stack.append(t)
    elif stack and stack[-1] == t:
        stack.pop()
    else:
        errs.append(f"unexpected </{t}>, open {stack[-3:]}")
if stack:
    errs.append(f"unclosed {stack}")
for h in re.findall(r'href="([^"]+)"', body):
    if not re.match(r"^(https?:|#|mailto:)", h) and not os.path.exists(os.path.join(HERE, h)):
        errs.append(f"missing local link {h}")
if re.search(r"undefined|NaN|Infinity|None|nan%", body):
    errs.append("undefined/NaN/None in body")
if "—" in body:
    errs.append("em dash in body")
svgs = body.count("<svg")
if svgs != 3:
    errs.append(f"{svgs} charts, want 3")
hdots = len(re.findall(r"<title>horizon ", body))
if hdots != 12:
    errs.append(f"{hdots} horizon dots, want 12")
sdots = len(re.findall(r"<title>size ", body))
if sdots != d["bucket_rows"] * 3:
    errs.append(f"{sdots} size marks, want {d['bucket_rows'] * 3}")
bars = len(re.findall(r"<title>fade ", body))
if bars != d["symbol_bars"]:
    errs.append(f"{bars} fade bars, want {d['symbol_bars']}")
trs = len(re.findall(r"<tr><td>", body))
if trs != d["bucket_rows"]:
    errs.append(f"{trs} table rows, want {d['bucket_rows']}")
p = d["pooled_2009"]
want = [
    f"{p['gaps']:,}", f"{p['same']:.1f}%", f"{p['mirror']:.1f}%", f"{p['d20']:.1f}%", f"{p['fade_win']:.1f}%",
    f"{abs(p['fade_mean']):.3f}%", f"{d['pull_points']:.1f} points", f"{d['symbols_negative']} of {d['symbols']}",
    f"{d['spy_all']['same']:.1f}%", f"{d['spy_all']['d20']:.1f}%", f"{abs(d['spy_2009']['fade_mean']):.3f}%",
]
for v in want:
    if v not in body:
        errs.append(f"headline {v} not in body")
for e in errs:
    print("FAIL", e)
print("check P-0433", f"{len(errs)} problems" if errs else "OK", "| bytes", len(html), "| charts", svgs)
sys.exit(1 if errs else 0)
