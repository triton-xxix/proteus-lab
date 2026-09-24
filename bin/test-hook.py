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
    ("Bash", {"command": "bash " + ROOT + "bin/mirror-vault.sh"}, "allow"),
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
    # bypasses in the quote-masking fix, found by probing it 2026-09-22. All six were allowed.
    # Escaped quotes are literal to bash and do NOT open a quoted string, so a regex that pairs
    # them up reads the rest of the line as an argument and misses the ';'.
    ("Bash", {"command": "echo a\\'b; rm -rf /tmp/x\\'c"}, "deny"),
    ("Bash", {"command": "echo \\'; rm -rf /tmp/y; echo \\'"}, "deny"),
    # '2>' is redirection too; the old regex only refused '>' when not preceded by a digit.
    ("Bash", {"command": "curl -s https://example.com 2>/Users/triton/.zshrc"}, "deny"),
    # '..' has to be resolved before the prefix comparison, or the folder check means nothing.
    ("Bash", {"command": "git -C /Users/triton/PROTEUS/../OBSIDIAN add -A"}, "deny"),
    ("Bash", {"command": "mkdir -p /Users/triton/PROTEUS/../../evil"}, "deny"),
    # KNOWN GAP, pinned here rather than fixed, because closing it is a policy call for Luke and
    # not a defect. The Read tool is held to READ_ROOTS, but cat/head/tail/grep via Bash are held
    # to nothing, so Bash can read anything on the disk. Tonight that freedom was used well (the
    # Field Notes item verified a claim against ~/.claude/skills), which is why it is not simply
    # clamped to the folder. A deny-list for .ssh/.aws/.gnupg/op config would be the cheap fix.
    ("Bash", {"command": "cat /Users/triton/PROTEUS/../.ssh/id_rsa"}, "allow"),
    ("Write", {"file_path": ROOT + "../OBSIDIAN/XXIX/IVY_ROSE/HOME.md"}, "deny"),
    ("Read", {"file_path": "/Users/triton/../../etc/passwd"}, "deny"),
    # variable expansion is not verifiable either, quoted or not
    ("Bash", {"command": "cat $HOME/.ssh/id_rsa"}, "deny"),
    ("Bash", {"command": "echo \"$HOME\""}, "deny"),
    # ...but the same characters inside single quotes are just text
    ("Bash", {"command": "grep -c 'a;b' " + ROOT + "x.md"}, "allow"),
    ("Bash", {"command": "grep -c 'cost $5 & up' " + ROOT + "x.md"}, "allow"),
    ("Bash", {"command": "git -C " + ROOT + " commit -m \"fix: for and while, 2>1; done\""}, "allow"),
]


