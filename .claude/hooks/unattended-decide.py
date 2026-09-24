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

# Shell syntax is decided by _scan() below, which tracks quote state the way bash does.
# There is deliberately no regex over the raw command: text inside quotes is an argument,
# and text outside quotes is syntax, and no pattern can tell those apart reliably.


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
                # Added 2026-09-24 for the sub-agent experiment: which caller the input names.
                # agent_id/agent_type are what Claude Code attaches to a sub-agent's calls, if it
                # attaches anything. "keys" lists the top-level input fields so the shape is on record.
                "agent_id": CTX.get("agent_id"),
                "agent_type": CTX.get("agent_type"),
                "cwd": CTX.get("cwd"),
                "keys": CTX.get("keys"),
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


def _norm(p):
    """Absolute, '..'-free, symlink-free form of p, or None if p is not an absolute path.

    Relative paths return None on purpose. Resolving them against the cwd would make a
    bare word like "upstream" look like a path inside the folder whenever the run happens
    to start there, which would quietly defeat the git remote check.
    """
    if not p.startswith("/") and not p.startswith("~"):
        return None
    try:
        return os.path.realpath(os.path.expanduser(p))
    except Exception:
        return None


def _under(p, root):
    q = _norm(p)
    if q is None:
        return False
    r = os.path.realpath(root)
    return q == r or q.startswith(r + os.sep)


def _under_root(p):
    """True for the Proteus folder itself and anything inside it.

    Both halves matter. The folder without a trailing slash is what `git -C` is normally
    given, and '..' has to be resolved before comparing or /Users/triton/PROTEUS/../OBSIDIAN
    reads as being inside the folder (both found 2026-09-22).
    """
    return _under(p, PROTEUS_ROOT)


def _scan(cmd):
    """Split a command into pipeline segments of argv tokens, honouring bash quoting rules.

    Returns (segments, None) or (None, reason). Each segment is a list of tokens with quotes
    removed, so the caller sees the same argv bash would build.

    The point is that quoting is tracked character by character rather than pattern-matched.
    A ';' inside quotes is text; a ';' outside quotes starts a second command; and an escaped
    \\' is a literal apostrophe that does NOT open a quoted string, which is exactly where a
    regex over the raw string goes wrong (found 2026-09-22: `echo a\\'b; rm -rf /` was allowed).
    """
    segs, words, tok, quote = [], [], None, None
    i, n = 0, len(cmd)

    def subst_at(j):
        return cmd[j] == "`" or cmd.startswith("$(", j) or cmd.startswith("${", j)

    while i < n:
        c = cmd[i]

        if quote == "'":                      # single quotes: everything is literal
            if c == "'":
                quote = None
            else:
                tok.append(c)
            i += 1
            continue

        if quote == '"':                      # double quotes: still expand and substitute
            if c == "\\" and i + 1 < n and cmd[i + 1] in '"\\$`':
                tok.append(cmd[i + 1])
                i += 2
                continue
            if c == '"':
                quote = None
                i += 1
                continue
            if subst_at(i) or c == "$":
                return None, "Substitution inside double quotes still runs; not verifiable here."
            tok.append(c)
            i += 1
            continue

        # unquoted from here
        if c == "\\":
            if i + 1 >= n:
                return None, "Trailing backslash."
            tok = tok if tok is not None else []
            tok.append(cmd[i + 1])
            i += 2
            continue

        if c in ("'", '"'):
            quote = c
            tok = tok if tok is not None else []
            i += 1
            continue

        if subst_at(i) or c == "$":
            return None, "Command or variable substitution is not verifiable here."

        if c == "|":
            if cmd.startswith("||", i):
                return None, "'||' chains two commands and is not verifiable here."
            if tok is not None:
                words.append("".join(tok))
                tok = None
            segs.append(words)
            words = []
            i += 1
            continue

        if c in ";&":
            return None, "'%s' outside quotes chains or backgrounds a command." % c
        if c in "<>":
            return None, "Shell redirection writes files outside the permission model; use the Write tool."
        if c in "()":
            return None, "Subshell grouping is not verifiable here."
        if c == "\n":
            return None, "A newline outside quotes starts a second command."

        if c.isspace():
            if tok is not None:
                words.append("".join(tok))
                tok = None
            i += 1
            continue

        tok = tok if tok is not None else []
        tok.append(c)
        i += 1

    if quote:
        return None, "Unbalanced quote."
    if tok is not None:
        words.append("".join(tok))
    segs.append(words)
    return segs, None


def bash_ok(cmd):
    """Return None if the command is safe to auto-allow, else the reason it is not."""
    segs, why = _scan(cmd)
    if why is not None:
        return why
    for parts in segs:
        if not parts:
            return "Empty pipe segment."
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
    CTX["agent_id"] = data.get("agent_id")
    CTX["agent_type"] = data.get("agent_type")
    CTX["cwd"] = data.get("cwd")
    CTX["keys"] = sorted(data.keys())

    if tool in FREE_TOOLS:
        path = ti.get("file_path") or ti.get("path") or ""
        if path and not any(_under(path, r) for r in READ_ROOTS):
            deny("%s outside %s." % (tool, READ_ROOTS[0]))
        decide("allow", "%s is read-only and inside the run's scope." % tool)

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if any(_under(path, r) for r in WRITE_ROOTS):
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
