"""P-0300: a small test library of my own rule files, renamed so the four RULES.md do not collide."""
import os
import shutil

DEST = "/Users/triton/PROTEUS/sandbox/markindex/docs"
SRC = {
    "charter.md": "/Users/triton/PROTEUS/CHARTER.md",
    "pass-marks.md": "/Users/triton/PROTEUS/PASS-MARKS.md",
    "desks/exchange-rules.md": "/Users/triton/PROTEUS/exchange/RULES.md",
    "desks/systems-rules.md": "/Users/triton/PROTEUS/systems/RULES.md",
    "desks/edges-rules.md": "/Users/triton/PROTEUS/edges/RULES.md",
}
for name, src in SRC.items():
    out = os.path.join(DEST, name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(src, out)
    print(name, sum(1 for _ in open(out, encoding="utf-8")), "lines")
