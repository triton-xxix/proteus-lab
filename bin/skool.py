#!/usr/bin/env python3
"""The Skool reading step of the nightly (field-notes/SKOOL-READING-PLAN.md).

    python3 /Users/triton/PROTEUS/bin/skool.py next [--n 2]   # assign up to N groups, write child prompts
    python3 /Users/triton/PROTEUS/bin/skool.py ingest          # collect digests, log, add to Field Notes
    python3 /Users/triton/PROTEUS/bin/skool.py status

`next` prints one GO line per group with the model and the prompt file; the parent spawns one
child per line with that file's text as the whole prompt. `ingest` marks a group read when its
digest exists and has a verdict line, puts it back in the queue otherwise (one retry, then it is
parked), appends one line per group to the run log and to this week's Field Notes draft under
"## Skool reading", and commits the queue, the digests and the draft. Nothing is fetched here: the
nightly reads local files only, pulls happen in interactive sessions.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime

ROOT = "/Users/triton/PROTEUS/"
QUEUE = ROOT + "field-notes/SKOOL-QUEUE.json"
OUT = ROOT + "state/agents/skool/"
TOOLSHELF = ROOT + "field-notes/toolshelf.jsonl"
MAX_TRIES = 2

BRIEF = """You are a reading child for Proteus, running unattended on {model}. Tonight's group: {gid}, "{title}".
Why this group: {why}

Read these local files with the Read tool (large ones in chunks with offset and limit):
{files}
For what Proteus already has, read {toolshelf} and skim /Users/triton/PROTEUS/PERSONA.md.
Earlier digests, if any, are in /Users/triton/PROTEUS/state/agents/skool/; do not repeat what they say.

Write exactly one file with the Write tool: {out}
Use exactly these headings, plain English, UK spelling, no em dashes:

# {gid}: {title}
## What it teaches
Five lines at most. The mechanism, not the marketing.
## Tools they use
One line each, with a URL if the transcript names one.
## What Proteus already has that does the same job
Name it from the toolshelf or the stack (Claude Code with skills, sub-agents, scheduled tasks and a
PreToolUse hook; launchd pollers; keyless YouTube, HN, GitHub, arXiv pulls; HyperFrames; local whisper;
Ollama; freqtrade). Say "nothing" if nothing.
## What we would need to fetch
Tools, repos or services, free first. "Nothing" is a fine answer.
## One thing worth trying
One concrete test, runnable in /Users/triton/PROTEUS/sandbox/ in under 30 minutes without accounts,
keys or spend if possible, and how big it is. If there is none, say so.
## Claims to check
Up to three specific claims (a number, a speed, a cost), each quoted in under 15 words, with how
Proteus could check it.
## Verdict
One line starting with exactly one of TRY, PARK or SKIP, then a reason.

