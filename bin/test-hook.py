#!/usr/bin/env python3
"""Test harness for .claude/hooks/unattended-decide.py (Proteus copy).

Runs the hook as a subprocess with a bound marker and asserts allow/deny per case. Restores the
marker file afterwards. Exit 0 on all pass, 1 otherwise.

    python3 /Users/triton/PROTEUS/bin/test-hook.py
"""
import json
import os
import subprocess
import sys
import time

ROOT = "/Users/triton/PROTEUS/"
HOOK = ROOT + ".claude/hooks/unattended-decide.py"
MARKER = ROOT + "state/unattended-session.json"
SID = "test-session-0001"

CASES = [
    # (tool, tool_input, expected)
    ("Read", {"file_path": ROOT + "CHARTER.md"}, "allow"),
    ("Read", {"file_path": "/etc/hosts"}, "deny"),
    ("Write", {"file_path": ROOT + "grinder/LEDGER.csv"}, "allow"),
    ("Write", {"file_path": "/Users/triton/OBSIDIAN/TRITON-CORE/Proteus/field-notes/2026-39.md"}, "allow"),
    ("Write", {"file_path": "/Users/triton/OBSIDIAN/TRITON-CORE/Systems/flywheel/ledger.yaml"}, "deny"),
    ("Edit", {"file_path": "/Users/triton/OBSIDIAN/XXIX/IVY_ROSE/HOME.md"}, "deny"),
    ("Edit", {"file_path": "/Users/triton/.openclaw/workspace/flywheel/bin/lane-sync.cjs"}, "deny"),
    ("Bash", {"command": "python3 " + ROOT + "grinder/scan.py --paper"}, "allow"),
    ("Bash", {"command": ROOT + ".venv/bin/python3 " + ROOT + "pitch/predict.py"}, "allow"),
    ("Bash", {"command": "python3 /Users/triton/OBSIDIAN/anything.py"}, "deny"),
    ("Bash", {"command": "node " + ROOT + "bin/build-lab.cjs"}, "allow"),
    ("Bash", {"command": "git -C " + ROOT + " add -A"}, "allow"),
    ("Bash", {"command": "git -C " + ROOT + " commit -m pre-register"}, "allow"),
    ("Bash", {"command": "git -C " + ROOT + " push origin main"}, "allow"),
    ("Bash", {"command": "git -C /Users/triton/OBSIDIAN/XXIX add -A"}, "deny"),
    ("Bash", {"command": "git -C " + ROOT + " push upstream main"}, "deny"),
    ("Bash", {"command": "git -C " + ROOT + " reset --hard"}, "deny"),
    ("Bash", {"command": "curl -s https://api.dexscreener.com/latest/dex/search?q=pump"}, "allow"),
    ("Bash", {"command": "curl -s https://x.invalid | jq ."}, "allow"),
    ("Bash", {"command": "ls " + ROOT + " && rm -rf /"}, "deny"),
    ("Bash", {"command": "echo hi > " + ROOT + "x.txt"}, "deny"),
    ("Bash", {"command": "for i in 1 2; do echo $i; done"}, "deny"),
    ("Bash", {"command": "gh repo view triton-xxix/proteus-lab"}, "allow"),
    ("Bash", {"command": "gh repo create proteus-x"}, "deny"),
    ("Bash", {"command": "mkdir -p " + ROOT + "grinder/cache"}, "allow"),
    ("Bash", {"command": "mkdir -p /Users/triton/elsewhere"}, "deny"),
    ("Bash", {"command": "rm " + ROOT + "HALT"}, "deny"),
    ("mcp__Claude_Browser__get_page_text", {}, "allow"),
    ("Agent", {"prompt": "x"}, "deny"),
    # found by the first nightly run, 2026-09-22
    ("Bash", {"command": "git -C /Users/triton/PROTEUS status --short"}, "allow"),
    ("Bash", {"command": "git -C /Users/triton/PROTEUS commit -m \"nightly: pre-register for 2026-09-22\n\nGrinder: 94 rows\""}, "allow"),
    ("Bash", {"command": "grep -ohiE '(token|1024|frontmatter)' /Users/triton/PROTEUS/field-notes/x.md"}, "allow"),
    ("Bash", {"command": "git -C /Users/triton/PROTEUS commit -m \"$(cat /etc/passwd)\""}, "deny"),
    ("Bash", {"command": "echo \"a; b\" && rm -rf /"}, "deny"),
    ("ToolSearch", {"query": "select:WebFetch"}, "allow"),
]


def run(tool, ti):
    payload = {"session_id": SID, "tool_name": tool, "tool_input": ti, "permission_mode": "default"}
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(payload), capture_output=True, text=True)
    if not p.stdout.strip():
        return "silent"
    try:
        return json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"]
    except Exception:
        return "unparsable:" + p.stdout[:80]


def main():
    os.makedirs(ROOT + "state", exist_ok=True)
    saved = None
    if os.path.exists(MARKER):
        with open(MARKER) as fh:
            saved = fh.read()
    with open(MARKER, "w") as fh:
        json.dump({"session_id": SID, "task": "test", "bound_at": time.time()}, fh)
    fails = 0
    try:
        for tool, ti, want in CASES:
            got = run(tool, ti)
            ok = got == want
            fails += 0 if ok else 1
            print(("PASS" if ok else "FAIL"), tool, json.dumps(ti)[:70], "want", want, "got", got)
    finally:
        if saved is None:
            os.remove(MARKER)
        else:
            with open(MARKER, "w") as fh:
                fh.write(saved)
    print("%d cases, %d failed" % (len(CASES), fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
