"""P-0020: does reladraw install from npm and render a 3-node text diagram to SVG, keyless?

Also checks two README claims by measurement: output is deterministic (two renders, same bytes),
and gaps are minimums (put a node between two others and they move apart; remove it and they close
back up). Usage: python3 p0020_reladraw.py
"""
import hashlib
import json
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET

SANDBOX = "/Users/triton/PROTEUS/sandbox/reladraw"
OUT = "/Users/triton/PROTEUS/experiments/2026-09-26-P-0020"

THREE = '''node app "Web app"
node app.ui  "Interface"
node app.api "API"  below app.ui

node store "Database"  right of app  level with app

edge app.api -> store  "queries"  from: right  to: left
'''

# SYNTAX.md's own corridor example, with and without the wedge. The README's "between X and Y"
# wording is an edge clause; on a node it is an error ("between" is not a direction), tried first.
PAIR = '''node hub    "Hub"
node side   "Side"    left of hub
'''

BETWEEN = '''node hub    "Hub"
node side   "Side"    left of hub
node wedge  "A much wider wedged node"  right of side  left of hub  level with hub
'''

results = {}


def sh(cmd, cwd, timeout=300):
    t = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, round(time.time() - t, 1), (p.stdout + p.stderr)[-1500:]


def render(name, src):
    path = os.path.join(OUT, name + ".reladraw")
    svg = os.path.join(OUT, name + ".svg")
    with open(path, "w") as f:
        f.write(src)
    rc, secs, out = sh([os.path.join(SANDBOX, "node_modules/.bin/reladraw"), path, "-o", svg], SANDBOX)
    r = {"rc": rc, "secs": secs, "out": out}
    if rc == 0 and os.path.exists(svg):
        data = open(svg, "rb").read()
        r["bytes"] = len(data)
        r["sha"] = hashlib.sha256(data).hexdigest()[:16]
        try:
            root = ET.fromstring(data)
            r["well_formed"] = True
            r["elements"] = sum(1 for _ in root.iter())
            r["viewBox"] = root.get("viewBox")
        except ET.ParseError as e:
            r["well_formed"] = False
            r["parse_error"] = str(e)
    results[name] = r
    return r


def box(svgpath, label):
    """(left, right) x of the node path drawn just before the text carrying this label."""
    s = open(svgpath).read()
    i = s.find(">" + label + "<")
    if i < 0:
        return None
    paths = list(re.finditer(r'<path d="M([-0-9.]+) [-0-9.]+ H([-0-9.]+)', s[:i]))
    if not paths:
        return None
    m = paths[-1]
    # path starts after the 8px corner radius on both sides
    return float(m.group(1)) - 8, float(m.group(2)) + 8


def main():
    os.makedirs(SANDBOX, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(os.path.join(SANDBOX, "package.json")):
        with open(os.path.join(SANDBOX, "package.json"), "w") as f:
            f.write('{"name": "p0020", "private": true}\n')
    rc, secs, out = sh(["npm", "install", "--ignore-scripts", "--no-audit", "--no-fund", "reladraw"], SANDBOX, 300)
    results["install"] = {"rc": rc, "secs": secs, "out": out}
    rc, secs, out = sh(["npm", "ls", "--all"], SANDBOX)
    results["deps"] = out
    render("three", THREE)
    again = dict(render("three_again", THREE))
    results["deterministic"] = results["three"].get("sha") == again.get("sha")
    render("pair", PAIR)
    render("between", BETWEEN)
    gap = {}
    for name in ("pair", "between"):
        svg = os.path.join(OUT, name + ".svg")
        if os.path.exists(svg):
            side, hub = box(svg, "Side"), box(svg, "Hub")
            wedge = box(svg, "A much wider wedged node")
            gap[name] = {"side": side, "hub": hub, "wedge": wedge,
                         "side_to_hub": (hub[0] - side[1]) if side and hub else None}
    results["gap_test"] = gap
    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
