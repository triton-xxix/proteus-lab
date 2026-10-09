"""Does holding a ranked pre-listing candidate list make money? Backtest on the last 12 months, with
the scorer fitted on the first half and judged on the second.

Rules, fixed before the first run (9 Oct 2026):
- Signals and targets exactly as analysis.py. A signal is "active" for 14 days after it is knowable.
- Probability per (signal, target), fitted on TRAIN (signals 9 Oct 2025 to 31 Mar 2026 only):
  p = (hits + 20 * base) / (n + 20), shrunk toward the target's base rate.
- Coin score on day d = 1 - product over targets the coin is not yet on, and over its active signals,
  of (1 - p). Coins with no active signal score 0 and are never listed.
- Each day at 00:00 UTC the top N coins by score (N = 10, 25, 50) form the list, equal weight.
  Stablecoins out.
- Daily paper return per member: close-to-close on the UTC daily candle (Binance, else OKX, else
  Bybit). If a target announcement for the member lands that day, the day's return is the coin's
  1-minute event-study result for that event (hold price to the low of the +3 minute bar, costs in)
  when it exists, else the venue's TEST-half median from minute.py; the coin then leaves the list.
- Costs: 0.25% each time a coin enters the list and each time it leaves it without a hit.
- Judged on TEST (1 Apr to 24 Sep 2026): total and mean daily return of each list, against
  (a) holding the whole universe equal weight (beats holding) and (b) 200 random lists of the same
  size drawn each day from coins with any active signal (beats luck: the share of random runs the
  list beats). TRAIN results are printed and labelled in-sample.
Writes backtest.json.
"""
import json
import math
import os
import random
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402

DAY = A.DAY
SPLIT = datetime(2026, 4, 1, tzinfo=timezone.utc).timestamp()
ACTIVE = 14 * DAY
SHRINK = 20
SIDE_COST = 0.0025
SIZES = (10, 25, 50)


def fit(sig, targets, before, avail, base):
    p = {}
    for tgt in targets:
        by = defaultdict(lambda: [0, 0])
        for x in sig:
            if not (A.W0 <= x["t"] < SPLIT) or A.on_target(x["symbol"], x["t"], tgt, targets, before):
                continue
            if (x["signal"], tgt) in (("upbit_krw", "upbit_krw"), ("binance_spot_announce", "binance_spot")):
                continue
            tt = targets[tgt].get(x["symbol"])
            by[x["signal"]][0] += tt is not None and x["t"] < tt <= x["t"] + A.H
            by[x["signal"]][1] += 1
        for name, (h, n) in by.items():
            p[(name, tgt)] = (h + SHRINK * base[tgt]) / (n + SHRINK)
    return p


def pops():
    """Per-event 3-minute result from the 1-minute study, keyed (venue, symbol), and venue medians on TEST."""
    ev, med = {}, {}
    for f in ("minute_events.json", "minute_coinbase.json"):
        p = os.path.join(HERE, f)
        if not os.path.exists(p):
            continue
        for r in json.load(open(p)):
            if r.get("pess_3") is not None:
                ev[(r["venue"], r["symbol"])] = r["pess_3"]
                if r["t"] >= SPLIT:
                    med.setdefault(r["venue"], []).append(r["pess_3"])
    return ev, {k: statistics.median(v) for k, v in med.items()}


