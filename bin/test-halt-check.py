#!/usr/bin/env python3
"""Test harness for bin/halt-check.py: every source, every failure path, the mirror lifecycle.

    python3 /Users/triton/PROTEUS/bin/test-halt-check.py

Nothing touches the real HALT file, the real run log or GitHub. A bare repo in a temp dir stands in
for origin, a JSON file stands in for the issues API, a socket that accepts and never answers stands
in for a hung GitHub. Exit 0 on all pass, 1 otherwise.
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time

ROOT = "/Users/triton/PROTEUS/"
CHECK = ROOT + "bin/halt-check.py"
ALLOWED = "triton-xxix"


def sh(*args, cwd=None):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def run(env, *args):
    full = dict(os.environ)
    full.update(env)
    p = subprocess.run([sys.executable, CHECK] + list(args), env=full, capture_output=True, text=True, timeout=60)
    return p.returncode, (p.stdout + p.stderr).strip()


class Harness:
    def __init__(self):
        self.tmp = tempfile.mkdtemp(prefix="proteus-halt-test-")
        self.bare = os.path.join(self.tmp, "origin.git")
        self.work = os.path.join(self.tmp, "work")
        self.runs = os.path.join(self.tmp, "runs") + "/"
        self.halt = os.path.join(self.tmp, "HALT")
        self.issues = os.path.join(self.tmp, "issues.json")
        sh("git", "init", "--bare", "-q", "-b", "main", self.bare)
        sh("git", "init", "-q", "-b", "main", self.work)
        sh("git", "-C", self.work, "config", "user.email", "test@proteus.invalid")
        sh("git", "-C", self.work, "config", "user.name", "Test Author")
        with open(os.path.join(self.work, "README"), "w") as fh:
            fh.write("stand-in for the lab\n")
        sh("git", "-C", self.work, "add", "-A")
        sh("git", "-C", self.work, "commit", "-q", "-m", "init")
        sh("git", "-C", self.work, "push", "-q", self.bare, "main")
        self.set_issues([])

    def env(self, **extra):
        e = {"PROTEUS_HALT_REMOTE": self.bare, "PROTEUS_HALT_ISSUES_URL": "file://" + self.issues,
             "PROTEUS_HALT_RUNS": self.runs, "PROTEUS_HALT_FILE": self.halt, "PROTEUS_HALT_TIMEOUT": "20"}
        e.update(extra)
        return e

    def set_issues(self, items):
        with open(self.issues, "w") as fh:
            json.dump(items, fh)

    def remote_halt(self, present, body="phone says stop"):
        path = os.path.join(self.work, "HALT")
        if present:
            with open(path, "w") as fh:
                fh.write(body + "\n")
            sh("git", "-C", self.work, "add", "HALT")
            sh("git", "-C", self.work, "commit", "-q", "-m", "HALT")
        else:
            sh("git", "-C", self.work, "rm", "-q", "HALT")
            sh("git", "-C", self.work, "commit", "-q", "-m", "clear HALT")
        sh("git", "-C", self.work, "push", "-q", self.bare, "main")

    def log_text(self):
        out = []
        if os.path.isdir(self.runs):
            for name in sorted(os.listdir(self.runs)):
                with open(self.runs + name) as fh:
                    out.append(fh.read())
        return "\n".join(out)

    def halt_first_line(self):
        if not os.path.exists(self.halt):
            return None
        with open(self.halt) as fh:
            return fh.readline().strip()

    def close(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


def issue(number, title, login, state="open"):
    return {"number": number, "title": title, "state": state, "created_at": "2026-09-24T21:00:00Z",
            "html_url": "https://github.com/x/y/issues/%d" % number, "user": {"login": login}}


def hung_server():
    """A TCP listener that accepts and never replies. Returns (port, stop)."""
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(5)
    held = []
    stop = threading.Event()

    def loop():
        srv.settimeout(0.5)
        while not stop.is_set():
            try:
                c, _ = srv.accept()
                held.append(c)
            except socket.timeout:
                continue
    t = threading.Thread(target=loop, daemon=True)
    t.start()

    def stopper():
        stop.set()
        for c in held:
            c.close()
        srv.close()
    return srv.getsockname()[1], stopper


def main():
    h = Harness()
    fails = 0

    def case(name, got, want, extra_ok=True):
        nonlocal fails
        ok = got == want and extra_ok
        fails += 0 if ok else 1
        print(("PASS" if ok else "FAIL"), name, "want", want, "got", got)

    try:
        # 1. everything clear
        rc, out = run(h.env())
        case("clear", rc, 0, "CLEAR" in out)

        # 2. local file written by a person: halts, never removed
        with open(h.halt, "w") as fh:
            fh.write("luke, by hand\n")
        rc, out = run(h.env())
        case("local person file halts", rc, 3, "local file" in out and h.halt_first_line() == "luke, by hand")
        os.remove(h.halt)

        # 3. HALT file on origin/main: halts, mirrors, logs author
        h.remote_halt(True)
        rc, out = run(h.env())
        first = h.halt_first_line() or ""
        case("remote file halts", rc, 3, "Test Author" in out and first.startswith("mirror:"))
        case("remote file logged", "HALT SET REMOTELY" in h.log_text(), True)
        # second check: still halted, no duplicate SET line
        rc, out = run(h.env())
        case("remote file still halts", rc, 3, h.log_text().count("HALT SET REMOTELY") == 1)

        # 4. clear it on the remote: mirror released, logged
        h.remote_halt(False)
        rc, out = run(h.env())
        case("remote cleared releases mirror", rc, 0, not os.path.exists(h.halt) and "HALT released" in h.log_text())

        # 5. issue by the allowed login: halts
        h.set_issues([issue(7, "HALT: grinder looks wrong", ALLOWED)])
        rc, out = run(h.env())
        case("issue by allowed login halts", rc, 3, "#7" in out and (h.halt_first_line() or "").startswith("mirror:"))

        # 6. issue by a stranger: ignored, logged, clear (the mirror from 5 is released)
        h.set_issues([issue(8, "HALT now please", "some-stranger"), issue(9, "halt", "another")])
        rc, out = run(h.env())
        case("stranger issues ignored", rc, 0, not os.path.exists(h.halt) and "not on the list, ignored" in h.log_text())

        # 7. closed issue by the allowed login: clear
        h.set_issues([issue(10, "HALT", ALLOWED, state="closed")])
        rc, out = run(h.env())
        case("closed issue is clear", rc, 0)

        # 8. issue with a title that does not start with HALT: clear
        h.set_issues([issue(11, "Question about HALT", ALLOWED)])
        rc, out = run(h.env())
        case("non-HALT title is clear", rc, 0)

        # 9. a pull request titled HALT: not an issue, clear
        pr = issue(12, "HALT", ALLOWED)
        pr["pull_request"] = {"url": "x"}
        h.set_issues([pr])
        rc, out = run(h.env())
        case("pull request titled HALT is clear", rc, 0)
        h.set_issues([])

        # 10. remote refused: fail closed, exit 4, no mirror file written
        rc, out = run(h.env(PROTEUS_HALT_REMOTE=os.path.join(h.tmp, "nowhere.git")))
        case("fetch refused fails closed", rc, 4, not os.path.exists(h.halt) and "HALT check FAILED" in h.log_text())

        # 11. issues API unreachable: fail closed
        rc, out = run(h.env(PROTEUS_HALT_ISSUES_URL="file://" + os.path.join(h.tmp, "missing.json")))
        case("issues feed missing fails closed", rc, 4)

        # 12. issues API returns garbage: fail closed
        with open(h.issues, "w") as fh:
            fh.write("<html>rate limited</html>")
        rc, out = run(h.env())
        case("issues feed garbage fails closed", rc, 4)
        h.set_issues([])

        # 13. issues API hangs: the timeout fires, fail closed, in bounded time
        port, stop = hung_server()
        t0 = time.time()
        rc, out = run(h.env(PROTEUS_HALT_ISSUES_URL="http://127.0.0.1:%d/issues" % port, PROTEUS_HALT_TIMEOUT="2"))
        stop()
        case("hung issues API fails closed", rc, 4, time.time() - t0 < 15)

        # 14. git fetch hangs: same
        port, stop = hung_server()
        t0 = time.time()
        rc, out = run(h.env(PROTEUS_HALT_REMOTE="git://127.0.0.1:%d/x.git" % port, PROTEUS_HALT_TIMEOUT="2"))
        stop()
        case("hung git remote fails closed", rc, 4, time.time() - t0 < 15)

        # 15. check fails while a mirror is present: stays halted, mirror kept
        h.set_issues([issue(13, "HALT", ALLOWED)])
        run(h.env())
        rc, out = run(h.env(PROTEUS_HALT_REMOTE=os.path.join(h.tmp, "nowhere.git")))
        case("failed check keeps the mirror", rc, 3, (h.halt_first_line() or "").startswith("mirror:"))
        h.set_issues([])
        run(h.env())

        # 16. a person's file is never removed by a clear remote
        with open(h.halt, "w") as fh:
            fh.write("\n")
        rc, out = run(h.env())
        case("empty person file halts and stays", rc, 3, os.path.exists(h.halt))
        os.remove(h.halt)

        # 17. --report lists the week's lines
        rc, out = run(h.env(), "--report")
        case("report", rc, 0, "## Kill switch" in out and "HALT SET REMOTELY" in out and "FAILED" in out)
    finally:
        h.close()
    n = 19
    print("%d cases, %d failed" % (n, fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
