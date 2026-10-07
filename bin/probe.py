#!/usr/bin/env python3
"""The probe loop: turn idle capacity into verdicts, one probe at a time, until a budget is spent.

    python3 /Users/triton/PROTEUS/bin/probe.py start [--minutes N | --until HH:MM] [--calls N] [--probes N]
    python3 /Users/triton/PROTEUS/bin/probe.py next
    python3 /Users/triton/PROTEUS/bin/probe.py verdict P-0007 --verdict works|broken|blocked|not-worth-it \
                                              --note "..." [--artefact PATH ...]
    python3 /Users/triton/PROTEUS/bin/probe.py stop --reason "..."
    python3 /Users/triton/PROTEUS/bin/probe.py add "title" [--source backlog|intel|persona|desk|field-notes|harvest]
                                              [--needs "..."] [--after YYYY-MM-DD] [--est MINUTES]
    python3 /Users/triton/PROTEUS/bin/probe.py kill P-0015 --by rule|luke --reason "..."
    python3 /Users/triton/PROTEUS/bin/probe.py ask P-0011 --week YYYY-WW
    python3 /Users/triton/PROTEUS/bin/probe.py asks | cull [--apply]
    python3 /Users/triton/PROTEUS/bin/probe.py status | queue | render

Design (2026-09-24, Luke's prompt 5):
  - The queue and every verdict live in state/probes.json. PROBES.md at the root is rendered from
    it and is the register the charter asks for: date, what, verdict, artefact, cost.
  - `start` opens tonight's loop file under state/probe-loop/ with a hard deadline, a call cap and
    a probe cap. Nothing in this script can move the deadline once set.
  - `next` checks, in this order: HALT file, deadline, minutes floor, probe cap, call cap, then
    picks the first runnable item. An item whose estimate is over the time left but within
    FIT_STRETCH times it is runnable, after the ones that fit cleanly (7 Oct 2026). If nothing
    runnable is left it prints REFILL with the next unused source in REFILL-SOURCES.md (6 Oct,
    capped), and otherwise stops the loop with the reason in plain words (queue empty; everything
    left needs something I do not have; everything left is waiting on a date or on the Sunday
    cull; why no refill). It never invents a probe itself: a refill is a source to learn from.
  - `verdict` counts the tool calls and denials the unattended hook logged for this session since
    the probe started, writes the register line and the run-log entry, then commits and pushes
    just those files. Under HALT it logs and does not commit. One commit per probe: the timestamp
    is the proof that the verdict was reached that night.
  - Calls are the token proxy. The hook logs one line per tool call, so a call cap is a token cap
    that can be measured mid-run. In an interactive session no marker is bound and calls are not
    measured; time alone governs.
  - A probe left in_progress by a dead session counts as an attempt. Three attempts without a
    verdict and the item waits for the Sunday cull, which kills it as "could not make it run".

Kills and asks (2026-09-27, Luke's review of charter v2):
  - A kill is its own status, not a note in the needs column: killed_at, killed_by (rule or
    luke) and the reason. Kills render in PROBES.md and are counted by bin/score.py.
  - An ask for Luke's hands is made once. `ask` records the Field Notes week it appeared in;
    `asks` prints only the items that need Luke and have never been asked, so the weekly cannot
    repeat an ask. `cull` kills anything asked 28 days ago and still waiting, and anything at
    three attempts. Without --apply it only prints what it would do.

No sub-agents are used or spawned here. The loop is sequential inside one session.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta

ROOT = os.environ.get("PROTEUS_ROOT", "/Users/triton/PROTEUS/")
if not ROOT.endswith("/"):
    ROOT += "/"
STATE = ROOT + "state/probes.json"
LOOP_DIR = ROOT + "state/probe-loop/"
REGISTER = ROOT + "PROBES.md"
RUNS = ROOT + "state/runs/"
HALT = ROOT + "HALT"
MARKER = ROOT + "state/unattended-session.json"
DECISIONS = ROOT + "state/unattended-decisions-%s.jsonl"
NO_GIT = os.environ.get("PROBE_NO_GIT") == "1"

VERDICTS = ("works", "broken", "blocked", "not-worth-it")
SOURCE_RANK = {"backlog": 1, "intel": 2, "vault": 2, "persona": 3, "field-notes": 3, "harvest": 3, "desk": 4, "refill": 4}
# vault: threads the vault split out of links Luke sent it, judged by the harvest child (2026-09-29). His own
# links rank with the intelligence lane, above the automated harvest, below the backlog's own questions.
DEFAULT_MAX_MINUTES = 60      # the loop's own ceiling, whatever the night's deadline says
DEFAULT_MAX_CALLS = 150       # hook-logged tool calls, the token proxy
DEFAULT_MAX_PROBES = 6
MIN_PROBE_MINUTES = 8         # do not start a probe with less than this left
# Fit slack (7 Oct 2026). On 6 Oct the loop stopped with 28 min left because P-0068 was estimated at
# 30. Of 54 timed verdicts to that night, none ran over its estimate; the longest took 12 min of 15
# and the median took a twentieth. So the estimate only has to be within FIT_STRETCH times the time
# left. Probes that fit cleanly go first; a stretch probe is started only when nothing fits cleanly,
# and the deadline, call cap and probe cap still stop the loop exactly as before.
FIT_STRETCH = 2.0
# Refill (6 Oct 2026, Luke: "ran out of anything runnable" read as doing the bare minimum). An empty
# or blocked queue with time left prints REFILL instead of STOP: go out to the first unused source in
# field-notes/REFILL-SOURCES.md, learn one thing, queue one build with `add --source refill`, then
# ask `next` again. At most REFILL_MAX a night, only with REFILL_MIN_LEFT minutes left. On by default
# since 7 Oct (the 6 Oct loop ran on a prompt without `--refill` and stopped); `--no-refill` turns it off.
REFILL_MAX = 2
REFILL_MIN_LEFT = 25
REFILL_SOURCES = ROOT + "field-notes/REFILL-SOURCES.md"
INTERACTIVE_MINUTES = 45      # default when no nightly preflight header is found
NIGHTLY_LENGTH_MIN = 90
NIGHTLY_RESERVE_MIN = 10      # kept back for the run log and the marker release
MAX_ATTEMPTS = 3
ASK_EXPIRY_DAYS = 28          # a probe blocked on Luke's hands this long after the ask is killed
LOOP_STALE_H = 3              # a loop older than this without a stop is a dead run


# ---------------------------------------------------------------- time and state helpers

def now():
    return datetime.now().astimezone()


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def parse_iso(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")


def hm(dt):
    return dt.strftime("%H:%M")


def load_state():
    try:
        with open(STATE) as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {"next_id": 1, "items": []}


def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    tmp = STATE + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(st, fh, indent=1)
        fh.write("\n")
    os.replace(tmp, STATE)


def find(st, pid):
    for it in st["items"]:
        if it["id"] == pid:
            return it
    sys.exit("no such probe: %s" % pid)


def loop_path(lp):
    return LOOP_DIR + lp["key"] + ".json"


def save_loop(lp):
    os.makedirs(LOOP_DIR, exist_ok=True)
    tmp = loop_path(lp) + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(lp, fh, indent=1)
        fh.write("\n")
    os.replace(tmp, loop_path(lp))


def current_loop():
    """The open loop, if any: newest loop file without a stop, started within LOOP_STALE_H."""
    try:
        names = sorted(n for n in os.listdir(LOOP_DIR) if re.match(r"\d{4}-\d{2}-\d{2}-\d{4}\.json$", n))
    except FileNotFoundError:
        return None
    for name in reversed(names[-2:]):
        with open(LOOP_DIR + name) as fh:
            lp = json.load(fh)
        if lp.get("stopped_at"):
            continue
        if now() - parse_iso(lp["started_at"]) > timedelta(hours=LOOP_STALE_H):
            continue
        return lp
    return None


def session_short():
    """First 8 chars of the bound unattended session id, or None in an interactive session."""
    try:
        with open(MARKER) as fh:
            sid = json.load(fh).get("session_id")
    except Exception:
        return None
    if not sid or sid == "closed":
        return None
    return str(sid)[:8]


def decisions_since(session, since):
    """(calls, denied_lines) the hook logged for this session at or after `since`."""
    if not session:
        return None, []
    days = {since.strftime("%Y-%m-%d"), now().strftime("%Y-%m-%d")}
    calls, denied = 0, []
    for day in sorted(days):
        try:
            fh = open(DECISIONS % day)
        except FileNotFoundError:
            continue
        with fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                    ts = parse_iso(rec["ts"])
                except Exception:
                    continue
                if rec.get("session") != session or ts < since:
                    continue
                calls += 1
                if rec.get("outcome") == "deny":
                    who = "child " + str(rec.get("agent_id"))[:8] + " " if rec.get("agent_id") else ""
                    denied.append("%s%s `%s`" % (who, rec.get("tool"), str(rec.get("detail", ""))[:90]))
    return calls, denied


def halted():
    return os.path.exists(HALT)


def run_log_append(lp, lines):
    os.makedirs(RUNS, exist_ok=True)
    with open(lp["run_log"], "a") as fh:
        for ln in lines:
            fh.write(ln.rstrip("\n") + "\n")


def git(args, check=True, timeout=120):
    if NO_GIT:
        return ""
    r = subprocess.run(["git", "-C", ROOT.rstrip("/")] + args, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args[:2]), (r.stderr or r.stdout).strip()[:300]))
    return r.stdout.strip()


def dash_paths():
    """The private dashboard payload, rebuilt so it rides in this commit. A dash fault never loses a verdict."""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import dash
        out = dash.build()
        return [out] if out else []
    except Exception:
        return []


def commit(paths, message):
    """Commit just these paths. Returns the short hash, or the reason nothing was committed."""
    if halted():
        return "HALT set: logged, not committed"
    if NO_GIT:
        return "git disabled (PROBE_NO_GIT=1)"
    rel = []
    for p in paths:
        if not p:
            continue
        ap = os.path.realpath(p) if p.startswith("/") else os.path.realpath(ROOT + p)
        if not ap.startswith(os.path.realpath(ROOT.rstrip("/")) + os.sep):
            continue
        if not os.path.exists(ap):
            continue
        rel.append(os.path.relpath(ap, ROOT.rstrip("/")))
    if not rel:
        return "nothing to commit"
    ignored = set(git(["check-ignore", "--"] + rel, check=False).split())
    if ignored:
        rel = [r for r in rel if r not in ignored]
    git(["add", "--"] + rel)
    if not git(["diff", "--cached", "--name-only", "--"] + rel):
        return "nothing to commit (no change in %s)" % ", ".join(rel)
    git(["commit", "-q", "-m", message, "--"] + rel)
    h = git(["rev-parse", "--short", "HEAD"])
    try:
        git(["push", "-q", "origin", "main"], timeout=90)
        return h + " pushed"
    except Exception as e:  # network trouble is not a reason to lose the verdict
        return h + " committed, push failed: %s" % str(e)[:120]
    return h


def ask_expiry(it):
    """The date a probe asked of Luke is killed if it is still waiting on him."""
    d = datetime.strptime(it["asked_at"][:10], "%Y-%m-%d") + timedelta(days=ASK_EXPIRY_DAYS)
    return d.strftime("%Y-%m-%d")


# ---------------------------------------------------------------- rendering

def cost_str(it):
    if it.get("minutes") is None:
        return "not run"
    c = "%d min" % it["minutes"]
    if it.get("calls") is not None:
        c += ", %d calls, %d denied" % (it["calls"], len(it.get("denied") or []))
    return c


def render(st):
    open_items = [i for i in st["items"] if i["status"] not in ("done", "killed")]
    done = sorted([i for i in st["items"] if i["status"] == "done"],
                  key=lambda i: (i.get("verdict_at") or "", i["id"]), reverse=True)
    killed = sorted([i for i in st["items"] if i["status"] == "killed"],
                    key=lambda i: (i.get("killed_at") or "", i["id"]), reverse=True)
    tally = {v: sum(1 for i in done if i["verdict"] == v) for v in VERDICTS}
    out = [
        "# Probes",
        "",
        "One thing I have not run before, taken to a verdict the same night. Rendered by `bin/probe.py`",
        "from `state/probes.json`; the queue is edited with `probe.py add`, never by hand. Verdicts are",
        "works, broken, blocked or not worth it; reading about a thing is not a verdict. Rules in",
        "`CHARTER.md` under Probes and The Sunday cull. Cost is minutes of the night plus the tool calls",
        "and denials the unattended hook logged during the probe (calls are not measured in an",
        "interactive session).",
        "",
        "Verdicts so far: %d works, %d broken, %d blocked, %d not worth it. Killed: %d." % (
            tally["works"], tally["broken"], tally["blocked"], tally["not-worth-it"], len(killed)),
        "",
        "## Queue (%d open)" % len(open_items),
        "",
        "| id | what | source | needs | after | attempts | est |",
        "|---|---|---|---|---|---|---|",
    ]
    for i in open_items:
        att = str(i.get("attempts", 0))
        if i.get("attempts", 0) >= MAX_ATTEMPTS:
            att += " (awaiting cull)"
        if i["status"] == "in_progress":
            att += " (in progress)"
        needs = i.get("needs") or "none"
        if i.get("asked_at"):
            needs += " (asked once, %s; killed %s if still waiting)" % (
                i.get("asked_in") or i["asked_at"], ask_expiry(i))
        out.append("| %s | %s | %s | %s | %s | %s | %s min |" % (
            i["id"], i["title"], i.get("source", ""), needs.replace("|", "/"),
            i.get("after") or "", att, i.get("est_minutes", "")))
    out += ["", "## Verdicts (%d)" % len(done), "",
            "| date | id | what | verdict | note | artefact | cost |",
            "|---|---|---|---|---|---|---|"]
    for i in done:
        arts = ", ".join("`%s`" % a for a in i.get("artefacts") or []) or "none"
        note = (i.get("note") or "").replace("|", "/").replace("\n", " ")
        out.append("| %s | %s | %s | **%s** | %s | %s | %s |" % (
            (i.get("verdict_at") or "")[:10], i["id"], i["title"], i["verdict"], note, arts, cost_str(i)))
        if i.get("denied"):
            out.append("| | | | | denied: %s | | |" % "; ".join(d.replace("|", "/") for d in i["denied"]))
    out += ["", "## Kills (%d)" % len(killed), "",
            "Published in the same format as live work. A kill can be reopened with a new probe if the",
            "reason goes away.", "",
            "| date | id | what | killed by | reason |",
            "|---|---|---|---|---|"]
    for i in killed:
        out.append("| %s | %s | %s | %s | %s |" % (
            (i.get("killed_at") or "")[:10], i["id"], i["title"].replace("|", "/"),
            "Luke's word" if i.get("killed_by") == "luke" else "the cull rule",
            (i.get("kill_reason") or "").replace("|", "/")))
    with open(REGISTER, "w") as fh:
        fh.write("\n".join(out) + "\n")


# ---------------------------------------------------------------- the loop

def budget_lines(lp):
    n = now()
    dl = parse_iso(lp["deadline"])
    left = int((dl - n).total_seconds() // 60)
    calls, _ = decisions_since(lp.get("session"), parse_iso(lp["started_at"]))
    if calls is None:
        c = "calls not measured (interactive session)"
    else:
        c = "%d of %d calls used" % (calls, lp["max_calls"])
    return left, calls, "budget: %d min left until %s, %s, %d of %d probes done" % (
        left, hm(dl), c, len(lp["probes"]), lp["max_probes"])


def stop_loop(lp, reason, st=None):
    st = st or load_state()
    lp["stopped_at"] = iso(now())
    lp["stop_reason"] = reason
    used = int((parse_iso(lp["stopped_at"]) - parse_iso(lp["started_at"])).total_seconds() // 60)
    calls, denied = decisions_since(lp.get("session"), parse_iso(lp["started_at"]))
    done = [find(st, pid) for pid in lp["probes"]]
    tally = ", ".join("%s %d" % (v, sum(1 for i in done if i["verdict"] == v)) for v in VERDICTS
                      if any(i["verdict"] == v for i in done)) or "none"
    ctext = "calls not measured" if calls is None else "%d calls, %d denied" % (calls, len(denied))
    line = "- Probe loop stopped %s: %s. %d probe(s) (%s), %d min, %s." % (
        hm(now()), reason, len(done), tally, used, ctext)
    save_loop(lp)
    run_log_append(lp, [line])
    res = commit([loop_path(lp), lp["run_log"], STATE, REGISTER] + dash_paths(),
                 "probe loop %s: %d probe(s), stopped: %s" % (lp["date"], len(done), reason[:60]))
    print("STOP: " + reason)
    print(line[2:])
    print("commit: " + res)


def cmd_start(a):
    lp = current_loop()
    if lp:
        print("a loop is already open (started %s, deadline %s); use next, or stop it first" % (
            hm(parse_iso(lp["started_at"])), hm(parse_iso(lp["deadline"]))))
        return
    n = now()
    day = n.strftime("%Y-%m-%d")
    run_log = RUNS + day + ".md"
    how = ""
    if a.until:
        h, m = [int(x) for x in a.until.split(":")]
        dl = n.replace(hour=h, minute=m, second=0, microsecond=0)
        if dl <= n:
            dl += timedelta(days=1)
        how = "--until %s" % a.until
    elif a.minutes:
        dl = n + timedelta(minutes=a.minutes)
        how = "--minutes %d" % a.minutes
    else:
        dl, how = None, ""
        for cand in (run_log, RUNS + (n - timedelta(days=1)).strftime("%Y-%m-%d") + ".md"):
            try:
                txt = open(cand).read()
            except FileNotFoundError:
                continue
            hits = re.findall(r"^## Nightly run (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})", txt, re.M)
            if hits:
                d, t = hits[-1]
                started = datetime.strptime(d + " " + t, "%Y-%m-%d %H:%M").replace(tzinfo=n.tzinfo)
                if n - started < timedelta(hours=LOOP_STALE_H):
                    dl = started + timedelta(minutes=NIGHTLY_LENGTH_MIN - NIGHTLY_RESERVE_MIN)
                    how = "nightly preflight %s plus %d min" % (t, NIGHTLY_LENGTH_MIN - NIGHTLY_RESERVE_MIN)
                    run_log = cand
                break
        if dl is None:
            dl = n + timedelta(minutes=INTERACTIVE_MINUTES)
            how = "no nightly preflight header found, interactive default %d min" % INTERACTIVE_MINUTES
    cap = n + timedelta(minutes=DEFAULT_MAX_MINUTES)
    if dl > cap:
        dl, how = cap, how + ", capped at the loop's own %d min" % DEFAULT_MAX_MINUTES
    lp = {
        "key": n.strftime("%Y-%m-%d-%H%M"), "date": day, "started_at": iso(n), "deadline": iso(dl), "deadline_how": how,
        "max_calls": a.calls, "max_probes": a.probes, "session": session_short(),
        "run_log": run_log, "probes": [], "stopped_at": None, "stop_reason": None,
    }
    # a probe left in progress by a dead session counts as a used attempt
    st = load_state()
    for it in st["items"]:
        if it["status"] == "in_progress":
            it["status"] = "open"
            it["started_at"] = None
    save_state(st)
    save_loop(lp)
    run_log_append(lp, ["- Probe loop started %s: deadline %s (%s), %d calls, %d probes, session %s." % (
        hm(n), hm(dl), how, a.calls, a.probes, lp["session"] or "interactive")])
    print("started %s, deadline %s (%s), max %d calls, max %d probes, session %s" % (
        hm(n), hm(dl), how, a.calls, a.probes, lp["session"] or "interactive, calls not measured"))
    if halted():
        print("note: HALT is set; verdicts will be logged but not committed")


def runnable(st, left_minutes):
    today = now().strftime("%Y-%m-%d")
    pool = [i for i in st["items"] if i["status"] == "open"]
    why = {"needs": [], "after": [], "cull": [], "fit": []}
    fit = []
    for i in pool:
        if i.get("attempts", 0) >= MAX_ATTEMPTS:
            why["cull"].append(i)
        elif i.get("needs"):
            why["needs"].append(i)
        elif i.get("after") and i["after"] > today:
            why["after"].append(i)
        elif int(i.get("est_minutes") or 0) > left_minutes * FIT_STRETCH:
            why["fit"].append(i)
        else:
            fit.append(i)
    # clean fits first, then stretch fits; within each, the usual source order
    fit.sort(key=lambda i: (int(i.get("est_minutes") or 0) > left_minutes,
                            SOURCE_RANK.get(i.get("source"), 9), i.get("attempts", 0), i["id"]))
    return fit, why, pool


def next_refill_source():
    """(number, source, how, build) for the first row of REFILL-SOURCES.md with an empty `used`, or None."""
    try:
        txt = open(REFILL_SOURCES).read()
    except FileNotFoundError:
        return None
    for line in txt.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or not cells[0].isdigit():
            continue
        if cells[1].startswith("~~"):
            continue
        if not cells[4]:
            return cells[:4]
    return None


def cmd_next(a):
    lp = current_loop()
    if not lp:
        print("STOP: no open loop; run `probe.py start` first")
        return
    st = load_state()
    left, calls, bline = budget_lines(lp)
    if halted():
        return stop_loop(lp, "HALT file present", st)
    if left <= 0:
        return stop_loop(lp, "deadline %s reached" % hm(parse_iso(lp["deadline"])), st)
    if left < MIN_PROBE_MINUTES:
        return stop_loop(lp, "%d min left, under the %d-minute floor for starting a probe" % (left, MIN_PROBE_MINUTES), st)
    if len(lp["probes"]) >= lp["max_probes"]:
        return stop_loop(lp, "probe cap of %d reached" % lp["max_probes"], st)
    if calls is not None and calls >= lp["max_calls"]:
        return stop_loop(lp, "call cap of %d reached (%d logged)" % (lp["max_calls"], calls), st)
    for it in st["items"]:
        if it["status"] == "in_progress":
            print("GO %s (still in progress since %s; record its verdict before asking for the next)" % (
                it["id"], hm(parse_iso(it["started_at"]))))
            print("title: " + it["title"])
            print(bline)
            return
    fit, why, pool = runnable(st, left)
    refill_on = not getattr(a, "no_refill", False)
    src = next_refill_source() if refill_on and not fit else None
    if not fit and src and left >= REFILL_MIN_LEFT and lp.get("refills", 0) < REFILL_MAX:
        lp["refills"] = lp.get("refills", 0) + 1
        save_loop(lp)
        print("REFILL %d of %d: nothing runnable in the queue and %d min left." % (lp["refills"], REFILL_MAX, left))
        print("source: #%s %s" % (src[0], src[1]))
        print("pull: %s (keyless; no git clone, no npm)" % src[2])
        print("build it suggests: %s" % src[3])
        print("do: learn one thing in under ten minutes, then queue ONE build you can finish tonight:")
        print("    python3 %sbin/probe.py add \"...\" --source refill --est 25" % ROOT)
        print("    write today's date in row %s's `used` column of %s, then run `probe.py next` again." % (src[0], REFILL_SOURCES))
        print(bline)
        return
    if not fit:
        if refill_on:
            if not src:
                refill_why = "every source in REFILL-SOURCES.md is used; add new ones"
            elif lp.get("refills", 0) >= REFILL_MAX:
                refill_why = "%d of %d refills used tonight" % (lp.get("refills", 0), REFILL_MAX)
            else:
                refill_why = "%d min left, under the %d needed for a refill" % (left, REFILL_MIN_LEFT)
        if not pool:
            return stop_loop(lp, "queue empty" + ("; no refill: " + refill_why if refill_on else ""), st)
        parts = []
        if why["needs"]:
            parts.append("%d need something I do not have (%s)" % (
                len(why["needs"]), "; ".join("%s: %s" % (i["id"], i["needs"]) for i in why["needs"])))
        if why["after"]:
            parts.append("%d wait on a date (%s)" % (
                len(why["after"]), "; ".join("%s after %s" % (i["id"], i["after"]) for i in why["after"])))
        if why["cull"]:
            parts.append("%d had three attempts and wait for the Sunday cull (%s)" % (
                len(why["cull"]), ", ".join(i["id"] for i in why["cull"])))
        if why["fit"]:
            parts.append("%d estimated over %g times the %d min left (%s)" % (
                len(why["fit"]), FIT_STRETCH, left,
                ", ".join("%s %s min" % (i["id"], i.get("est_minutes")) for i in why["fit"])))
        if refill_on:
            parts.append("no refill: " + refill_why)
        return stop_loop(lp, "nothing runnable: " + "; ".join(parts), st)
    it = fit[0]
    it["status"] = "in_progress"
    it["attempts"] = it.get("attempts", 0) + 1
    it["started_at"] = iso(now())
    save_state(st)
    print("GO " + it["id"])
    print("title: " + it["title"])
    print("source: %s, attempt %d of %d, est %s min" % (it.get("source"), it["attempts"], MAX_ATTEMPTS, it.get("est_minutes")))
    print(bline)
    if int(it.get("est_minutes") or 0) > left:
        print("stretch: estimated %s min against %d left. Go anyway (estimates run long); if the deadline %s comes first,"
              % (it.get("est_minutes"), left, hm(parse_iso(lp["deadline"]))))
        print("    record no verdict: `next` stops the loop and the next start reopens it as a used attempt.")
    print("artefact: write under %sexperiments/%s-%s/ (sandbox/ is gitignored)" % (ROOT, lp["date"], it["id"]))
    print("then: python3 %sbin/probe.py verdict %s --verdict works|broken|blocked|not-worth-it --note \"...\" --artefact PATH" % (ROOT, it["id"]))


def cmd_verdict(a):
    st = load_state()
    it = find(st, a.id)
    if it["status"] == "done":
        sys.exit("%s already has a verdict (%s on %s)" % (it["id"], it["verdict"], it.get("verdict_at")))
    lp = current_loop()
    n = now()
    ran = it["status"] == "in_progress" and it.get("started_at")
    if ran:
        started = parse_iso(it["started_at"])
        it["minutes"] = int((n - started).total_seconds() // 60)
        calls, denied = decisions_since(lp.get("session") if lp else session_short(), started)
        it["calls"], it["denied"] = calls, denied
    else:
        it["minutes"], it["calls"], it["denied"] = None, None, []
    it["status"], it["verdict"], it["verdict_at"] = "done", a.verdict, iso(n)
    it["note"] = a.note.strip()
    if it["note"] and it["note"][-1] not in ".!?":
        it["note"] += "."
    it["artefacts"] = [os.path.relpath(os.path.realpath(p), ROOT.rstrip("/")) if p.startswith("/") else p
                       for p in (a.artefact or [])]
    if a.verdict == "blocked" and a.needs:
        it["needs"] = a.needs
    save_state(st)
    render(st)
    paths = [STATE, REGISTER] + [ROOT + p for p in it["artefacts"]]
    lines = ["- Probe %s, **%s** (%s): %s%s" % (
        it["id"], it["verdict"], cost_str(it), it["note"],
        (" Artefact: " + ", ".join(it["artefacts"])) if it["artefacts"] else "")]
    if it["denied"]:
        lines.append("  Denied: " + "; ".join(it["denied"]))
    if lp:
        lp["probes"].append(it["id"])
        save_loop(lp)
        run_log_append(lp, lines)
        paths += [loop_path(lp), lp["run_log"]]
    else:
        day = n.strftime("%Y-%m-%d")
        run_log_append({"run_log": RUNS + day + ".md"}, lines)
        paths.append(RUNS + day + ".md")
    paths += dash_paths()
    res = commit(paths, "probe %s: %s, %s" % (it["id"], it["verdict"], it["title"][:70]))
    print("%s: %s (%s)" % (it["id"], it["verdict"], cost_str(it)))
    if it["denied"]:
        print("denied: " + "; ".join(it["denied"]))
    print("commit: " + res)
    if lp:
        print(budget_lines(lp)[2])


def cmd_stop(a):
    lp = current_loop()
    if not lp:
        print("no open loop")
        return
    stop_loop(lp, a.reason.strip())


def cmd_add(a):
    # Repeat guard (3 Oct 2026, after the fuel feeds ran twice): the title's own words against the
    # register. A REPEAT is refused unless --repeat-ok says why it is not one; the harvest already
    # dedupes against SEEN.md, so its adds only warn.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import seen
    verdict, report = seen.check(a.title, show=3)
    if verdict == "REPEAT":
        print("\n".join(report))
        if a.source != "harvest" and not a.repeat_ok:
            print("not added: looks like a repeat. Re-run with --repeat-ok \"why it is new\" if it is not.")
            sys.exit(1)
    st = load_state()
    pid = "P-%04d" % st["next_id"]
    st["next_id"] += 1
    st["items"].append({
        "id": pid, "title": a.title.strip(), "source": a.source, "needs": (a.needs or "").strip(),
        "after": a.after or "", "est_minutes": a.est, "added": now().strftime("%Y-%m-%d"),
        "status": "open", "attempts": 0, "started_at": None, "verdict": None, "verdict_at": None,
        "note": "", "artefacts": [], "minutes": None, "calls": None, "denied": [],
        "luke": bool(a.luke),
    })
    save_state(st)
    render(st)
    print("added %s: %s" % (pid, a.title.strip()))


def cmd_status(a):
    lp = current_loop()
    st = load_state()
    if lp:
        left, calls, bline = budget_lines(lp)
        print("loop open since %s (%s); %s" % (hm(parse_iso(lp["started_at"])), lp["deadline_how"], bline))
    else:
        print("no open loop")
    print("HALT: " + ("set" if halted() else "clear"))
    fit, why, pool = runnable(st, 10 ** 6)
    print("queue: %d open, %d runnable now, %d need something, %d wait on a date, %d await the cull" % (
        len(pool), len(fit), len(why["needs"]), len(why["after"]), len(why["cull"])))
    for i in st["items"]:
        if i["status"] == "in_progress":
            print("in progress: %s %s (since %s)" % (i["id"], i["title"], hm(parse_iso(i["started_at"]))))
    for i in fit:
        print("  next: %s [%s, %s min] %s" % (i["id"], i.get("source"), i.get("est_minutes"), i["title"]))
    for i in why["needs"]:
        print("  needs %s: %s %s" % (i["needs"], i["id"], i["title"]))
    done = [i for i in st["items"] if i["status"] == "done"]
    print("verdicts: %d" % len(done))


def kill(it, by, reason, when=None):
    it["status"] = "killed"
    it["killed_at"] = iso(when or now())
    it["killed_by"] = by
    it["kill_reason"] = reason.strip()
    it["started_at"] = None


def cmd_kill(a):
    st = load_state()
    it = find(st, a.id)
    if it["status"] in ("done", "killed"):
        sys.exit("%s is already %s" % (it["id"], it["status"]))
    kill(it, a.by, a.reason)
    save_state(st)
    render(st)
    print("%s killed (%s): %s" % (it["id"], a.by, it["kill_reason"]))


def cmd_ask(a):
    """Record that this probe's ask for Luke's hands appeared in a Field Notes. Once only."""
    st = load_state()
    it = find(st, a.id)
    if it.get("asked_at"):
        sys.exit("%s was already asked in %s; an ask is made once and never chased" % (
            it["id"], it.get("asked_in") or it["asked_at"]))
    it["luke"] = True
    it["asked_at"] = a.date or now().strftime("%Y-%m-%d")
    it["asked_in"] = a.week
    save_state(st)
    render(st)
    print("%s asked in %s; killed %s if still waiting" % (it["id"], a.week, ask_expiry(it)))


def cmd_asks(a):
    """Open probes that need Luke's hands and have never been asked: the only asks the weekly may make."""
    st = load_state()
    fresh = [i for i in st["items"] if i["status"] == "open" and i.get("luke") and not i.get("asked_at")]
    if not fresh:
        print("no new asks")
    for i in fresh:
        print("%s: %s (needs %s)" % (i["id"], i["title"], i.get("needs") or "Luke"))