def run():
    st, targets, before, avail, sig, turn, days, dix, close = A.build()
    res = A.tables(targets, before, avail, sig, turn, days, dix) if not os.path.exists(os.path.join(HERE, "research.json")) else json.load(open(os.path.join(HERE, "research.json")))
    base = {t: res[t]["base_rate_14d"] for t in targets}
    p = fit(sig, targets, before, avail, base)
    ev_pop, med_pop = pops()
    venue_of = {"upbit_krw": "upbit", "binance_spot": "binance", "coinbase": "coinbase"}
    fallback = {"upbit": 0.158, "binance": 0.06, "coinbase": 0.0}
    by_sym = defaultdict(list)
    for x in sig:
        by_sym[x["symbol"]].append(x)

    def score(s, d):
        q = 1.0
        for tgt in targets:
            if A.on_target(s, d, tgt, targets, before):
                continue
            for x in by_sym.get(s, []):
                if d - ACTIVE <= x["t"] <= d and (x["signal"], tgt) in p:
                    q *= 1 - p[(x["signal"], tgt)]
        return 1 - q

    def day_ret(s, d0):
        """Holding s from d0 to d0 + 1 day: (return, whether a target announcement ended it)."""
        for tgt in targets:
            tt = targets[tgt].get(s)
            if tt is not None and d0 < tt <= d0 + DAY and not A.on_target(s, d0, tgt, targets, before):
                v = venue_of[tgt]
                return ev_pop.get((v, s), med_pop.get(v, fallback[v])), True
        # the candle keyed d0 - 1 day closes at d0; the one keyed d0 closes at d0 + 1 day
        a, b = close.get(s, {}).get(d0 - DAY), close.get(s, {}).get(d0)
        return (b / a - 1) if a and b else 0.0, False

    grid = [d for d in days if A.W0 <= d <= A.W1]
    out = {"sizes": {}, "fitted_p": {"%s->%s" % k: round(v, 4) for k, v in sorted(p.items(), key=lambda kv: -kv[1])[:40]}}
    rng = random.Random(9)
    for n in SIZES:
        held, rets, hits, pool_sizes = set(), [], [], []
        rand_rets = [[] for _ in range(200)]
        rand_held = [set() for _ in range(200)]
        uni = []
        for d in grid:
            scored = [(score(s, d), s) for s in avail if avail[s] <= d and s not in A.STABLE]
            pool = [s for v, s in scored if v > 0]
            pool_sizes.append(len(pool))
            top = [s for v, s in sorted(scored, reverse=True)[:n] if v > 0]
            # the day runs from d to d + 1: return measured on the candle that closes at d + 1
            r, cost = [], 0.0
            for s in top:
                if s not in held:
                    cost += SIDE_COST
            for s in held - set(top):
                cost += SIDE_COST
            hit_today = []
            for s in top:
                x, hit = day_ret(s, d)
                r.append(x)
                if hit:
                    hit_today.append(s)
            held = set(top) - set(hit_today)
            rets.append((d, (sum(r) - cost) / max(1, len(top)) if top else 0.0, len(top)))
            hits += [(d, s) for s in hit_today]
            u = [day_ret(s, d)[0] for s in avail if avail[s] <= d and s not in A.STABLE and close.get(s, {}).get(d)]
            uni.append((d, statistics.mean(u) if u else 0.0))
            for k in range(200):
                pick = rng.sample(pool, min(len(top), len(pool))) if pool else []
                rc = sum(SIDE_COST for s in pick if s not in rand_held[k]) + sum(SIDE_COST for s in rand_held[k] - set(pick))
                rr = [day_ret(s, d) for s in pick]
                rand_rets[k].append((d, (sum(x for x, _ in rr) - rc) / max(1, len(pick)) if pick else 0.0))
                rand_held[k] = {s for s, (x, h) in zip(pick, rr) if not h}

        def total(xs, lo, hi):
            v = 1.0
            for d, x, *rest in xs:
                if lo <= d < hi:
                    v *= 1 + x
            return v - 1

        block = {}
        for half, lo, hi in (("train_in_sample", A.W0, SPLIT), ("test", SPLIT, A.W1 + DAY)):
            mine = total(rets, lo, hi)
            rand = sorted(total(rr, lo, hi) for rr in rand_rets)
            block[half] = {"list_total_pct": round(100 * mine, 1), "universe_total_pct": round(100 * total(uni, lo, hi), 1),
                           "random_median_pct": round(100 * statistics.median(rand), 1),
                           "share_of_random_beaten": round(sum(x < mine for x in rand) / len(rand), 2),
                           "hits": sum(1 for d, s in hits if lo <= d < hi),
                           "hit_symbols": [s for d, s in hits if lo <= d < hi],
                           "member_days": sum(k for d, x, k in rets if lo <= d < hi)}
            md = block[half]["member_days"]
            block[half]["hits_per_100_member_days"] = round(100 * block[half]["hits"] / md, 2) if md else None
        block["median_pool_with_any_signal"] = statistics.median(pool_sizes)
        out["sizes"][str(n)] = block
        print("top", n, json.dumps(block, indent=1), flush=True)
    json.dump(out, open(os.path.join(HERE, "backtest.json"), "w"), indent=1)


if __name__ == "__main__":
    run()
