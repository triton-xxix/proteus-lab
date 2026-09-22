#!/usr/bin/env python3
"""PreToolUse hook: make an EXPLICIT permission decision in unattended Proteus runs.

Copied 2026-09-22 from /Users/triton/OBSIDIAN/.claude/hooks/unattended-decide.py (installed there
2026-08-28 on Luke's approval) and re-rooted for Proteus. Same design, different roots:

  - on the safe list  -> "allow"  (no prompt)
  - anything else     -> "deny"   (no prompt; the model reads the reason and routes around it)

A denial costs one tool call. A prompt costs the whole night. That asymmetry is the entire design.

SCOPE. Acts only for the session the marker file state/unattended-session.json belongs to.
Interactive sessions never match, so Luke's own sessions in this folder prompt as normal.

Differences from the vault hook, all deliberate:
  - WRITE_ROOTS: this folder plus the vault mirror folder TRITON-CORE/Proteus/. Nothing else.
  - python3 / node / bash may run any script under PROTEUS_ROOT (the desks live in subfolders,
    not only bin/), plus the folder's own venv interpreter.
  - git: read verbs plus add, commit, push, pull (Proteus commits its predictions; that is the
    pre-registration proof). Remote names must start with "proteus-" or be omitted.
  - gh: repo/pages read verbs only; repo creation is an interactive-session job.
  - curl: allowed (API pulls). Redirection still refused; write results with the Write tool.
  - The vault's protect-vaults.py does not run here; the write roots make the vault unreachable.

Test: python3 /Users/triton/PROTEUS/bin/test-hook.py
"""
import json
import os
import re
import sys
import time

PROTEUS_ROOT = "/Users/triton/PROTEUS/"
MARKER = PROTEUS_ROOT + "state/unattended-session.json"
LOG_DIR = PROTEUS_ROOT + "state/"
FLY_BIN = PROTEUS_ROOT + "bin/"
VENV_PY = PROTEUS_ROOT + ".venv/bin/python3"
VENV_PY_ALT = PROTEUS_ROOT + ".venv/bin/python"

BIND_WINDOW_S = 900        # an unbound marker older than this is ignored, never bound
BOUND_MAX_S = 3 * 3600     # a bound marker older than this is a dead run; ignore it

WRITE_ROOTS = (
    PROTEUS_ROOT,
    "/Users/triton/OBSIDIAN/TRITON-CORE/Proteus/",
)

READ_ROOTS = ("/Users/triton/",)

# Tools that cannot prompt and cannot act outside the session.
FREE_TOOLS = {"Read", "Glob", "Grep", "TodoWrite", "NotebookRead", "BashOutput", "KillShell", "Skill",
              "WebFetch", "WebSearch", "ToolSearch", "SearchSkills", "SearchPlugins", "ListSkills"}

# First token of each pipe segment must be one of these.
SAFE_CMDS = {
    "ls", "cat", "head", "tail", "grep", "egrep", "fgrep", "wc", "sort", "uniq", "cut", "tr",
    "jq", "echo", "printf", "date", "find", "stat", "dirname", "basename", "awk", "sed", "diff",
    "true", "test", "which", "file", "shasum", "column", "curl", "mkdir", "touch",
}

GIT_READ = ("status", "log", "show", "diff", "rev-parse", "-C", "branch", "remote")
GIT_WRITE = ("add", "commit", "push", "pull", "fetch")
GH_READ = ("repo", "api", "auth")

COMPLEX = re.compile(r"(;|&&|\|\||\$\(|`|\bfor\b|\bwhile\b|\bdo\b|\bdone\b|\bif\b|\bthen\b|\n)")
REDIRECT = re.compile(r"(?<![0-9])>>?")


def marker_active(session_id):
    try:
        mtime = os.path.getmtime(MARKER)
        with open(MARKER) as fh:
            marker = json.load(fh)
    except Exception:
        return False

    now = time.time()
    bound = marker.get("session_id")

    if bound is None:
        if now - mtime > BIND_WINDOW_S:
            return False
        marker["session_id"] = session_id
        marker["bound_at"] = now
        tmp = MARKER + ".tmp"
        try:
            with open(tmp, "w") as fh:
                json.dump(marker, fh)
            os.replace(tmp, MARKER)
        except Exception:
            return False
        return True

    if bound != session_id:
        return False
    return (now - float(marker.get("bound_at") or mtime)) <= BOUND_MAX_S


def log(session_id, permission_mode, tool, ti, outcome):
    try:
        detail = ti.get("command") or ti.get("file_path") or ti.get("notebook_path") or ti.get("url") or ""
        path = LOG_DIR + "unattended-decisions-" + time.strftime("%Y-%m-%d") + ".jsonl"
        with open(path, "a") as fh:
            fh.write(json.dumps({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "session": str(session_id)[:8],
                "permission_mode": permission_mode,
                "tool": tool,
                "outcome": outcome,
                "detail": str(detail)[:400],
            }) + "\n")
    except Exception:
        pass


CTX = {"session": "", "mode": None, "tool": "", "ti": {}}


