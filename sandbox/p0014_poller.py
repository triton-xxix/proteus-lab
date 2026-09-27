"""P-0014: pump.fun graduation rate over a full day.

Run by launchd every 5 minutes (label com.proteus.p0014, plist in the experiment folder, loaded
from there, nothing written to ~/Library). Each run pulls GeckoTerminal new_pools pages 1 and 2 for
Solana and appends every pool not seen before to pools.jsonl, plus one line per poll to polls.jsonl.
After 24 hours from the first poll it writes DONE and unloads its own launchd job.
Usage: python3 p0014_poller.py [poll|summary]
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone

OUT = "/Users/triton/PROTEUS/experiments/2026-09-27-P-0014"
POOLS = os.path.join(OUT, "pools.jsonl")
POLLS = os.path.join(OUT, "polls.jsonl")
START = os.path.join(OUT, "START")
DONE = os.path.join(OUT, "DONE")
LABEL = "com.proteus.p0014"
HOURS = 24
GT = "https://api.geckoterminal.com/api/v2/networks/solana/new_pools?page=%d"


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def unload():
    subprocess.run(["/bin/launchctl", "bootout", "gui/%d/%s" % (os.getuid(), LABEL)], capture_output=True)


def seen_ids():
    ids = set()
    if os.path.exists(POOLS):
        for line in open(POOLS):
            try:
                ids.add(json.loads(line)["id"])
            except Exception:
                pass
    return ids


def poll():
    os.makedirs(OUT, exist_ok=True)
    if os.path.exists(DONE) or os.path.exists("/Users/triton/PROTEUS/HALT"):
        unload()
        return
    if not os.path.exists(START):
        open(START, "w").write(str(time.time()))
    if time.time() - float(open(START).read()) > HOURS * 3600:
        open(DONE, "w").write(now())
        unload()
        return
    seen = seen_ids()
    got, new, errors = 0, 0, []
    for page in (1, 2):
        try:
            req = urllib.request.Request(GT % page, headers={"Accept": "application/json",
                                                             "User-Agent": "proteus-p0014"})
            data = json.load(urllib.request.urlopen(req, timeout=30))["data"]
        except Exception as e:
            errors.append("page %d: %s" % (page, e))
            continue
        with open(POOLS, "a") as f:
            for p in data:
                got += 1
                if p["id"] in seen:
                    continue
                seen.add(p["id"])
                new += 1
                a = p["attributes"]
                f.write(json.dumps({"id": p["id"], "dex": p["relationships"]["dex"]["data"]["id"],
                                    "name": a.get("name"), "created": a.get("pool_created_at"),
                                    "seen": now()}) + "\n")
        time.sleep(2)
    with open(POLLS, "a") as f:
        f.write(json.dumps({"ts": now(), "rows": got, "new": new, "errors": errors}) + "\n")


def summary():
    pools = [json.loads(l) for l in open(POOLS)] if os.path.exists(POOLS) else []
    polls = [json.loads(l) for l in open(POLLS)] if os.path.exists(POLLS) else []
    dex = Counter(p["dex"] for p in pools)
    print(json.dumps({"polls": len(polls), "polls_with_errors": sum(1 for p in polls if p["errors"]),
                      "pools": len(pools), "by_dex": dex.most_common(),
                      "first": polls[0]["ts"] if polls else None, "last": polls[-1]["ts"] if polls else None,
                      "done": os.path.exists(DONE)}, indent=1))


if __name__ == "__main__":
    {"poll": poll, "summary": summary}[sys.argv[1] if len(sys.argv) > 1 else "poll"]()
