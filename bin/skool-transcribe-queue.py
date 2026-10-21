#!/usr/bin/env python3
"""Slow, unattended transcription of Skool course videos, run by launchd (com.proteus.skool-transcribe).

    python3 /Users/triton/PROTEUS/bin/skool-transcribe-queue.py run      # one pass (launchd, every 20 min)
    python3 /Users/triton/PROTEUS/bin/skool-transcribe-queue.py status
    python3 /Users/triton/PROTEUS/bin/skool-transcribe-queue.py add LIST.tsv   # slug<TAB>url rows

Queue: state/skool-transcribe/queue.tsv (slug, url). Results: field-notes/skool/transcripts/<slug>.txt
(gitignored, course text). Log: state/skool-transcribe/log.jsonl, one line per attempt.

Built 19 Oct 2026 on Luke's ask ("not mad at how long it takes, I just want to know it's getting done").
Rules, from the 15 and 19 Oct blocks:
- YouTube captions are never requested: about 10 caption fetches 20 s apart got the Mac IP-blocked twice.
  YouTube goes straight to audio download (yt-dlp with node as its JS runtime) and local whisper.
- One video at a time, a pause after every download, and no new video started after 15 minutes of a pass.
- Two YouTube failures in a row end the pass and set a 6-hour cool-off (one 403 is often passing;
  skool_transcript.py already retries each download three times).
- Two failures and a row is parked, not retried for ever. HALT stops everything.
Skool pulls themselves need the signed-in browser pane, so they are not here.
"""
import fcntl, json, os, subprocess, sys, time
from datetime import datetime

ROOT = "/Users/triton/PROTEUS/"
DIR = ROOT + "state/skool-transcribe/"
QUEUE, LOG, COOL = DIR + "queue.tsv", DIR + "log.jsonl", DIR + "cooloff-until"
OUT = ROOT + "field-notes/skool/transcripts/"
PY = ROOT + "sandbox/skool-venv/bin/python"
TOOL = ROOT + "sandbox/skool_transcript.py"
PASS_SECONDS, PAUSE, MAX_TRIES, COOL_HOURS = 15 * 60, 90, 2, 6


def rows():
    if not os.path.exists(QUEUE):
        return []
    out = []
    for line in open(QUEUE):
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 2 and parts[0] and not parts[0].startswith("#"):
            out.append((parts[0], parts[1]))
    return out


def attempts():
    """Failed tries per slug. A "blocked" result (a bot challenge nothing here can pass, 21 Oct 2026) counts
    as MAX_TRIES at once, so the row is parked after one go instead of poking the challenge again."""
    n = {}
    if os.path.exists(LOG):
        for line in open(LOG):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("result") == "blocked":
                n[r["slug"]] = MAX_TRIES
            elif r.get("result") != "ok":
                n[r["slug"]] = n.get(r["slug"], 0) + 1
    return n


def log(**kw):
    kw["at"] = datetime.now().isoformat(timespec="seconds")
    with open(LOG, "a") as fh:
        fh.write(json.dumps(kw) + "\n")


def pending():
    tries = attempts()
    todo, parked = [], []
    for slug, url in rows():
        if os.path.exists(OUT + slug + ".txt") and os.path.getsize(OUT + slug + ".txt") > 0:
            continue
        (parked if tries.get(slug, 0) >= MAX_TRIES else todo).append((slug, url))
    return todo, parked


def cmd_run():
    os.makedirs(DIR, exist_ok=True)
    if os.path.exists(ROOT + "HALT"):
        print("HALT set"); return
    lock = open(DIR + "lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("another pass is running"); return
    if os.path.exists(COOL) and time.time() < float(open(COOL).read() or 0):
        print("cooling off until", datetime.fromtimestamp(float(open(COOL).read())).strftime("%H:%M")); return
    todo, _ = pending()
    start = time.time()
    yt_fails = 0
    for slug, url in todo:
        if time.time() - start > PASS_SECONDS or os.path.exists(ROOT + "HALT"):
            break
        yt = "youtu" in url
        args = [PY, TOOL, url, "--out", OUT + slug + ".txt"] + (["--force-whisper"] if yt else [])
        t0 = time.time()
        p = subprocess.run(args, capture_output=True, text=True, stdin=subprocess.DEVNULL,
                           env=dict(os.environ, PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin"))
        secs = int(time.time() - t0)
        if p.returncode == 0:
            how = p.stdout.strip().rsplit("via ", 1)[-1][:-1]
            log(slug=slug, url=url, result="ok", how=how, secs=secs)
            yt_fails = 0
            print("ok", slug, secs, "s", how)
        else:
            err = (p.stderr or p.stdout).strip().splitlines()[-1:] or ["?"]
            blocked = "Turnstile" in (p.stderr or "") or "HTTP Error 401" in err[0]
            log(slug=slug, url=url, result="blocked" if blocked else "fail", err=err[0][:300], secs=secs)
            print("BLOCKED" if blocked else "FAIL", slug, err[0][:200])
            yt_fails = yt_fails + 1 if yt else yt_fails
            if yt_fails >= 2:
                open(COOL, "w").write(str(time.time() + COOL_HOURS * 3600))
                print("YouTube refused twice in a row; cooling off", COOL_HOURS, "h"); break
        time.sleep(PAUSE if yt else 5)


def cmd_status():
    todo, parked = pending()
    done = sum(1 for s, _ in rows() if os.path.exists(OUT + s + ".txt"))
    print("queue %d: done %d, to do %d, parked %d" % (len(rows()), done, len(todo), len(parked)))
    if os.path.exists(COOL) and time.time() < float(open(COOL).read() or 0):
        print("cooling off until", datetime.fromtimestamp(float(open(COOL).read())).strftime("%d %b %H:%M"))
    blocked = {r["slug"] for r in (json.loads(l) for l in open(LOG)) if r.get("result") == "blocked"} if os.path.exists(LOG) else set()
    for s, u in parked:
        print("parked (Vimeo bot challenge, needs an interactive browser or another day):" if s in blocked else "parked:", s, u)


def vkey(u):
    """One key per video, so the same YouTube/Loom/Vimeo link written two ways is queued once."""
    import re
    for pat, tag in ((r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", "yt"),
                     (r"loom\.com/(?:share|embed)/([0-9a-f]{32})", "loom"), (r"vimeo\.com/(?:video/)?(\d+)", "vimeo")):
        m = re.search(pat, u)
        if m:
            return tag + ":" + m.group(1)
    return u.split("?")[0]


def cmd_add(path):
    os.makedirs(DIR, exist_ok=True)
    have = {s for s, _ in rows()}
    urls = {vkey(u) for _, u in rows()}
    added = 0
    with open(QUEUE, "a") as fh:
        for line in open(path):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2 or parts[0] in have or vkey(parts[1]) in urls:
                continue
            fh.write("%s\t%s\n" % (parts[0], parts[1])); have.add(parts[0]); urls.add(vkey(parts[1])); added += 1
    print("added %d from %s" % (added, path))


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "status"
    if c == "add":
        cmd_add(sys.argv[2])
    elif c == "run":
        cmd_run()
    else:
        cmd_status()
