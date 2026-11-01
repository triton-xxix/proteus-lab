"""P-0282: run pixelfx's own tools/check.mjs once per category, time each run, parse the ok/fail/warn
lines. Writes results.json beside this script. Node, no dependencies; the repo is at
sandbox/pixelfx-src/pixelfx-main (pulled as a tarball for P-0272 on 31 Oct 2026).

    python3 experiments/2026-11-01-P-0282/run_check.py
"""
import json
import os
import re
import subprocess
import time

REPO = "/Users/triton/PROTEUS/sandbox/pixelfx-src/pixelfx-main"
CHECK = REPO + "/tools/check.mjs"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

cats = sorted(d for d in os.listdir(REPO + "/src/fx") if os.path.isdir(os.path.join(REPO, "src/fx", d)))
res = {"categories": {}, "warnings": [], "fails": []}
t_all = time.time()
total = {"effects": 0, "pass": 0, "fail": 0, "warn": 0}
for c in cats:
    t0 = time.time()
    p = subprocess.run(["node", CHECK, c], cwd=REPO, capture_output=True, text=True, timeout=600)
    dt = time.time() - t0
    lines = p.stdout.splitlines()
    m = None
    for l in lines:
        m2 = re.match(r"(\d+) effects: (\d+) pass, (\d+) fail, (\d+) with warnings", l)
        if m2:
            m = m2
    n, ok, fail, warn = (int(x) for x in m.groups()) if m else (0, 0, 0, 0)
    for l in lines:
        if l.strip() and not re.match(r"ok\s", l) and "effects:" not in l:
            (res["fails"] if "fail" in l.lower() else res["warnings"]).append({"category": c, "line": l.rstrip()})
    res["categories"][c] = {"effects": n, "pass": ok, "fail": fail, "warn": warn, "seconds": round(dt, 2),
                            "seconds_per_effect": round(dt / n, 3) if n else None, "rc": p.returncode,
                            "stderr_tail": p.stderr[-300:]}
    for k, v in (("effects", n), ("pass", ok), ("fail", fail), ("warn", warn)):
        total[k] += v
    print(c, n, "pass", ok, "fail", fail, "warn", warn, "%.1fs" % dt, flush=True)
res["total"] = dict(total, seconds=round(time.time() - t_all, 1))
slow = sorted(res["categories"].items(), key=lambda kv: -(kv[1]["seconds_per_effect"] or 0))
res["slowest_per_effect"] = [(k, v["seconds_per_effect"]) for k, v in slow[:5]]
print("total", res["total"], "slowest per effect", res["slowest_per_effect"])
json.dump(res, open(OUT, "w"), indent=1)
