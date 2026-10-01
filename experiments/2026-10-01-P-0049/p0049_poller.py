"""P-0049: pump.fun poller v3. Same feed as P-0032 (six pages of GeckoTerminal new_pools every two
minutes for 24 hours), with the two fixes P-0033 asked for:

1. Every pool row keeps its base token address, so a graduation is a pumpswap pool whose base token
   is a pump-fun launch seen earlier, not a name match.
2. The five-minute snapshot of each pump-fun launch is taken by a per-pool lookup
   (pools/multi, 30 addresses a call), not by hoping the pool is still on page six.
   Graduates found in the feed get the same lookup on their pump-fun pool at minute five, so the
   minute-five profile exists for every launch the lookup reaches.

Run by launchd every 120 s (label com.proteus.p0049, plist in this folder, loaded from here,
nothing written to ~/Library). Stops itself 24 hours after the first poll and on HALT, and unloads
its own job. Writes only under this folder. Usage: python3 p0049_poller.py [poll|summary|load|unload]
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone

OUT = "/Users/triton/PROTEUS/experiments/2026-10-01-P-0049"
POOLS = os.path.join(OUT, "pools.jsonl")        # one line per pool first seen, all dexes, with base token
SNAPS = os.path.join(OUT, "snapshots.jsonl")    # 5-minute snapshots of pump-fun launches, by lookup
POLLS = os.path.join(OUT, "polls.jsonl")
START = os.path.join(OUT, "START")
DONE = os.path.join(OUT, "DONE")
PLIST = os.path.join(OUT, "com.proteus.p0049.plist")
LABEL = "com.proteus.p0049"
HOURS = 24
PAGES = 6
PAGE_GAP = 4.0
RETRY_GAP = 8.0
GT = "https://api.geckoterminal.com/api/v2/networks/solana/new_pools?page=%d"
MULTI = "https://api.geckoterminal.com/api/v2/networks/solana/pools/multi/%s"
SNAP_AT_MIN = 5.0
MISS_AFTER_MIN = 20.0   # a launch not looked up by minute 20 is logged as missed, not snapshotted late
MULTI_MAX = 30
MULTI_CALLS_MAX = 4     # per poll; 6 pages plus 4 lookups stays inside the free tier's 30 a minute


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


def fetch(url, errors, label):
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "proteus-p0049"})
            return json.load(urllib.request.urlopen(req, timeout=30))["data"]
        except Exception as e:
            errors.append("%s try %d: %s" % (label, attempt, str(e)[:60]))
            time.sleep(RETRY_GAP)
    return None


def state():
    """Seen pool ids, and pump-fun launches still owed a 5-minute snapshot (address -> created)."""
    seen, pending = set(), {}
    if os.path.exists(POOLS):
        for line in open(POOLS):
            try:
                p = json.loads(line)
            except Exception:
                continue
            seen.add(p["id"])
            if p["dex"] == "pump-fun" and p.get("created"):
                pending[p["address"]] = p["created"]
    if os.path.exists(SNAPS):
        for line in open(SNAPS):
            try:
                s = json.loads(line)
            except Exception:
                continue
            pending.pop(s["address"], None)
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
    got, new, errors, saturated, t0 = 0, 0, [], 0, time.time()
    for page in range(1, PAGES + 1):
        data = fetch(GT % page, errors, "page %d" % page)
        if data is None:
            continue
        page_new, stamp = 0, now()
        with open(POOLS, "a") as fp:
            for p in data:
                got += 1
                if p["id"] in seen:
                    continue
                a, rel = p["attributes"], p["relationships"]
                row = {"id": p["id"], "address": a.get("address"), "dex": rel["dex"]["data"]["id"],
                       "base": rel["base_token"]["data"]["id"], "quote": rel["quote_token"]["data"]["id"],
                       "name": a.get("name"), "created": a.get("pool_created_at"), "seen": stamp}
                fp.write(json.dumps(row) + "\n")
                seen.add(p["id"])
                new += 1
                page_new += 1
                if row["dex"] == "pump-fun" and row["created"]:
                    pending[row["address"]] = row["created"]
        if page == PAGES and data and page_new == len(data):
            saturated = 1
        time.sleep(PAGE_GAP)

    # 5-minute lookups, oldest first; anything past MISS_AFTER_MIN is written as missed
    stamp = now()
    due, missed = [], []
    for addr, created in sorted(pending.items(), key=lambda kv: kv[1]):
        age = (ts(stamp) - ts(created)).total_seconds() / 60
        if age >= MISS_AFTER_MIN:
            missed.append(addr)
        elif age >= SNAP_AT_MIN:
            due.append(addr)
    snaps = 0
    with open(SNAPS, "a") as fs:
        for addr in missed:
            fs.write(json.dumps({"address": addr, "kind": "missed", "seen": stamp}) + "\n")
        for i in range(0, min(len(due), MULTI_MAX * MULTI_CALLS_MAX), MULTI_MAX):
            batch = due[i:i + MULTI_MAX]
            data = fetch(MULTI % ",".join(batch), errors, "multi %d" % (i // MULTI_MAX + 1))
            if data is None:
                continue
            got_back = set()
            for p in data:
                a = p["attributes"]
                created = a.get("pool_created_at")
                age = (ts(now()) - ts(created)).total_seconds() / 60 if created else None
                fs.write(json.dumps({"address": a.get("address"), "kind": "5min", "age_min": round(age, 2) if age else None,
                                     "seen": now(), **trim(a)}) + "\n")
                got_back.add(a.get("address"))
                snaps += 1
            for addr in batch:
                if addr not in got_back:
                    fs.write(json.dumps({"address": addr, "kind": "gone", "seen": now()}) + "\n")
            time.sleep(PAGE_GAP)
    with open(POLLS, "a") as f:
        f.write(json.dumps({"ts": now(), "rows": got, "new": new, "snaps": snaps, "missed": len(missed),
                            "due": len(due), "pending": len(pending) - snaps - len(missed),
                            "last_page_all_new": saturated, "secs": round(time.time() - t0, 1),
                            "errors": errors}) + "\n")


def summary():
    pools = [json.loads(l) for l in open(POOLS)] if os.path.exists(POOLS) else []
    polls = [json.loads(l) for l in open(POLLS)] if os.path.exists(POLLS) else []
    snaps = [json.loads(l) for l in open(SNAPS)] if os.path.exists(SNAPS) else []
    launches = {p["base"] for p in pools if p["dex"] == "pump-fun"}
    grads = {p["base"] for p in pools if p["dex"] == "pumpswap" and p["base"] in launches}
    print(json.dumps({"polls": len(polls), "polls_with_errors": sum(1 for p in polls if p["errors"]),
                      "polls_last_page_all_new": sum(p.get("last_page_all_new", 0) for p in polls),
                      "pools": len(pools), "by_dex": Counter(p["dex"] for p in pools).most_common(8),
                      "launch_tokens": len(launches), "graduated_tokens": len(grads),
                      "snapshots": Counter(s["kind"] for s in snaps).most_common(),
                      "first": polls[0]["ts"] if polls else None, "last": polls[-1]["ts"] if polls else None,
                      "done": os.path.exists(DONE)}, indent=1))


if __name__ == "__main__":
    {"poll": poll, "summary": summary, "load": load, "unload": unload}[sys.argv[1] if len(sys.argv) > 1 else "poll"]()
