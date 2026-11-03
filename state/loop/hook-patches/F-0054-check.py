"""F-0054 check: the hook's node rule, old way and patched way, on the commands that were denied.

    python3 /Users/triton/PROTEUS/state/loop/hook-patches/F-0054-check.py

Pure Python, imports nothing from .claude/. Exit 0 when the old way denies the two harmless forms,
the new way allows them, and both ways still deny a script outside the folder and a child running a
parent script behind the flag.
"""
import sys

ROOT = "/Users/triton/PROTEUS/"
CHILD_EXEC_ROOT = ROOT + "sandbox/"


def under(p, root=ROOT):
    return p.startswith(root)


def parent(parts, patched):
    head = parts[0]
    if patched and len(parts) > 2 and parts[1] == "--experimental-strip-types":
        parts = [head] + parts[2:]
    if patched and len(parts) == 2 and parts[1] in ("--version", "-v"):
        return "allow"
    if len(parts) > 1 and under(parts[1]):
        return "allow"
    if len(parts) > 1 and parts[1] == "-e":
        return "allow"
    return "deny"


def child(parts, patched):
    if parent(parts, patched) == "deny":
        return "deny"
    head = parts[0]
    if patched and len(parts) > 2 and parts[1] == "--experimental-strip-types":
        parts = [head] + parts[2:]
    script = parts[1] if len(parts) > 1 and under(parts[1]) else None
    if script is not None and not under(script, CHILD_EXEC_ROOT):
        return "deny"
    return "allow"


CASES = [
    # (who, command, old, new)
    ("parent", "node --version", "deny", "allow"),
    ("parent", "node --version --eval x", "deny", "deny"),
    ("parent", "node --experimental-strip-types " + ROOT + "sandbox/x.ts", "deny", "allow"),
    ("parent", "node --experimental-strip-types /Users/triton/OBSIDIAN/x.ts", "deny", "deny"),
    ("parent", "node " + ROOT + "bin/build-lab.cjs", "allow", "allow"),
    ("child", "node --experimental-strip-types " + ROOT + "bin/x.ts", "deny", "deny"),
    ("child", "node --experimental-strip-types " + ROOT + "sandbox/x.ts", "deny", "allow"),
]

bad = 0
for who, cmd, want_old, want_new in CASES:
    fn = parent if who == "parent" else child
    got_old, got_new = fn(cmd.split(), False), fn(cmd.split(), True)
    ok = got_old == want_old and got_new == want_new
    bad += not ok
    print("%s %-6s old %-5s new %-5s %s" % ("OK  " if ok else "FAIL", who, got_old, got_new, cmd))

# Without the child strip, the flag hides a parent script from the child's script check.
leak = "node --experimental-strip-types " + ROOT + "bin/x.ts"
parts = leak.split()
hidden = parent(parts, True) == "allow" and not under(parts[1])
print("child strip needed (flag hides the script from parts[1]): %s" % hidden)
sys.exit(1 if bad or not hidden else 0)