def cmd_cull(a):
    """The Sunday cull, as far as the probe register goes. Prints; writes only with --apply."""
    st = load_state()
    today = now().strftime("%Y-%m-%d")
    kills = []
    for i in st["items"]:
        if i["status"] not in ("open", "in_progress"):
            continue
        if i.get("attempts", 0) >= MAX_ATTEMPTS:
            kills.append((i, "could not make it run: %d attempts without a verdict" % i["attempts"]))
        elif i.get("asked_at") and ask_expiry(i) <= today:
            kills.append((i, "blocked on Luke's hands %d days after the ask in %s; never chased, reopen if he acts" % (
                ASK_EXPIRY_DAYS, i.get("asked_in") or i["asked_at"])))
    if not kills:
        print("cull: nothing to kill by rule")
    for i, why in kills:
        print("%s %s: %s" % ("KILL" if a.apply else "would kill", i["id"], why))
        if a.apply:
            kill(i, "rule", why)
    if a.apply and kills:
        save_state(st)
        render(st)


def cmd_queue(a):
    st = load_state()
    for i in st["items"]:
        if i["status"] not in ("done", "killed"):
            print("%s [%s, %s min, attempts %d, needs %s] %s" % (
                i["id"], i.get("source"), i.get("est_minutes"), i.get("attempts", 0), i.get("needs") or "none", i["title"]))