# Fan-out cases run with FANOUT_ENABLED overridden on, under a fresh session id each time so the
# spawn counter (which reads today's decisions log) starts from zero. The id begins with 't', which
# no real session id does (they are hex), so `grep -v '"session": "t'` drops every test line.
FANOUT_SID = "t%07x" % (int(time.time()) & 0xFFFFFFF)
CHILD = {"agent_id": "a-test-child-0001", "agent_type": "general-purpose"}
PARENT = {}
ON = {"PROTEUS_FANOUT_OVERRIDE": "1"}
FANOUT_CASES = [
    # (who, tool, tool_input, expected)
    # parent spawning, caps on type, isolation, model
    (PARENT, "Agent", {"subagent_type": "general-purpose", "model": "haiku", "prompt": "x"}, "allow"),   # 1
    (PARENT, "Agent", {"subagent_type": "Explore", "model": "sonnet", "prompt": "x"}, "allow"),          # 2
    (PARENT, "Agent", {"subagent_type": "general-purpose", "model": "opus", "prompt": "x"}, "deny"),
    (PARENT, "Agent", {"subagent_type": "general-purpose", "prompt": "x"}, "deny"),                       # model absent
    (PARENT, "Agent", {"subagent_type": "general-purpose", "model": "haiku", "isolation": "worktree", "prompt": "x"}, "deny"),
    (PARENT, "Agent", {"subagent_type": "Plan", "model": "haiku", "prompt": "x"}, "deny"),
    (PARENT, "Agent", {"subagent_type": "claude-code-guide", "model": "haiku", "prompt": "x"}, "deny"),
    # depth one
    (CHILD, "Agent", {"subagent_type": "general-purpose", "model": "haiku", "prompt": "x"}, "deny"),
    # child writes: scratch only
    (CHILD, "Write", {"file_path": ROOT + "sandbox/probe/out.txt"}, "allow"),
    (CHILD, "Write", {"file_path": ROOT + "state/agents/2026-09-24/child.md"}, "allow"),
    (CHILD, "Edit", {"file_path": ROOT + "state/runs/2026-09-24.md"}, "deny"),
    (CHILD, "Write", {"file_path": ROOT + "SPEND.md"}, "deny"),
    (CHILD, "Write", {"file_path": ROOT + "TRACK-RECORD.md"}, "deny"),
    (CHILD, "Write", {"file_path": ROOT + "grinder/LEDGER.csv"}, "deny"),
    (CHILD, "Write", {"file_path": ROOT + "pitch/PREDICTIONS.csv"}, "deny"),
    (CHILD, "Write", {"file_path": ROOT + "state/unattended-session.json"}, "deny"),
    (CHILD, "Write", {"file_path": "/Users/triton/OBSIDIAN/TRITON-CORE/Proteus/field-notes/x.md"}, "deny"),
    (CHILD, "Write", {"file_path": ROOT + "sandbox/../SPEND.md"}, "deny"),
    # child bash: no git writes, scripts from sandbox only, mkdir/touch in scratch only
    (CHILD, "Bash", {"command": "git -C " + ROOT + " status --short"}, "allow"),
    (CHILD, "Bash", {"command": "git -C " + ROOT + " add -A"}, "deny"),
    (CHILD, "Bash", {"command": "git -C " + ROOT + " commit -m x"}, "deny"),
    (CHILD, "Bash", {"command": "git -C " + ROOT + " push origin main"}, "deny"),
    (CHILD, "Bash", {"command": "git push origin main"}, "deny"),
    (CHILD, "Bash", {"command": "python3 " + ROOT + "sandbox/check_claims.py"}, "allow"),
    (CHILD, "Bash", {"command": ROOT + ".venv/bin/python3 " + ROOT + "sandbox/diag_pitch.py"}, "allow"),
    (CHILD, "Bash", {"command": ROOT + ".venv/bin/python3 " + ROOT + "grinder/paper.py --apply-rules"}, "deny"),
    (CHILD, "Bash", {"command": "bash " + ROOT + "bin/send-field-notes.sh"}, "deny"),
    (CHILD, "Bash", {"command": ROOT + "bin/run-nightly.sh"}, "deny"),
    (CHILD, "Bash", {"command": "node " + ROOT + "bin/build-lab.cjs"}, "deny"),
    (CHILD, "Bash", {"command": "curl -s https://api.dexscreener.com/latest/dex/search?q=pump"}, "allow"),
    (CHILD, "Bash", {"command": "cat " + ROOT + "CHARTER.md"}, "allow"),
    (CHILD, "Bash", {"command": "mkdir -p " + ROOT + "sandbox/probe"}, "allow"),
    (CHILD, "Bash", {"command": "mkdir -p " + ROOT + "grinder/cache"}, "deny"),
    (CHILD, "Bash", {"command": "touch " + ROOT + "state/agents/x"}, "allow"),
    (CHILD, "Bash", {"command": "touch " + ROOT + "HALT"}, "deny"),
    (CHILD, "Bash", {"command": "echo one; echo two"}, "deny"),                                      # parent rules still apply
    # child reads and browser: unchanged from the parent
    (CHILD, "Read", {"file_path": ROOT + "CHARTER.md"}, "allow"),
    (CHILD, "Read", {"file_path": "/etc/hosts"}, "deny"),
    (CHILD, "mcp__Claude_Browser__get_page_text", {}, "allow"),
    # the spawn cap: two allowed above, two more here, the fifth is denied
    (PARENT, "Agent", {"subagent_type": "general-purpose", "model": "haiku", "prompt": "x"}, "allow"),   # 3
    (PARENT, "Agent", {"subagent_type": "general-purpose", "model": "sonnet", "prompt": "x"}, "allow"),  # 4
    (PARENT, "Agent", {"subagent_type": "general-purpose", "model": "haiku", "prompt": "x"}, "deny"),    # 5, cap
    (PARENT, "Agent", {"subagent_type": "Explore", "model": "sonnet", "prompt": "x"}, "deny"),           # still capped
]


def run(tool, ti, sid=SID, who=None, env=None):
    payload = {"session_id": sid, "tool_name": tool, "tool_input": ti, "permission_mode": "default"}
    payload.update(who or {})
    full_env = dict(os.environ)
    full_env.update(env or {})
    p = subprocess.run([sys.executable, HOOK], input=json.dumps(payload), capture_output=True, text=True, env=full_env)
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
        # fan-out: rebind the marker to the fresh id, switch the feature on for the subprocess only
        with open(MARKER, "w") as fh:
            json.dump({"session_id": FANOUT_SID, "task": "test", "bound_at": time.time()}, fh)
        for who, tool, ti, want in FANOUT_CASES:
            got = run(tool, ti, sid=FANOUT_SID, who=who, env=ON)
            ok = got == want
            fails += 0 if ok else 1
            label = "child " if who else "parent"
            print(("PASS" if ok else "FAIL"), "fanout", label, tool, json.dumps(ti)[:60], "want", want, "got", got)
        # and with the feature off, the parent's Agent call is denied whatever it asks for
        got = run("Agent", {"subagent_type": "general-purpose", "model": "haiku", "prompt": "x"}, sid=FANOUT_SID)
        ok = got == "deny"
        fails += 0 if ok else 1
        print(("PASS" if ok else "FAIL"), "fanout off", "Agent", "want deny got", got)
    finally:
        if saved is None:
            os.remove(MARKER)
        else:
            with open(MARKER, "w") as fh:
                fh.write(saved)
    print("%d cases, %d failed" % (len(CASES) + len(FANOUT_CASES) + 1, fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
