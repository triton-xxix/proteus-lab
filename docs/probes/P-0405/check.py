"""Lint docs/probes/P-0405/index.html, or a saved copy of the live body given as the first argument.

Fails on unbalanced tags, a missing local link, undefined or NaN, a chart with the wrong number of marks,
or a headline number from data.json missing from the body.
python3 /Users/triton/PROTEUS/docs/probes/P-0405/check.py [body.html]
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
if re.search(r"undefined|NaN|Infinity|None|nan%", body):
    errs.append("undefined/NaN/None in body")
svgs = body.count("<svg")
if svgs != 4:
    errs.append(f"{svgs} charts, want 4")
main_dots = len(re.findall(r"<title>G-\d{4} [^<]*snapshot", body))
if main_dots != d["main_rows"]:
    errs.append(f"{main_dots} main dots, want {d['main_rows']}")
r01_dots = len(re.findall(r"<title>R-\d{4} [^<]*snapshot", body))
if r01_dots != d["r01_rows"]:
    errs.append(f"{r01_dots} R01 dots, want {d['r01_rows']}")
trade_marks = len(re.findall(r"<title>trade G-\d{4}", body))
if trade_marks != d["main_rows"]:
    errs.append(f"{trade_marks} trade marks, want {d['main_rows']}")
flip_rows = len(re.findall(r"<tr><td>G-\d{4}</td>", body))
if flip_rows != d["flips"]:
    errs.append(f"{flip_rows} flip rows, want {d['flips']}")
for k in ("median_abs_gap_pct", "r01_median_abs_gap_pct"):
    v = f"{d[k]:.2f}%"
    if v not in body:
        errs.append(f"{k} {v} not in body")
for k in ("total_ledger", "total_candle", "move", "worst_move", "rest_move"):
    v = f"£{abs(d[k]):,.2f}"
    if v not in body:
        errs.append(f"{k} {v} not in body")
for e in errs:
    print("FAIL", e)
print("check P-0405", f"{len(errs)} problems" if errs else "OK", "| bytes", len(html), "| charts", svgs)
sys.exit(1 if errs else 0)