def cmd_render(a):
    render(load_state())
    print("rendered " + REGISTER)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("--minutes", type=int)
    s.add_argument("--until")
    s.add_argument("--calls", type=int, default=DEFAULT_MAX_CALLS)
    s.add_argument("--probes", type=int, default=DEFAULT_MAX_PROBES)
    s.set_defaults(fn=cmd_start)
    s = sub.add_parser("next")
    s.add_argument("--refill", action="store_true", help="kept for old prompts; refill is now the default")
    s.add_argument("--no-refill", action="store_true", help="on an empty or blocked queue, STOP instead of REFILL")
    s.set_defaults(fn=cmd_next)
    s = sub.add_parser("verdict")
    s.add_argument("id")
    s.add_argument("--verdict", required=True, choices=VERDICTS)
    s.add_argument("--note", required=True)
    s.add_argument("--artefact", action="append")
    s.add_argument("--needs", help="for blocked: what it is blocked on")
    s.set_defaults(fn=cmd_verdict)
    s = sub.add_parser("stop")
    s.add_argument("--reason", required=True)
    s.set_defaults(fn=cmd_stop)
    s = sub.add_parser("add")
    s.add_argument("title")
    s.add_argument("--source", default="backlog", choices=sorted(SOURCE_RANK))
    s.add_argument("--needs", default="")
    s.add_argument("--after", default="")
    s.add_argument("--est", type=int, default=20)
    s.add_argument("--luke", action="store_true", help="the need is Luke's hands: asked once, expires in 28 days")
    s.add_argument("--repeat-ok", default="", help="why a title the repeat guard flags is new after all")
    s.set_defaults(fn=cmd_add)
    s = sub.add_parser("kill")
    s.add_argument("id")
    s.add_argument("--by", required=True, choices=("rule", "luke"))
    s.add_argument("--reason", required=True)
    s.set_defaults(fn=cmd_kill)
    s = sub.add_parser("ask")
    s.add_argument("id")
    s.add_argument("--week", required=True, help="the Field Notes week the ask appeared in, YYYY-WNN")
    s.add_argument("--date", help="YYYY-MM-DD, default today")
    s.set_defaults(fn=cmd_ask)
    s = sub.add_parser("asks")
    s.set_defaults(fn=cmd_asks)
    s = sub.add_parser("cull")
    s.add_argument("--apply", action="store_true")
    s.set_defaults(fn=cmd_cull)
    for name, fn in (("status", cmd_status), ("queue", cmd_queue), ("render", cmd_render)):
        sub.add_parser(name).set_defaults(fn=fn)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
