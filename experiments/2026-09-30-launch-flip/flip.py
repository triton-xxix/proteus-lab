#!/usr/bin/env python3
"""Luke's question, 30 Sep 2026: buy a pump.fun launch right at the start and sell 20 to 30 minutes
in; what would it have made? Random sample of the 26,801 pump-fun launches P-0032 logged over 24h
(28 to 29 Sep), GeckoTerminal minute candles from creation, three entry timings, exits at 20 and 30
minutes, plus a -50% stop version. Paper only; descriptive.

Costs: v0.2's model (paths.pnl_v02): 1% fee and $0.05 each side, constant-product impact, exit
slippage. Depth on the bonding curve is the curve's virtual reserve, not GeckoTerminal's "reserve":
pump.fun starts every curve with 30 virtual SOL, so quote depth is taken as 30 SOL at $200 plus half
the reported reserve. Stated, not measured. A pool with no trade after entry exits at the last price,
which on a bonding curve is sellable (the curve always quotes).

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-09-30-launch-flip/flip.py [N]
"""
import json
import os
import random
import statistics as st
import sys
import time
from datetime import datetime, timezone

import requests

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paths  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/triton/PROTEUS/experiments/2026-09-28-P-0032/"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
DEX = sys.argv[2] if len(sys.argv) > 2 else "pump-fun"
CACHE = HERE + "/candles/"
os.makedirs(CACHE, exist_ok=True)
VIRTUAL_QUOTE_USD = 30 * 200


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def candles(addr, created):
    p = CACHE + addr + ".json"
    if os.path.exists(p):
        return json.load(open(p))
    r = None
    for attempt in range(8):
        r = requests.get("https://api.geckoterminal.com/api/v2/networks/solana/pools/%s/ohlcv/minute" % addr,
                         params={"aggregate": 1, "limit": 100, "currency": "usd", "token": "base",
                                 "before_timestamp": int(created + 75 * 60)},
                         headers={"Accept": "application/json", "User-Agent": "proteus-lab/0.2"}, timeout=30)
        if r.status_code == 429:
            time.sleep(30 * (attempt + 1)); continue
        break
    if r is None or r.status_code not in (200, 404):
        return None                     # rate-limited or failing: not cached, so a rerun tries again
    c = sorted(r.json()["data"]["attributes"]["ohlcv_list"]) if r.status_code == 200 else None
    json.dump(c, open(p, "w"))
    time.sleep(3.0)
    return c


def exit_at(c, t_entry, entry, minutes, stop=None):
    horizon = t_entry + minutes * 60
    last = entry
    for t, o, h, l, cl, v in c:
        if t <= t_entry - 60:
            continue
        if t >= horizon:
            break
        if stop is not None and l <= entry * (1 + stop):
            return (o if o <= entry * (1 + stop) else entry * (1 + stop)), "stop_loss"
        last = cl
    return last, "time_stop"


def main():
    pools = [json.loads(l) for l in open(SRC + "pools.jsonl")]
    launches = [p for p in pools if p["dex"] == DEX]
    first = {}
    for l in open(SRC + "snapshots.jsonl"):
        s = json.loads(l)
        if s["kind"] == "first":
            first[s["id"]] = s
    random.seed(20260930)
    sample = random.sample(launches, min(N, len(launches)))
    rows = []
    for i, p in enumerate(sample):
        addr = p["id"].split("_", 1)[1]
        created, seen = ts(p["created"]), ts(p["seen"])
        c = candles(addr, created)
        if (i + 1) % 50 == 0:
            print("candles %d/%d" % (i + 1, len(sample)), flush=True)
        if not c:
            rows.append({"id": addr, "status": "no-candles"}); continue
        snap = first.get(p["id"], {})
        if DEX == "pump-fun":
            depth = VIRTUAL_QUOTE_USD + (float(snap.get("reserve") or 0) / 2)
        elif snap.get("reserve"):
            depth = max(float(snap["reserve"]) / 2, 1000.0)
        else:
            depth = VIRTUAL_QUOTE_USD        # launchpad curves without a snapshot: same assumption as pump.fun, stated
        liq = 2 * depth
        rec = {"id": addr, "name": p["name"], "status": "ok", "n_candles": len(c),
               "minutes_traded": len({x[0] for x in c if x[0] < created + 75 * 60}),
               "peak_60m": max(x[2] for x in c if x[0] < created + 3600) / c[0][1] - 1}
        entries = {
            "launch": (c[0][0], c[0][1]),                                         # open of the first traded minute: the fantasy fill
            "minute2": next(((x[0], x[1]) for x in c if x[0] >= c[0][0] + 60), (c[-1][0], c[-1][4])),   # a fast bot, one minute behind
            "seen": next(((x[0], x[1]) for x in c if x[0] >= seen), (c[-1][0], c[-1][4])),              # when our 2-minute poller saw it
        }
        for en, (t0, e) in entries.items():
            for mins in (20, 30):
                for stop in (None, -0.5):
                    fill, reason = exit_at(c, t0, e, mins, stop)
                    key = "%s_%dm%s" % (en, mins, "_stop" if stop else "")
                    rec[key] = paths.pnl_v02(e, fill, reason, 100.0, liq)
                    rec[key + "_move"] = fill / e - 1
        rows.append(rec)
    json.dump(rows, open(HERE + "/results-%s.json" % DEX, "w"))
    ok = [r for r in rows if r["status"] == "ok"]
    L = ["# Buy a %s launch, sell 20 to 30 minutes in" % DEX, "",
         "Random sample of %d of the %d %s pools P-0032 logged, 28 to 29 Sep 2026; %d with candles. "
         "£100 paper stake, v0.2 costs, depth assumed where not measured (see flip.py). Paper, in-sample." % (len(sample), len(launches), DEX, len(ok)), "",
         "Trading life: median %d traded minutes in the first 75; %d%% traded in 5 minutes or fewer." % (
             st.median(r["minutes_traded"] for r in ok), 100 * sum(r["minutes_traded"] <= 5 for r in ok) / len(ok)), "",
         "| Entry | Exit | Exp £ per trade | Median move | Winners | Best-3 removed | Total £ over %d trades |" % len(ok),
         "|---|---|---|---|---|---|---|"]
    for en in ("launch", "minute2", "seen"):
        for mins in (20, 30):
            for stop in ("", "_stop"):
                k = "%s_%dm%s" % (en, mins, stop)
                p = sorted(r[k] for r in ok)
                L.append("| %s | %d min%s | %.1f | %+.0f%% | %d%% | %.1f | %.0f |" % (
                    {"launch": "first traded minute (fantasy)", "minute2": "one minute later", "seen": "when our poller saw it"}[en],
                    mins, ", -50% stop" if stop else "", st.mean(p), 100 * st.median(r[k + "_move"] for r in ok),
                    100 * sum(x > 0 for x in p) / len(p), st.mean(p[:-3]), sum(p)))
    open(HERE + "/REPORT-%s.md" % DEX, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
