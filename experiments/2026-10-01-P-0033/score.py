"""P-0033: score the P-0032 poller (24 h of GeckoTerminal new_pools, 6 pages every 2 min, 28-29 Sep 2026).

Counts against P-0014's floor, the graduation rate, and minute-five profiles of graduates versus the rest.
Graduation is matched by pool name ("X / SOL") between a pump-fun launch and a later pumpswap pool,
because the poller did not record the base token address.
"""
import json
import os
import statistics as st
from collections import Counter, defaultdict
from datetime import datetime, timezone

SRC = "/Users/triton/PROTEUS/experiments/2026-09-28-P-0032"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-01-P-0033"


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def rows(name):
    out = []
    for line in open(os.path.join(SRC, name)):
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), 2) if xs else None


def q(xs, p):
    xs = sorted(x for x in xs if x is not None)
    return round(xs[int(p * (len(xs) - 1))], 2) if xs else None


def main():
    polls, pools, snaps = rows("polls.jsonl"), rows("pools.jsonl"), rows("snapshots.jsonl")
    start, end = ts(polls[0]["ts"]), ts(polls[-1]["ts"])
    hours = (end - start).total_seconds() / 3600
    by_dex = Counter(p["dex"] for p in pools)
    gaps = [(ts(b["ts"]) - ts(a["ts"])).total_seconds() for a, b in zip(polls, polls[1:])]

    # launches created inside the window only, so the count is per day and not padded by the first poll
    launches = [p for p in pools if p["dex"] == "pump-fun" and p.get("created") and ts(p["created"]) >= start]
    swaps = [p for p in pools if p["dex"] == "pumpswap" and p.get("created") and ts(p["created"]) >= start]
    first_age = {s["id"]: s["age_min"] for s in snaps if s["kind"] == "first"}
    five = {}
    for s in snaps:
        if s["kind"] == "5min" and s["id"] not in five:
            five[s["id"]] = s

    by_name = defaultdict(list)
    for p in launches:
        by_name[p["name"]].append(p)
    grads, lat = set(), []
    for s in swaps:
        cands = by_name.get(s["name"], [])
        if len(cands) == 1 and ts(cands[0]["created"]) <= ts(s["created"]):
            grads.add(cands[0]["id"])
            lat.append((ts(s["created"]) - ts(cands[0]["created"])).total_seconds() / 60)
    unique_names = sum(1 for v in by_name.values() if len(v) == 1)

    def profile(ids):
        ss = [five[i] for i in ids if i in five]
        return {"n_with_5min_snapshot": len(ss),
                "age_min_median": med([s["age_min"] for s in ss]),
                "fdv_median": med([f(s["fdv"]) for s in ss]),
                "reserve_median": med([f(s["reserve"]) for s in ss]),
                "vol_m5_median": med([f(s["vol_m5"]) for s in ss]),
                "buyers_m5_median": med([f(s["buyers_m5"]) for s in ss]),
                "buyers_m5_p90": q([f(s["buyers_m5"]) for s in ss], 0.9),
                "buys_to_sells_m5_median": med([f(s["buys_m5"]) / f(s["sells_m5"]) for s in ss
                                                if f(s["sells_m5"]) and f(s["buys_m5"]) is not None])}

    grad_ids = [p["id"] for p in launches if p["id"] in grads]
    rest_ids = [p["id"] for p in launches if p["id"] not in grads]
    result = {
        "window_utc": [polls[0]["ts"], polls[-1]["ts"]], "hours": round(hours, 2),
        "polls": len(polls), "polls_with_errors": sum(1 for p in polls if p["errors"]),
        "polls_last_page_all_new": sum(p.get("last_page_all_new", 0) for p in polls),
        "poll_gap_s_median": med(gaps), "poll_gap_s_max": round(max(gaps), 1) if gaps else None,
        "pools_all_dexes": len(pools), "by_dex": by_dex.most_common(8),
        "pump_fun_launches_in_window": len(launches),
        "pump_fun_launches_per_day": round(len(launches) * 24 / hours),
        "pumpswap_pools_in_window": len(swaps),
        "first_seen_age_min_median": med([first_age[p["id"]] for p in launches if p["id"] in first_age]),
        "first_seen_age_min_p90": q([first_age[p["id"]] for p in launches if p["id"] in first_age], 0.9),
        "launches_with_unique_name": unique_names,
        "graduates_matched_by_name": len(grads),
        "graduation_rate_matched": round(len(grads) / len(launches), 4) if launches else None,
        "pumpswap_per_launch": round(len(swaps) / len(launches), 4) if launches else None,
        "grad_latency_min_median": med(lat), "grad_latency_min_p90": q(lat, 0.9),
        "minute_five_graduates": profile(grad_ids),
        "minute_five_rest": profile(rest_ids),
        "p0014_floor": {"pump_fun_launches": 7326, "pumpswap": 757, "estimate_launches_per_day": 14000},
    }
    with open(os.path.join(OUT, "result.json"), "w") as fh:
        json.dump(result, fh, indent=1)
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
