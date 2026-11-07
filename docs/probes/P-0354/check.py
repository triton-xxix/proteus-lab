"""Lint docs/probes/P-0354/index.html, or a saved copy of the live body given as the first argument.

Fails on unbalanced tags, a missing local link, undefined or NaN, a chart with the wrong number of marks,
or a headline number from data.json missing from the body.
python3 /Users/triton/PROTEUS/docs/probes/P-0354/check.py [body.html]
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
VOID = {"meta", "link", "br", "img", "input", "hr"}
stack = []
for close, tag, self_ in re.findall(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>", body):
    t = tag.lower()
    if t in VOID or self_:
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
if re.search(r"undefined|NaN|Infinity|None", body):
    errs.append("undefined/NaN/None in body")
svgs = body.count("<svg")
if svgs != 5:
    errs.append(f"{svgs} charts, want 5")
hour_bars = len(re.findall(r"<title>\d\d UTC:", body))
if hour_bars != 24:
    errs.append(f"{hour_bars} hour bars, want 24")
day_squares = len(re.findall(r"<title>2026-10-\d\d: rounded", body))
if day_squares != 28:
    errs.append(f"{day_squares} day squares, want 28")
for k in ("gap", "sampling_and_rounding", "lag_at_warm_hours", "unexplained"):
    v = f"{d[k]:.2f}"
    if v not in body:
        errs.append(f"{k} {v} not in body")
for e in errs:
    print("FAIL", e)
print("check P-0354", f"{len(errs)} problems" if errs else "OK", "| bytes", len(html), "| charts", svgs)
sys.exit(1 if errs else 0)