def decide(kind, reason):
    log(CTX["session"], CTX["mode"], CTX["tool"], CTX["ti"], kind)
    sys.stdout.write(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": kind,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def deny(reason):
    decide("deny", reason + " [Unattended Proteus run: denied rather than prompted, because a "
                            "prompt would hang the whole run. Do NOT retry this verbatim. Recompose "
                            "it from allowlisted pieces (absolute-path scripts under "
                            "/Users/triton/PROTEUS/; ls/cat/head/tail/grep/wc/jq/awk/curl; git "
                            "add/commit/push; one command, no ';' '&&' '$()', no loops, no "
                            "redirection), or do it with the Read/Write/Edit tools, or skip it and "
                            "note the skip in the run log.]")


def _under_root(p):
    return p.startswith(PROTEUS_ROOT) or p == PROTEUS_ROOT.rstrip("/")


QUOTED = re.compile(r'"(?:[^"\\]|\\.)*"|\'[^\']*\'', re.S)


def _mask_quotes(cmd):
    """Replace the inside of quoted arguments with a neutral token. A commit message containing the
    word "for", a newline, or a regex with "|" is an argument, not shell syntax (found by the first
    nightly run, 2026-09-22). Command substitution and backticks inside double quotes still
    execute, so those are checked on the raw string first."""
    return QUOTED.sub('"ARG"', cmd)


def bash_ok(cmd):
    """Return None if the command is safe to auto-allow, else the reason it is not."""
    if "$(" in cmd or "`" in cmd:
        return "Command substitution or backticks are not verifiable here, even inside quotes."
    masked = _mask_quotes(cmd)
    if COMPLEX.search(masked):
        return "Compound shell (loop, ';', '&&', '$()' or backticks) is not verifiable here."
    if REDIRECT.search(masked):
        return "Shell redirection writes files outside the permission model; use the Write tool."
    for seg in masked.split("|"):
        seg = seg.strip()
        if not seg:
            return "Empty pipe segment."
        parts = seg.split()
        head = parts[0]
        if _under_root(head):
            continue
        if head in ("node", "bash", "sh", "python3", "python", VENV_PY, VENV_PY_ALT):
            if len(parts) > 1 and _under_root(parts[1]):
                continue
            if head == "node" and len(parts) > 1 and parts[1] == "-e":
                continue
            if head in ("python3", "python", VENV_PY, VENV_PY_ALT) and len(parts) > 1 and parts[1] in ("-c", "-m"):
                continue
            return "'%s' is allowed only for scripts under %s (absolute path), 'node -e', or 'python3 -c/-m'." % (head, PROTEUS_ROOT)
        if head == "git":
            verb = parts[1] if len(parts) > 1 else ""
            if verb == "-C":
                if len(parts) < 4 or not _under_root(parts[2]):
                    return "git -C is allowed only inside %s." % PROTEUS_ROOT
                verb = parts[3]
            if verb in GIT_READ:
                continue
            if verb in GIT_WRITE:
                if verb in ("push", "pull", "fetch"):
                    remote_args = [p for p in parts if not p.startswith("-") and p not in ("git", "-C", verb) and not _under_root(p)]
                    if remote_args and not (remote_args[0] in ("origin",) or remote_args[0].startswith("proteus-")):
                        return "git %s is allowed only to origin or a proteus-* remote." % verb
                continue
            return "git verb '%s' is not on the Proteus safe list." % verb
        if head == "gh":
            if len(parts) > 1 and parts[1] in GH_READ:
                if len(parts) > 2 and parts[2] in ("create", "delete", "edit", "login", "logout", "refresh"):
                    return "gh %s %s is an interactive-session job." % (parts[1], parts[2])
                continue
            return "gh is read-only here."
        if head in SAFE_CMDS:
            if head == "sed" and "-i" in parts:
                return "sed -i edits in place; use the Edit tool."
            if head in ("mkdir", "touch"):
                targets = [p for p in parts[1:] if not p.startswith("-")]
                if not targets or not all(_under_root(t) for t in targets):
                    return "%s is allowed only under %s." % (head, PROTEUS_ROOT)
            continue
        return "'%s' is not on the unattended safe list." % head
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    session_id = data.get("session_id") or ""
    if not session_id or not marker_active(session_id):
        sys.exit(0)

    tool = data.get("tool_name", "") or ""
    ti = data.get("tool_input", {}) or {}
    CTX["session"], CTX["mode"], CTX["tool"], CTX["ti"] = session_id, data.get("permission_mode"), tool, ti

    if tool in FREE_TOOLS:
        path = ti.get("file_path") or ti.get("path") or ""
        if path and not path.startswith(READ_ROOTS):
            deny("%s outside %s." % (tool, READ_ROOTS[0]))
        decide("allow", "%s is read-only and inside the run's scope." % tool)

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if path.startswith(WRITE_ROOTS):
            decide("allow", "Inside the Proteus write roots.")
        deny("%s to %s is outside the Proteus write roots (%s). Proteus writes its own folder and "
             "the vault mirror folder, nothing else." % (tool, path or "(no path)", ", ".join(WRITE_ROOTS)))

    if tool == "Bash":
        why = bash_ok((ti.get("command", "") or "").strip())
        if why is None:
            decide("allow", "On the Proteus unattended Bash safe list.")
        deny(why)

    if tool.startswith("mcp__Claude_Browser__"):
        decide("allow", "Browser pane reads are in scope; the charter forbids state-changing clicks.")

    deny("Tool '%s' is not available in an unattended Proteus run." % tool)


if __name__ == "__main__":
    main()