Rules, each enforced by a hook that will refuse you: you cannot spawn agents, run git, or run
anything in /Users/triton/PROTEUS/bin/; you may write only under /Users/triton/PROTEUS/state/agents/
or /Users/triton/PROTEUS/sandbox/. No web fetches: local files only. A refusal is a result to report,
not a problem to route around. Your final message is two lines: the verdict line, and any refusals.
"""


def load():
    return json.load(open(QUEUE))


def save(q):
    with open(QUEUE, "w") as fh:
        json.dump(q, fh, indent=1)
        fh.write("\n")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def digest_path(g, day):
    return OUT + "%s-%s.md" % (day, g["id"])


def cmd_next(a):
    q = load(); day = today()
    os.makedirs(OUT, exist_ok=True)
    ready = []
    for g in q["groups"]:
        if g["status"] != "queued":
            continue
        missing = [f for f in g["files"] if not os.path.exists(ROOT + f)]
        if not g["files"]:
            g["status"] = "needs-pull"; g["note"] = "no files listed"
            continue
        if missing:
            # files listed but not on disk yet: a transcription batch is still running, so wait
            g["note"] = "waiting on: %s" % ", ".join(missing[:3])
            continue
        g.pop("note", None)
        ready.append(g)
    for g in ready[:a.n]:
        prompt = BRIEF.format(model=g["model"], gid=g["id"], title=g["title"], why=g.get("why", ""),
                              files="\n".join("- " + ROOT + f for f in g["files"]), toolshelf=TOOLSHELF,
                              out=digest_path(g, day))
        pfile = OUT + "%s-%s.prompt.md" % (day, g["id"])
        open(pfile, "w").write(prompt)
        g["status"] = "assigned"; g["assigned"] = day; g["tries"] = g.get("tries", 0) + 1
        print("GO %s model=%s prompt=%s expect=%s" % (g["id"], g["model"], pfile, digest_path(g, day)))
    save(q)
    if not ready:
        pulls = [g["id"] for g in q["groups"] if g["status"] == "needs-pull"]
        print("STOP: nothing local to read%s" % (" (needs an interactive pull: %s)" % ", ".join(pulls) if pulls else ""))


def verdict_of(text):
    m = re.search(r"^## Verdict\s*\n+\s*(TRY|PARK|SKIP)\b(.*)$", text, re.M)
    return (m.group(1), m.group(2).strip(" :-.")) if m else (None, None)


def cmd_ingest(a):
    q = load(); lines = []
    for g in q["groups"]:
        if g["status"] != "assigned":
            continue
        p = digest_path(g, g["assigned"])
        text = open(p).read() if os.path.exists(p) else ""
        v, why = verdict_of(text)
        if v:
            g["status"] = "read"; g["verdict"] = v; g["digest"] = p.replace(ROOT, "")
            lines.append("- Skool %s read (%s): **%s** %s. Digest `%s`." % (g["id"], g["title"], v, why, g["digest"]))
        else:
            g["status"] = "queued" if g.get("tries", 0) < MAX_TRIES else "parked"
            lines.append("- Skool %s: no usable digest (%s); %s." % (g["id"], "file missing" if not text else "no verdict line", g["status"]))
    save(q)
    if not lines:
        print("nothing assigned"); return
    day = today()
    with open(ROOT + "state/runs/%s.md" % day, "a") as fh:
        fh.write("\n".join(lines) + "\n")
    wk = datetime.now().strftime("%G-W%V")
    draft = ROOT + "field-notes/drafts/%s.md" % wk
    if os.path.exists(draft):
        d = open(draft).read()
        if "## Skool reading" not in d:
            d = d.rstrip("\n") + "\n\n## Skool reading\n\n"
        d = d.rstrip("\n") + "\n" + "\n".join(l for l in lines if " read (" in l) + "\n"
        open(draft, "w").write(d)
    print("\n".join(lines))
    if os.path.exists(ROOT + "HALT"):
        print("HALT set: written, not committed"); return
    files = [QUEUE, draft, OUT] if os.path.exists(draft) else [QUEUE, OUT]
    subprocess.run(["git", "-C", ROOT, "add"] + files, check=False)
    # named paths (2026-10-09): a bare commit took whatever another session had staged
    r = subprocess.run(["git", "-C", ROOT, "commit", "-q", "-m", "skool: reading digests %s" % day, "--"] + files, capture_output=True, text=True)
    if r.returncode == 0:
        subprocess.run(["git", "-C", ROOT, "push", "-q", "origin", "main"], check=False)
        print("committed and pushed")


def cmd_status(a):
    for g in load()["groups"]:
        print("%s %-10s %-6s %s %s" % (g["id"], g["status"], g["model"], g.get("verdict", ""), g["title"]))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("next"); s.add_argument("--n", type=int, default=2); s.set_defaults(f=cmd_next)
    sp.add_parser("ingest").set_defaults(f=cmd_ingest)
    sp.add_parser("status").set_defaults(f=cmd_status)
    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
