"""F-0023 check: the node --test rule, old way v new way, pure Python, imports nothing from .claude/.
Exit 0 when the old rule denies the legitimate sandbox test run and the new rule allows it while
still denying the unsafe forms."""
import os
import sys

ROOT = "/Users/triton/PROTEUS/"
SANDBOX = ROOT + "sandbox/"


def under(p, root):
    q = os.path.realpath(p) if p.startswith("/") else None
    r = os.path.realpath(root)
    return q is not None and (q == r or q.startswith(r + os.sep))


def old(parts):
    head = parts[0]
    if head == "node" and len(parts) == 2 and parts[1] in ("--version", "-v"):
        return "allow"
    if len(parts) > 1 and under(parts[1], ROOT):
        return "allow"
    if head == "node" and len(parts) > 1 and parts[1] == "-e":
        return "allow"
    return "deny"


def new(parts):
    head = parts[0]
    if head == "node" and len(parts) == 2 and parts[1] in ("--version", "-v"):
        return "allow"
    if head == "node" and len(parts) > 2 and parts[1] == "--test":
        return "allow" if all(not p.startswith("-") and under(p, SANDBOX) for p in parts[2:]) else "deny"
    return old(parts)


cases = [
    ("node --test " + SANDBOX + "p0154-herk/test.mjs", "deny", "allow"),
    ("node --test " + SANDBOX + "a.mjs " + SANDBOX + "b.mjs", "deny", "allow"),
    ("node --test " + ROOT + "bin/x.test.js", "deny", "deny"),
    ("node --test", "deny", "deny"),
    ("node --test --eval x " + SANDBOX + "a.mjs", "deny", "deny"),
    ("node --test /Users/triton/OBSIDIAN/x.mjs", "deny", "deny"),
    ("node --test " + SANDBOX + "../bin/x.js", "deny", "deny"),
    ("node " + ROOT + "bin/build-lab.cjs", "allow", "allow"),
]
bad = 0
for cmd, want_old, want_new in cases:
    p = cmd.split()
    o, n = old(p), new(p)
    ok = o == want_old and n == want_new
    bad += not ok
    print("OK  " if ok else "FAIL", cmd, "old", o, "new", n)
sys.exit(1 if bad else 0)
