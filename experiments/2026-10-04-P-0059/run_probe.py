"""P-0059: time the answer-me-with-html bundled CLI rendering Markdown to HTML, offline-checked."""
import json
import os
import re
import subprocess
import time

HERE = "/Users/triton/PROTEUS/experiments/2026-10-04-P-0059"
REPO = "/Users/triton/PROTEUS/sandbox/p0059/answer-me-with-html-HEAD"
CLI = f"{REPO}/skills/answer-me-with-html/scripts/am.mjs"
env = dict(os.environ, AM_HOME="/Users/triton/PROTEUS/sandbox/p0059/am-home")

jobs = [
    ("tcp.en", f"{REPO}/examples/tcp.en.md"),
    ("architecture", f"{REPO}/examples/architecture.md"),
    ("draft", f"{HERE}/draft.md"),
]
results = []
for name, src in jobs:
    out = f"{HERE}/{name}.html"
    runs = []
    for _ in range(3):
        t0 = time.perf_counter()
        p = subprocess.run(["node", CLI, "render", src, "-o", out, "--no-open"],
                           env=env, capture_output=True, text=True, timeout=60)
        runs.append(round(time.perf_counter() - t0, 3))
    html = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    ext = sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"', html)))
    md_words = len(open(src, encoding="utf-8").read().split())
    results.append({
        "name": name, "rc": p.returncode, "seconds": runs, "html_bytes": len(html),
        "svg_count": html.count("<svg"), "table_count": html.count("<table"),
        "external_refs": ext, "md_words": md_words,
        "stderr_tail": p.stderr[-300:], "stdout_tail": p.stdout[-300:],
    })
json.dump(results, open(f"{HERE}/results.json", "w"), indent=2)
for r in results:
    print(r["name"], "rc", r["rc"], "s", r["seconds"], "bytes", r["html_bytes"],
          "svg", r["svg_count"], "tables", r["table_count"], "ext", len(r["external_refs"]),
          "md words", r["md_words"])
    if r["rc"]:
        print("  stderr:", r["stderr_tail"])
