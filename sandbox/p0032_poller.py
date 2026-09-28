"""P-0032: pump.fun poller v2. Six pages of GeckoTerminal new_pools every two minutes for 24 hours,
so launches are not missed (P-0014 pulled two pages every five minutes and the feed rolled over
between polls on 129 of 284 polls), plus a trimmed attribute snapshot of every pump-fun launch and
pumpswap pool at first sight and again at the first poll where it is at least five minutes old.

Run by launchd every 120 s (label com.proteus.p0032, plist in the experiment folder, loaded from
there, nothing written to ~/Library). Stops itself after 24 hours from the first poll, and on HALT.
Writes only under its experiment folder. Usage: python3 p0032_poller.py [poll|summary|load|unload]
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone

OUT = "/Users/triton/PROTEUS/experiments/2026-09-28-P-0032"
POOLS = os.path.join(OUT, "pools.jsonl")        # one line per pool first seen, all dexes
SNAPS = os.path.join(OUT, "snapshots.jsonl")    # attribute snapshots, pump-fun and pumpswap only
POLLS = os.path.join(OUT, "polls.jsonl")
START = os.path.join(OUT, "START")
DONE = os.path.join(OUT, "DONE")
PLIST = os.path.join(OUT, "com.proteus.p0032.plist")
LABEL = "com.proteus.p0032"
HOURS = 24
PAGES = 6            # 10 drew 429 from page 6 on the first poll; 100 rows already covered 10 minutes
PAGE_GAP = 4.0       # seconds between pages; one retry after RETRY_GAP on a 429
RETRY_GAP = 8.0
GT = "https://api.geckoterminal.com/api/v2/networks/solana/new_pools?page=%d"
SNAP_DEX = {"pump-fun", "pumpswap"}
SNAP_AT_MIN = 5.0


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def domain():
    return "gui/%d" % os.getuid()


def load():
    r = subprocess.run(["/bin/launchctl", "bootstrap", domain(), PLIST], capture_output=True, text=True)
    print("bootstrap rc", r.returncode, (r.stdout or r.stderr).strip()[:200])


def unload():
    subprocess.run(["/bin/launchctl", "bootout", domain() + "/" + LABEL], capture_output=True)


def num(x):
    try:
        return float(x) if x is not None else None
    except (TypeError, ValueError):
        return None


def trim(a):
    tx = a.get("transactions") or {}
    pc = a.get("price_change_percentage") or {}
    vol = a.get("volume_usd") or {}
    m5 = tx.get("m5") or {}
    h1 = tx.get("h1") or {}
    return {"price": num(a.get("base_token_price_usd")), "fdv": num(a.get("fdv_usd")), "mcap": num(a.get("market_cap_usd")),
            "reserve": num(a.get("reserve_in_usd")), "vol_m5": num(vol.get("m5")), "vol_h1": num(vol.get("h1")),
            "buys_m5": m5.get("buys"), "sells_m5": m5.get("sells"), "buyers_m5": m5.get("buyers"),
            "sellers_m5": m5.get("sellers"), "buys_h1": h1.get("buys"), "sells_h1": h1.get("sells"),
            "chg_m5": num(pc.get("m5")), "chg_h1": num(pc.get("h1"))}


def state():
    """Seen ids and, for snapshot dexes, which pools still need their 5-minute snapshot."""
    seen, pending = set(), {}
    if os.path.exists(POOLS):
        for line in open(POOLS):
            try:
                p = json.loads(line)
            except Exception:
                continue
            seen.add(p["id"])
            if p["dex"] in SNAP_DEX and p.get("created"):
                pending[p["id"]] = p["created"]
    if os.path.exists(SNAPS):
        for line in open(SNAPS):
            try:
                s = json.loads(line)
            except Exception:
                continue
            if s.get("kind") == "5min":
                pending.pop(s["id"], None)
    return seen, pending


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
    seen, pending = state()
    got, new, snaps, errors, saturated = 0, 0, 0, [], 0
    t0 = time.time()
    for page in range(1, PAGES + 1):
        data = None
        for attempt in (1, 2):
            try:
                req = urllib.request.Request(GT % page, headers={"Accept": "application/json",
                                                                 "User-Agent": "proteus-p0032"})
                data = json.load(urllib.request.urlopen(req, timeout=30))["data"]
                break
            except Exception as e:
                errors.append("page %d try %d: %s" % (page, attempt, str(e)[:60]))
                time.sleep(RETRY_GAP)
        if data is None:
            continue
        page_new = 0
        stamp = now()
        with open(POOLS, "a") as fp, open(SNAPS, "a") as fs:
            for p in data:
                got += 1
                pid = p["id"]
                a = p["attributes"]
                dex = p["relationships"]["dex"]["data"]["id"]
                created = a.get("pool_created_at")
                if pid not in seen:
                    seen.add(pid)
                    new += 1
                    page_new += 1
                    fp.write(json.dumps({"id": pid, "dex": dex, "name": a.get("name"), "created": created,
                                         "seen": stamp}) + "\n")
                    if dex in SNAP_DEX and created:
                        age = (ts(stamp) - ts(created)).total_seconds() / 60
                        fs.write(json.dumps({"id": pid, "kind": "first", "age_min": round(age, 2), "seen": stamp,
                                             **trim(a)}) + "\n")
                        snaps += 1
                        if age >= SNAP_AT_MIN:
                            fs.write(json.dumps({"id": pid, "kind": "5min", "age_min": round(age, 2), "seen": stamp,
                                                 **trim(a)}) + "\n")
                            snaps += 1
                        else:
                            pending[pid] = created
                elif pid in pending:
                    age = (ts(stamp) - ts(pending[pid])).total_seconds() / 60
                    if age >= SNAP_AT_MIN:
                        fs.write(json.dumps({"id": pid, "kind": "5min", "age_min": round(age, 2), "seen": stamp,
                                             **trim(a)}) + "\n")
                        snaps += 1
                        pending.pop(pid, None)
        if page == PAGES and page_new == len(data) and data:
            saturated = 1
        time.sleep(PAGE_GAP)
    with open(POLLS, "a") as f:
        f.write(json.dumps({"ts": now(), "rows": got, "new": new, "snaps": snaps, "pending": len(pending),
                            "last_page_all_new": saturated, "secs": round(time.time() - t0, 1),
                            "errors": errors}) + "\n")


def summary():
    pools = [json.loads(l) for l in open(POOLS)] if os.path.exists(POOLS) else []
    polls = [json.loads(l) for l in open(POLLS)] if os.path.exists(POLLS) else []
    snaps = [json.loads(l) for l in open(SNAPS)] if os.path.exists(SNAPS) else []
    print(json.dumps({"polls": len(polls), "polls_with_errors": sum(1 for p in polls if p["errors"]),
                      "polls_last_page_all_new": sum(p.get("last_page_all_new", 0) for p in polls),
                      "pools": len(pools), "by_dex": Counter(p["dex"] for p in pools).most_common(8),
                      "snapshots": Counter(s["kind"] for s in snaps).most_common(),
                      "first": polls[0]["ts"] if polls else None, "last": polls[-1]["ts"] if polls else None,
                      "done": os.path.exists(DONE)}, indent=1))


if __name__ == "__main__":
    {"poll": poll, "summary": summary, "load": load, "unload": unload}[sys.argv[1] if len(sys.argv) > 1 else "poll"]()
