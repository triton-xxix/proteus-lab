#!/usr/bin/env python3
"""The private live dashboard (Luke, 7 Oct 2026: "live, but private... be a little bit cautious").

    python3 /Users/triton/PROTEUS/bin/dash.py                  # gather and seal docs/dash/payload.json
    python3 /Users/triton/PROTEUS/bin/dash.py --commit         # the same, then commit and push the payload alone
    python3 /Users/triton/PROTEUS/bin/dash.py --print          # the plaintext, for a look
    python3 /Users/triton/PROTEUS/bin/dash.py --email-body IN OUT   # copy a note and append the URL and passphrase footer
    python3 /Users/triton/PROTEUS/bin/dash.py --link           # print the unlock link

What it is: a passphrase-locked page at https://triton-xxix.github.io/proteus-lab/dash/ that shows where
everything sits, rebuilt by every run (each probe verdict, the close commit, the mirror) so it moves during
the nightly. The payload is sealed by bin/dash-seal.cjs (AES-256-GCM, PBKDF2) with a passphrase generated once
into state/dash.key, which is gitignored and never leaves this Mac. Honest limit: the proteus-lab repo is
public, so the lock protects the assembled view and the convenience, not secrets. Standard library only; the
numbers come from bin/home.py's own builders so the vault front page and the dashboard never disagree.
"""
import csv
import glob
import hashlib
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = "/Users/triton/PROTEUS/"
KEY = ROOT + "state/dash.key"
LAST = ROOT + "state/dash.last"
OUT = ROOT + "docs/dash/payload.json"
SEAL = ROOT + "bin/dash-seal.cjs"
NODE = "/usr/local/bin/node"
URL = "https://triton-xxix.github.io/proteus-lab/dash/"
ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"


