"""Lint docs/probes/P-0475/index.html, or a saved copy of the live body given as the first argument.

Fails on unbalanced tags, a missing local link, undefined or NaN, a chart with the wrong number of marks,
or a headline number from data.json missing from the body.
python3 /Users/triton/PROTEUS/docs/probes/P-0475/check.py [body.html]
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
for label, pat, want in (
    ("fee dots", r"<title>fee dot ", d["fees_fetched"]),
    ("balance readings", r"<title>reading ", d["readings"]),
    ("coin bars", r"<title>coin ", d["coins"]),
    ("table rows", r"<tr><td>", d["table_rows"]),
):
    got = len(re.findall(pat, body))
    if got != want:
        errs.append(f"{got} {label}, want {want}")
lo, hi = d["sol_per_day"]
want = [
    f"{lo:,.0f} to {hi:,.0f} SOL", f"{d['runway_days'][0]} to {d['runway_days'][1]} days", f"{d['fee_median_sol']:.6f} SOL",
    f"{d['tx_per_s']:.1f} a second", f"{d['fee_times_shot']:.0f} times", f"{d['rises']} of {d['readings'] - 1}",
    f"{d['pages_for_24h']:,} pages", f"{d['median_share_pct']:.1f}%", f"{d['sum_held_bn']:.2f} billion",
    f"{d['wallet_sol']:,.0f} SOL", f"{d['burn_share_of_wallet_pct_a_day']:.2f}%",
]
for v in want:
    if v not in body:
        errs.append(f"headline {v} not in body")
for e in errs:
    print("FAIL", e)
print("check P-0475", f"{len(errs)} problems" if errs else "OK", "| bytes", len(html), "| charts", svgs)
sys.exit(1 if errs else 0)
