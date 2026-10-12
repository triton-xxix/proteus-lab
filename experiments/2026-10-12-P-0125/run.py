#!/usr/bin/env python3
"""P-0125: does exempting _child from the stray-image rule pass the parked Inception digest, and nothing else change?

Runs the live check.py and a patched copy (blob excludes images and _child) on:
  head   the digest as committed by the child (backdrop path in _child.notes)
  work   the working-tree digest (note cleaned by hand on 10 Oct)
  ctrl   head with a .jpg planted in one_line, to show the patch still catches a real stray image
Writes result.json beside this script.
"""
import copy
import json
import os
import subprocess
import types

ROOT = "/Users/triton/PROTEUS/"
SITE = ROOT + "sites/nolan/"
DIGEST = "state/agents/nolan/2026-10-10-inception.json"
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = ROOT + "sandbox/p0125/"
os.makedirs(TMP, exist_ok=True)

OLD = 'blob = json.dumps({k: v for k, v in d.items() if k != "images"})'
NEW = 'blob = json.dumps({k: v for k, v in d.items() if k not in ("images", "_child")})'


def load(patched):
    src = open(SITE + "check.py").read()
    assert OLD in src, "blob line moved; patch target not found"
    if patched:
        src = src.replace(OLD, NEW)
    m = types.ModuleType("check_p" if patched else "check_l")
    m.__file__ = SITE + "check.py"
    exec(compile(src, SITE + "check.py", "exec"), m.__dict__)
    return m


head = json.loads(subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + DIGEST], capture_output=True, text=True, check=True).stdout)
work = json.load(open(ROOT + DIGEST))
ctrl = copy.deepcopy(head)
ctrl["one_line"] = ctrl.get("one_line", "") + " see poster.jpg"

cases = {"head": head, "work": work, "ctrl": ctrl}
live, patched = load(False), load(True)
out = {}
for name, d in cases.items():
    p = TMP + name + ".json"
    json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)
    row = {}
    for label, mod in (("live", live), ("patched", patched)):
        fails, warns = mod.check_film(p)
        row[label] = {"fails": fails, "warns": warns}
    out[name] = row
    print("%-5s live %d fail %d warn | patched %d fail %d warn" % (
        name, len(row["live"]["fails"]), len(row["live"]["warns"]), len(row["patched"]["fails"]), len(row["patched"]["warns"])))
    for label in ("live", "patched"):
        for f in row[label]["fails"]:
            print("   %s FAIL: %s" % (label, f))
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=2, ensure_ascii=False)
