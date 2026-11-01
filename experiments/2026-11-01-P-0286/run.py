"""P-0286: build teardown's v8-live example and load it in headless Chromium.

Steps, each optional on re-run: extract the codeload tarball into sandbox/teardown/src, run
`node sims/build.mjs v8-live` with that as cwd, then open the built HTML from file:// in
Playwright's already-cached Chromium (Python playwright if present, else report), count console
errors, take a screenshot, and write results.json beside this script.
"""
import json
import os
import subprocess
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SB = Path("/Users/triton/PROTEUS/sandbox/teardown")
TGZ = SB / "src.tar.gz"
out = {}

src = next((p for p in SB.glob("src/*") if p.is_dir()), None)
if src is None:
    with tarfile.open(TGZ) as t:
        t.extractall(SB / "src", filter="data")
    src = next(p for p in SB.glob("src/*") if p.is_dir())
out["src"] = str(src)
pkg = json.loads((src / "package.json").read_text()) if (src / "package.json").exists() else {}
out["deps"] = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

if sys.argv[1:] == ["load"]:
    # Python playwright is not in the venv; use teardown's own node playwright
    r = subprocess.run(["/usr/local/bin/node", str(HERE / "load.mjs")], capture_output=True, text=True, timeout=180)
    print(r.stdout[-3000:], r.stderr[-1500:])
    sys.exit(r.returncode)

if sys.argv[1:] == ["extract"]:
    print(json.dumps(out, indent=1))
    sys.exit(0)

t = time.time()
r = subprocess.run(["/usr/local/bin/node", "sims/build.mjs", "v8-live"], cwd=src, capture_output=True, text=True)
out["build_rc"] = r.returncode
out["build_s"] = round(time.time() - t, 1)
out["build_tail"] = (r.stdout + r.stderr)[-800:]
html = src / "teardown-out" / "dist" / "v8-live.html"
out["html_exists"] = html.exists()
if html.exists():
    data = html.read_text(errors="replace")
    out["html_bytes"] = html.stat().st_size
    out["external_refs"] = sorted({s for s in ("http://", "https://") if f'src="{s}' in data or f"href=\"{s}" in data})

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        out["load"] = "python playwright not installed"
    else:
        errs, reqs = [], []
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
            pg = b.new_page(viewport={"width": 1280, "height": 800})
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("request", lambda q: reqs.append(q.url) if not q.url.startswith(("file:", "data:", "blob:")) else None)
            t = time.time()
            pg.goto(html.as_uri())
            pg.wait_for_timeout(6000)
            out["load_s"] = round(time.time() - t, 1)
            out["canvas_count"] = pg.evaluate("document.querySelectorAll('canvas').length")
            out["title"] = pg.title()
            pg.screenshot(path=str(HERE / "v8-live.png"))
            b.close()
        out["console_errors"] = errs[:10]
        out["network_requests"] = reqs[:10]

(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
