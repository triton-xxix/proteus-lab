#!/usr/bin/env python3
"""Rebuild USAGE.md from the Claude Code session transcripts for this folder. Never typed by hand.

    python3 /Users/triton/PROTEUS/bin/usage.py          # print the table
    python3 /Users/triton/PROTEUS/bin/usage.py --write  # rewrite USAGE.md

The charter (What Proteus costs in Claude) asks for one row per session: date, task, model, output
tokens, cache reads, cache writes, uncached input, wall time, with monthly totals at the top and
Luke's own sessions labelled apart from the scheduled ones.

How a row is found. A transcript is one JSONL file per session under
~/.claude/projects/-Users-triton-PROTEUS/. A session can hold more than one run: the 26 Sep
nightly was resumed interactively the next morning. So a session is cut into segments at every
real user prompt, and each segment is labelled by that prompt: a prompt carrying
`<scheduled-task name="proteus-nightly">` is the nightly, `proteus-weekly` the weekly, anything
else is interactive (Luke's). Sub-agent transcripts under <session>/subagents/ are their own rows,
labelled with the parent segment's task and "child".

Tokens. One API response can be written as several transcript records (one per content block)
that repeat the same usage, so usage is counted once per requestId. Wall time is active time: the
gaps between records, each capped at 10 minutes, so a session left open overnight does not count
the night.

Unit is tokens. No pounds figure: Luke pays a subscription, and a list-price estimate is only worth
publishing once the prices are checked against the current price list, not remembered.
"""
import glob
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta

ROOT = "/Users/triton/PROTEUS/"
TRANSCRIPTS = os.path.expanduser("~/.claude/projects/-Users-triton-PROTEUS/")
GAP_CAP = timedelta(minutes=10)
TASK_RE = re.compile(r'<scheduled-task name="proteus-([a-z-]+)"')
FIELDS = ("output", "cache_read", "cache_write", "input")


def parse_ts(s):
    return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")