def home():
    spec = importlib.util.spec_from_file_location("home", ROOT + "bin/home.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ensure_key():
    if os.path.exists(KEY):
        return json.load(open(KEY))
    os.makedirs(os.path.dirname(KEY), exist_ok=True)
    # bin/secrets.py shadows the stdlib `secrets` module on sys.path, so use SystemRandom and os.urandom.
    rng = random.SystemRandom()
    phrase = "-".join("".join(rng.choice(ALPHABET) for _ in range(4)) for _ in range(5))
    import base64
    key = {"passphrase": phrase, "salt": base64.b64encode(os.urandom(16)).decode(), "created": datetime.now(timezone.utc).isoformat()}
    fd = os.open(KEY, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as fh:
        json.dump(key, fh)
    return key


def read(path, n=None):
    try:
        text = open(path).read()
    except OSError:
        return ""
    return text if n is None else "\n".join(text.splitlines()[-n:])


def jload(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default


def md_section(lines):
    """home.py's builders return Markdown lines; keep them as text blocks."""
    return "\n".join(lines).strip()


def run_logs():
    return sorted(glob.glob(ROOT + "state/runs/2*.md"))


def now_block():
    marker = jload(ROOT + "state/unattended-session.json", {})
    loops = sorted(glob.glob(ROOT + "state/probe-loop*/*.json")) + sorted(glob.glob(ROOT + "state/probe-loops/*.json"))
    loop = jload(loops[-1], {}) if loops else {}
    logs = run_logs()
    latest = logs[-1] if logs else ""
    return {
        "halt": os.path.exists(ROOT + "HALT"),
        "marker": {"task": marker.get("task"), "session": (str(marker.get("session_id"))[:8] if marker.get("session_id") else None),
                   "live": bool(marker.get("session_id")) and marker.get("session_id") != "closed"},
        "loop": {k: loop.get(k) for k in ("date", "started_at", "stopped_at", "stop_reason", "deadline", "probes") if k in loop},
        "run_log_file": os.path.basename(latest),
        "run_log_tail": read(latest, 14) if latest else "",
    }


def probes_block():
    d = jload(ROOT + "state/probes.json", {"items": []})
    items = d.get("items", [])
    done = sorted([p for p in items if p.get("status") == "done"], key=lambda p: p.get("verdict_at") or "")
    tally = {}
    for p in done:
        tally[p.get("verdict")] = tally.get(p.get("verdict"), 0) + 1
    return {
        "tally": tally,
        "killed": sum(p.get("status") == "killed" for p in items),
        "in_progress": [{"id": p["id"], "title": p["title"], "since": p.get("started_at")} for p in items if p.get("status") == "in-progress"],
        "queue": [{"id": p["id"], "title": p["title"][:110], "after": p.get("after"), "needs": (p.get("needs") or "")[:100], "source": p.get("source")} for p in items if p.get("status") == "open"],
        "last": [{"id": p["id"], "verdict": p.get("verdict"), "when": (p.get("verdict_at") or "")[:16], "note": (p.get("note") or "")[:220]} for p in done[-6:][::-1]],
    }


def lichess_block():
    rows = list(csv.DictReader(open(ROOT + "games/lichess/GAMES.csv"))) if os.path.exists(ROOT + "games/lichess/GAMES.csv") else []
    wdl = {k: sum(1 for r in rows if r.get("result") == k) for k in ("win", "draw", "loss")}
    last = rows[-1] if rows else {}
    return {"games": len(rows), "wdl": wdl, "rating": last.get("my_rating_after"), "last": last.get("finished_utc"), "opponent": last.get("opponent"), "opp_rating": last.get("opp_rating"), "id": "tritonxxix"}


def expedition_block():
    chosen, lines = None, []
    for path in run_logs()[-21:]:
        for line in open(path):
            if "Big Expedition" in line or "rug-check" in line.lower():
                lines.append("%s: %s" % (os.path.basename(path)[:10], line.strip("- \n")[:200]))
            m = re.search(r"Big Expedition chosen: (.+?), fortnight (\d+ \w+) to (\d+ \w+)", line)
            if m:
                chosen = {"title": m.group(1), "from": m.group(2), "to": m.group(3)}
    return {"chosen": chosen, "lines": lines[-8:]}


def usage_block():
    text = read(ROOT + "USAGE.md")
    head = [l for l in text.splitlines()[:40] if l.startswith("|") or l.startswith("#") or l.startswith("Built")]
    return "\n".join(head[:24])


def backlog_block():
    text = read(ROOT + "BACKLOG.md")
    items = re.findall(r"^- \*\*(.+?)\*\*", text, re.M)
    return items[:16]


def commits_block():
    try:
        out = subprocess.run(["git", "-C", ROOT, "log", "-20", "--format=%h%x09%cI%x09%s"], capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return []
    return [dict(zip(("sha", "when", "msg"), l.split("\t", 2))) for l in out.splitlines() if l]


def sites_block():
    s = jload(ROOT + "sites/nolan/site.json", None)
    return [s] if s else []


def gather():
    h = home()
    return {
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "now": now_block(),
        "probes": probes_block(),
        "desks": {"grinder": md_section(h.grinder()), "pitch": md_section(h.pitch()), "jobs": md_section(h.jobs())},
        "expedition": expedition_block(),
        "lichess": lichess_block(),
        "money": md_section(h.spend()),
        "usage": usage_block(),
        "draft": md_section(h.draft()),
        "backlog": backlog_block(),
        "commits": commits_block(),
        "sites": sites_block(),
    }


def build(force=False):
    """Seal the payload. Returns the payload path when (re)built, None when unchanged."""
    key = ensure_key()
    data = gather()
    stable = dict(data); stable.pop("built_at", None)
    digest = hashlib.sha256(json.dumps(stable, sort_keys=True).encode()).hexdigest()
    if not force and os.path.exists(OUT) and read(LAST).strip() == digest:
        return None
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    r = subprocess.run([NODE, SEAL, KEY, OUT], input=json.dumps(data).encode(), capture_output=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError("seal failed: " + r.stderr.decode()[:200])
    open(LAST, "w").write(digest)
    return OUT


def commit():
    if os.path.exists(ROOT + "HALT"):
        print("HALT set: built, not committed"); return
    subprocess.run(["git", "-C", ROOT, "add", "--", OUT], check=False)
    r = subprocess.run(["git", "-C", ROOT, "commit", "-q", "-m", "dash: %s" % datetime.now().strftime("%H:%M"), "--", OUT], capture_output=True, text=True)
    if r.returncode == 0:
        subprocess.run(["git", "-C", ROOT, "push", "-q", "origin", "main"], check=False)
        print("dash: committed and pushed")
    else:
        print("dash: nothing to commit")


def link():
    return URL + "#k=" + ensure_key()["passphrase"]


def main():
    a = sys.argv[1:]
    if a[:1] == ["--print"]:
        print(json.dumps(gather(), indent=2, ensure_ascii=False)); return
    if a[:1] == ["--link"]:
        print(link()); return
    if a[:1] == ["--email-body"] and len(a) == 3:
        body = open(a[1]).read().rstrip("\n")
        body += "\n\n---\n\nThe private dashboard: %s\nPassphrase, if the link does not unlock it: %s\n" % (link(), ensure_key()["passphrase"])
        os.makedirs(os.path.dirname(a[2]), exist_ok=True)
        open(a[2], "w").write(body)
        print(a[2]); return
    out = build(force="--force" in a)
    print("dash: sealed %s" % out if out else "dash: unchanged")
    if "--commit" in a and out:
        commit()


if __name__ == "__main__":
    main()
