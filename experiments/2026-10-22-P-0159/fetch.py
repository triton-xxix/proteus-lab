"""P-0159 / D-013: candle fetch for G2 window two, outcomes unread.

Window two: G2 counted rows (latency <= 120 s, Jupiter liquidity at entry >= $50,000, P present) whose
block time is at or after the 14 Oct 16:34Z reload and whose entry is before 21 Oct 16:34Z. This script
reads only mint and entry_t from those rows and never P or any exit field, so the blind read stays blind.
Candles as P-0100 (GeckoTerminal 1-minute OHLCV, keyless, the mint's top pool), cached append-only in
candles.jsonl so any run resumes. Stops itself at --stop (epoch seconds) or on HALT.

    python3 fetch.py --count            # count only
    python3 fetch.py --stop 1792625400  # fetch until then
"""
import json
import os
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-10-P-0100")
import reprice as P0100  # noqa: E402  (get() and fetch() with the 2.2 s pace and 429 backoff)

OUT = "/Users/triton/PROTEUS/experiments/2026-10-22-P-0159/"
CACHE = OUT + "candles.jsonl"
W2_FROM = 1791995640   # 2026-10-14T16:34:00Z
W2_TO = 1792600440     # 2026-10-21T16:34:00Z


def window_two():
    keep = []
    for line in open("/Users/triton/PROTEUS/grinder/graduates/closed.jsonl"):
        r = json.loads(line)
        if (r.get("latency_s") is not None and r["latency_s"] <= 120 and (r.get("liq") or 0) >= 50000
                and r.get("P") is not None and r["block_t"] >= W2_FROM and r["entry_t"] < W2_TO):
            keep.append({"mint": r["mint"], "entry_t": r["entry_t"]})
    return sorted(keep, key=lambda r: r["entry_t"])


def main():
    import time
    ts = window_two()
    have = set()
    if os.path.exists(CACHE):
        have = {json.loads(l)["key"] for l in open(CACHE)}
    todo = [r for r in ts if "%s|%d" % (r["mint"], int(r["entry_t"])) not in have]
    print("window two counted", len(ts), "cached", len(ts) - len(todo), "to fetch", len(todo), flush=True)
    if "--count" in sys.argv:
        return
    stop = int(sys.argv[sys.argv.index("--stop") + 1]) if "--stop" in sys.argv else 0
    done = 0
    with open(CACHE, "a") as fh:
        for r in todo:
            if stop and time.time() >= stop:
                print("stop time reached", flush=True)
                break
            if os.path.exists("/Users/triton/PROTEUS/HALT"):
                print("HALT", flush=True)
                break
            d = P0100.fetch(r)
            d["key"] = "%s|%d" % (r["mint"], int(r["entry_t"]))
            fh.write(json.dumps(d) + "\n")
            fh.flush()
            done += 1
            if done % 10 == 0:
                print("fetched", done, "of", len(todo), round(time.time()), flush=True)
    print("fetched this run", done, flush=True)


if __name__ == "__main__":
    main()