def prompt_text(rec):
    """The text of a real user prompt, or None for tool results and system-injected records."""
    if rec.get("type") != "user" or rec.get("isMeta") or rec.get("isSidechain"):
        return None
    c = (rec.get("message") or {}).get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            return None
        texts = [b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text"]
        return "\n".join(texts) if texts else None
    return None


def task_of(text):
    m = TASK_RE.search(text or "")
    return m.group(1) if m else "interactive"


def short_model(m):
    return (m or "unknown").replace("claude-", "")


def read_records(path):
    out = []
    try:
        fh = open(path)
    except OSError:
        return out
    with fh:
        for line in fh:
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
    return out


def new_seg(session, task, child=None):
    return {"session": session, "task": task, "child": child, "start": None, "last": None,
            "active": timedelta(0), "models": defaultdict(int), "tok": dict.fromkeys(FIELDS, 0),
            "seen": {}}


def add_record(seg, rec):
    ts = rec.get("timestamp")
    if ts:
        t = parse_ts(ts)
        if seg["start"] is None:
            seg["start"] = t
        elif seg["last"] is not None and t > seg["last"]:
            seg["active"] += min(t - seg["last"], GAP_CAP)
        seg["last"] = max(seg["last"] or t, t)
    if rec.get("type") != "assistant":
        return
    msg = rec.get("message") or {}
    u = msg.get("usage")
    if not u:
        return
    if msg.get("model") == "<synthetic>":  # client-made placeholder messages, not API calls
        return
    rid = rec.get("requestId") or msg.get("id") or rec.get("uuid")
    old = seg["seen"].get(rid)
    # a response streamed into several records carries growing output counts: keep the largest
    if old is None or (u.get("output_tokens") or 0) > (old[1].get("output_tokens") or 0):
        seg["seen"][rid] = (short_model(msg.get("model")), u)


def settle(seg):
    """Sum the one usage kept per response into the segment's totals."""
    for model, u in seg["seen"].values():
        seg["tok"]["output"] += u.get("output_tokens") or 0
        seg["tok"]["cache_read"] += u.get("cache_read_input_tokens") or 0
        seg["tok"]["cache_write"] += u.get("cache_creation_input_tokens") or 0
        seg["tok"]["input"] += u.get("input_tokens") or 0
        seg["models"][model] += u.get("output_tokens") or 0
    return seg


def segments_for(path):
    session = os.path.basename(path)[:-6]
    recs = read_records(path)
    segs, cur = [], None
    for rec in recs:
        text = prompt_text(rec)
        if text is not None:
            if cur is None or task_of(text) != cur["task"] or cur["task"] != "interactive":
                cur = new_seg(session, task_of(text))
                segs.append(cur)
        if cur is None:
            cur = new_seg(session, "interactive")
            segs.append(cur)
        add_record(cur, rec)
    segs = [settle(s) for s in segs]
    segs = [s for s in segs if s["start"] and sum(s["tok"].values())]
    # children: one row each, labelled with the segment that was running when they started
    for cpath in sorted(glob.glob(os.path.join(TRANSCRIPTS, session, "subagents", "*.jsonl"))):
        crecs = read_records(cpath)
        child = new_seg(session, "interactive", child=os.path.basename(cpath)[6:-6][:8])
        for rec in crecs:
            add_record(child, rec)
        settle(child)
        if not child["start"]:
            continue
        parent = [s for s in segs if s["start"] <= child["start"]]
        child["task"] = parent[-1]["task"] if parent else (segs[0]["task"] if segs else "interactive")
        segs.append(child)
    return segs


def all_segments():
    segs = []
    for path in sorted(glob.glob(TRANSCRIPTS + "*.jsonl")):
        segs += segments_for(path)
    segs.sort(key=lambda s: (s["start"], s["child"] or ""))
    return segs


def k(n):
    if n >= 1_000_000:
        return "%.2fM" % (n / 1e6)
    if n >= 1000:
        return "%.1fk" % (n / 1e3)
    return str(n)


def label(s):
    t = s["task"] if s["task"] == "interactive" else s["task"]
    t = {"interactive": "interactive (Luke)"}.get(t, t)
    return t + (", child " + s["child"] if s["child"] else "")


def model_of(s):
    ms = sorted(s["models"].items(), key=lambda kv: -kv[1])
    return ", ".join(m for m, _ in ms) or "unknown"


def render(segs):
    months = OrderedDict()
    weeks = defaultdict(lambda: defaultdict(int))
    for s in segs:
        m = s["start"].strftime("%Y-%m")
        kind = "interactive" if s["task"] == "interactive" else "scheduled"
        months.setdefault(m, {"scheduled": dict.fromkeys(FIELDS, 0), "interactive": dict.fromkeys(FIELDS, 0)})
        for f in FIELDS:
            months[m][kind][f] += s["tok"][f]
        if kind == "scheduled":
            iy, iw, _ = s["start"].isocalendar()
            weeks["%d-W%02d" % (iy, iw)]["output"] += s["tok"]["output"]
            weeks["%d-W%02d" % (iy, iw)]["runs"] += 0 if s["child"] else 1
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [
        "# Usage",
        "",
        "What Proteus costs in Claude, in tokens, rebuilt every Sunday by `bin/usage.py` from the",
        "session transcripts on this Mac. Never typed by hand.",
        "",
        "What it cannot see: sessions on other machines or in other folders, and anything before the",
        "transcripts on disk. Interactive sessions are labelled \"interactive (Luke)\" and kept apart",
        "from the scheduled runs, so the nightly is not blamed for them. A session resumed later is",
        "split at each prompt, so one transcript can be two rows. Wall time is active time, gaps",
        "capped at 10 minutes. Times and weeks are UTC. No pounds figure yet: it waits until list",
        "prices are checked, not remembered.",
        "",
        "Rebuilt %s." % now,
        "",
        "## By month",
        "",
        "| Month | Who | Output | Cache reads | Cache writes | Uncached input |",
        "|---|---|---|---|---|---|",
    ]
    for m, v in months.items():
        for kind in ("scheduled", "interactive"):
            t = v[kind]
            out.append("| %s | %s | %s | %s | %s | %s |" % (
                m, "scheduled runs" if kind == "scheduled" else "Luke's sessions",
                k(t["output"]), k(t["cache_read"]), k(t["cache_write"]), k(t["input"])))
    out += ["", "## Scheduled output by ISO week",
            "",
            "The charter's alarm: a week more than double the trailing four-week average is named in",
            "Field Notes with the step that caused it.",
            "",
            "| Week | Runs | Output | Trailing 4-week average | Over double? |", "|---|---|---|---|---|"]
    wk = sorted(weeks)
    for idx, w in enumerate(wk):
        prev = [weeks[x]["output"] for x in wk[max(0, idx - 4):idx]]
        avg = sum(prev) / len(prev) if prev else None
        flag = "n/a" if avg is None else ("YES" if weeks[w]["output"] > 2 * avg else "no")
        out.append("| %s | %d | %s | %s | %s |" % (w, weeks[w]["runs"], k(weeks[w]["output"]),
                                                  "n/a" if avg is None else k(int(avg)), flag))
    out += ["", "## By session", "",
            "| Start (UTC) | Task | Model | Output | Cache reads | Cache writes | Uncached input | Active time | Session |",
            "|---|---|---|---|---|---|---|---|---|"]
    for s in segs:
        mins = int(s["active"].total_seconds() // 60)
        out.append("| %s | %s | %s | %s | %s | %s | %s | %d min | %s |" % (
            s["start"].strftime("%Y-%m-%d %H:%M"), label(s), model_of(s), k(s["tok"]["output"]),
            k(s["tok"]["cache_read"]), k(s["tok"]["cache_write"]), k(s["tok"]["input"]), mins,
            s["session"][:8]))
    return "\n".join(out) + "\n"


def main():
    text = render(all_segments())
    if "--write" in sys.argv:
        open(ROOT + "USAGE.md", "w").write(text)
        print("wrote USAGE.md")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
