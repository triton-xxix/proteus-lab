"""P-0173: render web-ocean's ocean.min.html in headless Chrome with WebGPU and record what happens.

Two passes on the same page: a DOM dump after a virtual-time budget (does #err show?) and a
screenshot. Chrome's stderr carries console lines with --enable-logging=stderr. Writes results.json
and shot.png beside this script.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "/Users/triton/PROTEUS/sandbox/p0173-ocean.min.html"
PROFILE = "/Users/triton/PROTEUS/sandbox/p0173-profile"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = [CHROME, "--headless=new", "--user-data-dir=" + PROFILE, "--enable-unsafe-webgpu",
        "--enable-logging=stderr", "--v=0", "--window-size=1280,720", "--no-first-run"]


MODE = sys.argv[2] if len(sys.argv) > 2 else "virtual"  # virtual: --virtual-time-budget; real: --timeout


def run(extra, budget_ms):
    t = time.time()
    clock = ["--virtual-time-budget=%d" % budget_ms] if MODE == "virtual" else ["--timeout=%d" % budget_ms]
    p = subprocess.run(BASE + clock + extra + ["file://" + PAGE],
                       capture_output=True, text=True, timeout=120)
    return p, round(time.time() - t, 1)


def console_lines(stderr):
    out = []
    for line in stderr.splitlines():
        if "CONSOLE" in line or "Uncaught" in line or "WebGPU" in line or "FATAL" in line:
            out.append(line.strip()[:300])
    return out


def main():
    raw = open(PAGE, "rb").read()
    res = {"mode": MODE, "bytes": len(raw), "kb": round(len(raw) / 1024, 2), "sha256": hashlib.sha256(raw).hexdigest()}

    p, secs = run(["--dump-dom"], int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
    dom = p.stdout
    m = re.search(r'<div[^>]*id="err"[^>]*>(.*?)</div>', dom, re.S)
    err_tag = re.search(r'<[^>]*id="err"[^>]*>', dom)
    fps = re.search(r'<[^>]*id="fps"[^>]*>(.*?)</', dom, re.S)
    res["dump"] = {
        "exit": p.returncode, "seconds": secs, "dom_chars": len(dom),
        "err_tag": err_tag.group(0) if err_tag else None,
        "err_text": m.group(1).strip()[:300] if m else None,
        "fps_text": fps.group(1).strip()[:100] if fps else None,
        "console": console_lines(p.stderr)[:40],
        "stderr_tail": p.stderr.strip().splitlines()[-15:],
    }

    shot = os.path.join(HERE, "shot-%s.png" % MODE)
    p2, secs2 = run(["--screenshot=" + shot], 5000)
    res["screenshot"] = {"exit": p2.returncode, "seconds": secs2,
                         "png_bytes": os.path.getsize(shot) if os.path.exists(shot) else 0,
                         "console": console_lines(p2.stderr)[:40]}

    json.dump(res, open(os.path.join(HERE, "results-%s.json" % MODE), "w"), indent=1)
    print(json.dumps(res, indent=1)[:6000])


if __name__ == "__main__":
    main()
