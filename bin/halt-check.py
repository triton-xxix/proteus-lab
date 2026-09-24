#!/usr/bin/env python3
"""The kill switch, checked from three places, failing closed.

    python3 /Users/triton/PROTEUS/bin/halt-check.py            exit 0 = clear, anything else = halted
    python3 /Users/triton/PROTEUS/bin/halt-check.py --report   the week's halts as a Field Notes block

Sources, any one of which halts:

  1. The local file /Users/triton/PROTEUS/HALT. Touched by hand on the Mac. Always wins, never
     touched by this script unless it wrote the file itself (see "mirror" below).
  2. A file called HALT at the head of origin/main on GitHub. Needs push rights to the repo.
  3. An OPEN GitHub issue on the repo whose title starts with HALT and whose author is on
     HALT_AUTHORS. This is the phone handle: GitHub app, repo, Issues, +, title HALT, create.
     Anyone on the internet can open an issue on a public repo; only the author login, which
     GitHub sets and nobody can forge, decides whether it counts. Strangers' issues are ignored
     and counted in the log.

Fail closed. If the remote check cannot complete (no network, timeout, bad JSON, git error,
anything unexpected), the exit code is non-zero and the caller stops. A skipped night is the cost
of a check that could not run; a night that ran because the check broke is the thing this guards
against. A transient failure is logged but does not write the local file, so the next run checks
again rather than waiting for a hand on the Mac.

Mirror. When a remote source halts, the script writes the local HALT file with a first line of
"mirror: ..." so every other check (the send script, the hook) sees the same switch without a
network call. When the remote source is gone again (issue closed, file deleted from main) and
the local file is a mirror this script wrote, the script removes it and logs the release. A local
file written by a person (no "mirror:" first line) is never removed here; that is `rm` on the Mac.

Every set, release and failed check is one line in state/runs/YYYY-MM-DD.md, and --report gathers
the week's lines for Field Notes so a halt cannot pass unnoticed.

Exit codes: 0 clear, 3 halted (any source), 4 the check itself failed (treated as halted by every
caller; the distinction is only for the log).
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

ROOT = "/Users/triton/PROTEUS/"
HALT = os.environ.get("PROTEUS_HALT_FILE", ROOT + "HALT")           # test harness only; nothing in a run sets it
RUNS = os.environ.get("PROTEUS_HALT_RUNS", ROOT + "state/runs/")   # test harness redirects the log
REPO = "triton-xxix/proteus-lab"
REMOTE = os.environ.get("PROTEUS_HALT_REMOTE", "origin")          # test harness points this at a bare repo
ISSUES_URL = os.environ.get("PROTEUS_HALT_ISSUES_URL",             # test harness points this at a file://
                            "https://api.github.com/repos/%s/issues?state=open&per_page=50" % REPO)
TIMEOUT_S = float(os.environ.get("PROTEUS_HALT_TIMEOUT", "45"))
MIRROR_TAG = "mirror:"

# Logins whose open HALT issue counts. GitHub sets the author login; it cannot be forged.
# Luke's personal login, if he has one, is one line here (and he must be able to close it too).
HALT_AUTHORS = ("triton-xxix",)


def now():
    return time.strftime("%H:%M")


def log(line):
    os.makedirs(RUNS, exist_ok=True)
    day = time.strftime("%Y-%m-%d")
    with open(RUNS + day + ".md", "a") as fh:
        fh.write("%s %s\n" % (now(), line))


def local_state():
    """('none' | 'person' | 'mirror', first line or '')."""
    if not os.path.exists(HALT):
        return "none", ""
    try:
        with open(HALT) as fh:
            first = fh.readline().strip()
    except Exception:
        return "person", ""
    if first.startswith(MIRROR_TAG):
        return "mirror", first
    return "person", first


def git(*args):
    p = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True, timeout=TIMEOUT_S)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def remote_file():
    """None if no HALT file on the remote main, else a description string. Raises on any failure."""
    rc, out, err = git("fetch", "--quiet", REMOTE, "main")
    if rc != 0:
        raise RuntimeError("git fetch %s main failed: %s" % (REMOTE, (err or out)[:160]))
    rc, _, _ = git("cat-file", "-e", "FETCH_HEAD:HALT")
    if rc != 0:
        return None
    rc, who, _ = git("log", "-1", "--format=%an %aI %h", "FETCH_HEAD", "--", "HALT")
    rc2, body, _ = git("show", "FETCH_HEAD:HALT")
    body = body.splitlines()[0].strip() if body else ""
    return "HALT file on %s/main, committed by %s%s" % (REMOTE, who or "unknown", (": " + body) if body else "")


def remote_issue():
    """None if no open HALT issue by an allowed author, else a description. Raises on any failure.
    Returns (description, ignored_count)."""
    req = urllib.request.Request(ISSUES_URL, headers={"Accept": "application/vnd.github+json",
                                                      "User-Agent": "proteus-halt-check"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not isinstance(data, list):
        raise RuntimeError("issues API returned %s, not a list" % type(data).__name__)
    ignored = 0
    for it in data:
        if "pull_request" in it:
            continue
        title = (it.get("title") or "").strip()
        if not title.upper().startswith("HALT"):
            continue
        author = ((it.get("user") or {}).get("login") or "")
        if it.get("state") != "open":
            continue
        if author not in HALT_AUTHORS:
            ignored += 1
            continue
        return ("issue #%s \"%s\" opened by %s at %s %s" % (it.get("number"), title[:60], author,
                                                            it.get("created_at"), it.get("html_url") or ""), ignored)
    return None, ignored


def check():
    kind, first = local_state()
    if kind == "person":
        log("HALT set (local file%s); stopped" % ((": " + first) if first else ""))
        print("HALTED local file" + ((": " + first) if first else ""))
        return 3

    try:
        f = remote_file()
        issue, ignored = remote_issue()
    except Exception as e:  # noqa: BLE001  fail closed, whatever it was
        reason = "%s: %s" % (type(e).__name__, str(e)[:200])
        if kind == "mirror":
            log("HALT check failed (%s); local mirror stays: %s" % (reason, first))
            print("HALTED mirror (remote check failed: %s): %s" % (reason, first))
            return 3
        log("HALT check FAILED (%s); treated as halted, run skipped" % reason)
        print("HALTED: remote check failed, treating as halted: " + reason)
        return 4

    if ignored:
        log("HALT: %d open HALT-titled issue(s) from logins not on the list, ignored" % ignored)

    source = f or issue
    if source:
        if kind == "mirror" and first == MIRROR_TAG + " " + source:
            log("HALT still set remotely: %s" % source)
        else:
            with open(HALT, "w") as fh:
                fh.write("%s %s\nSet by bin/halt-check.py at %s. Clear the remote source; this file "
                         "then clears itself on the next check.\n" % (MIRROR_TAG, source, time.strftime("%Y-%m-%d %H:%M")))
            log("HALT SET REMOTELY: %s" % source)
        print("HALTED remote: " + source)
        return 3

    if kind == "mirror":
        try:
            os.remove(HALT)
            log("HALT released: remote source gone, mirror removed (was: %s)" % first)
            print("CLEAR (mirror released: %s)" % first)
        except Exception as e:  # noqa: BLE001
            log("HALT mirror could not be removed (%s); still halted" % e)
            print("HALTED mirror (could not remove): %s" % e)
            return 3
        return 0

    print("CLEAR")
    return 0


def report(days=7):
    """Markdown block for Field Notes: every halt line from the last `days` run logs."""
    cutoff = time.time() - days * 86400
    lines = []
    for i in range(days + 1):
        day = time.strftime("%Y-%m-%d", time.localtime(cutoff + i * 86400))
        path = RUNS + day + ".md"
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            for raw in fh:
                s = raw.strip()
                if s[:5].replace(":", "").isdigit() and "HALT" in s[6:]:
                    lines.append("- %s %s" % (day, s))
    kind, first = local_state()
    out = ["## Kill switch"]
    if not lines and kind == "none":
        out.append("Not pulled this week. No halt set, no remote halt seen, no failed check. The local file is absent.")
    else:
        sets = sum(1 for l in lines if "HALT SET REMOTELY" in l or "HALT set (local" in l)
        fails = sum(1 for l in lines if "HALT check FAILED" in l)
        out.append("Pulled %d time(s) this week, %d failed check(s). Every line the runs logged:" % (sets, fails))
        out.extend(lines or ["- (no lines in the run logs)"])
        if kind != "none":
            out.append("")
            out.append("**The local HALT file is present right now** (%s%s). Nothing is sent or pushed until it is gone."
                       % (kind, (": " + first) if first else ""))
    return "\n".join(out)


def main():
    if "--report" in sys.argv:
        print(report())
        return 0
    try:
        return check()
    except Exception as e:  # noqa: BLE001  the last net: any bug in this file is a halt, not a run
        try:
            log("HALT check CRASHED (%s: %s); treated as halted" % (type(e).__name__, str(e)[:160]))
        except Exception:
            pass
        print("HALTED: check crashed: %s" % e)
        return 4


if __name__ == "__main__":
    sys.exit(main())
