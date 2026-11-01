"""P-0287: reanimate's recorder against a public page, keyless.

`run.py extract` unpacks the codeload tarball into sandbox/reanimate/src and lists the files.
`run.py cmd <args...>` runs a command (bun, node) with the repo folder as cwd, because the hook
allows no `cd`; stdout and stderr tails are printed.
"""
import os
import subprocess
import sys
import tarfile
from pathlib import Path

SB = Path("/Users/triton/PROTEUS/sandbox/reanimate")
src = next((p for p in SB.glob("src/*") if p.is_dir()), None)
if src is None:
    with tarfile.open(SB / "src.tar.gz") as t:
        t.extractall(SB / "src", filter="data")
    src = next(p for p in SB.glob("src/*") if p.is_dir())

if sys.argv[1] == "extract":
    for p in sorted(src.rglob("*")):
        if p.is_file() and "node_modules" not in p.parts:
            print(p.relative_to(src), p.stat().st_size)
elif sys.argv[1] == "cmd":
    # Playwright 1.64.1 wants Chromium 1248; the user cache has 1234, so browsers go in the sandbox
    env = {**os.environ, "PLAYWRIGHT_BROWSERS_PATH": "/Users/triton/PROTEUS/sandbox/ms-playwright"}
    r = subprocess.run(sys.argv[2:], cwd=src / "skills/reanimate/scripts", env=env, capture_output=True, text=True, timeout=900)
    print("rc", r.returncode)
    print(r.stdout[-4000:])
    print(r.stderr[-2000:])
