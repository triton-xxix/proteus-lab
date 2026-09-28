"""P-0014 scoring: pump.fun graduation rate over the 24h poll, 27 to 28 Sep 2026.

Reads experiments/2026-09-27-P-0014/pools.jsonl and polls.jsonl. GeckoTerminal lists a bonding
curve launch as dex pump-fun and a graduated pool as dex pumpswap. Pool ids differ between the
two, so graduations are matched to launches by token name (the "X / SOL" label) with the pumpswap
pool created after the pump-fun pool. Names collide, so the matched figure is reported beside the
raw ratio and both are labelled. Writes analysis.json next to the inputs.
"""
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone

OUT = "/Users/triton/PROTEUS/experiments/2026-09-27-P-0014"


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


pools = [json.loads(l) for l in open(os.path.join(OUT, "pools.jsonl"))]
polls = [json.loads(l) for l in open(os.path.join(OUT, "polls.jsonl"))]

first, last = ts(polls[0]["ts"]), ts(polls[-1]["ts"])
hours = (last - first).total_seconds() / 3600
gaps = [(ts(b["ts"]) - ts(a["ts"])).total_seconds() for a, b in zip(polls, polls[1:])]
saturated = sum(1 for p in polls if p["new"] == p["rows"] and p["rows"] > 0)
rows_per_poll = Counter(p["rows"] for p in polls)

by_dex = Counter(p["dex"] for p in pools)
launches = [p for p in pools if p["dex"] == "pump-fun"]
grads = [p for p in pools if p["dex"] == "pumpswap"]

# window: launches created inside the poll window, so a graduation later in the window could be seen
in_window_launch = [p for p in launches if p["created"] and first <= ts(p["created"]) <= last]
in_window_grad = [p for p in grads if p["created"] and first <= ts(p["created"]) <= last]

# match by name: graduation pool created after a launch pool of the same name inside the window
launch_by_name = defaultdict(list)
for p in in_window_launch:
    launch_by_name[p["name"]].append(ts(p["created"]))
matched, lag_minutes = 0, []
for g in in_window_grad:
    cands = [t for t in launch_by_name.get(g["name"], []) if t <= ts(g["created"])]
    if cands:
        matched += 1
        lag_minutes.append((ts(g["created"]) - max(cands)).total_seconds() / 60)
lag_minutes.sort()


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def q(xs, f):
    return round(xs[int(f * (len(xs) - 1))], 1) if xs else None


# graduations per launch in the first 12 hours only, so every launch had at least 12h to graduate
mid = first + (last - first) / 2
early_launch = [p for p in in_window_launch if ts(p["created"]) <= mid]
early_names = defaultdict(list)
for p in early_launch:
    early_names[p["name"]].append(ts(p["created"]))
early_matched = 0
for g in in_window_grad:
    cands = [t for t in early_names.get(g["name"], []) if t <= ts(g["created"])]
    if cands:
        early_matched += 1

# per-hour launch and graduation counts, to show the feed cap
hour_launch = Counter(ts(p["created"]).strftime("%H") for p in in_window_launch)
hour_grad = Counter(ts(p["created"]).strftime("%H") for p in in_window_grad)

# name collisions among launches: how many names appear more than once
name_counts = Counter(p["name"] for p in in_window_launch)
dup_names = sum(1 for n, c in name_counts.items() if c > 1)

result = {
    "window_utc": [polls[0]["ts"], polls[-1]["ts"]],
    "hours": round(hours, 2),
    "polls": len(polls),
    "polls_with_errors": sum(1 for p in polls if p["errors"]),
    "poll_gap_seconds": {"min": min(gaps), "median": sorted(gaps)[len(gaps) // 2], "max": max(gaps)},
    "rows_per_poll": rows_per_poll.most_common(),
    "polls_saturated_all_rows_new": saturated,
    "pools_total": len(pools),
    "by_dex": by_dex.most_common(),
    "launches_pump_fun": len(launches),
    "graduations_pumpswap": len(grads),
    "raw_ratio_pct": pct(len(grads), len(launches)),
    "in_window_launches": len(in_window_launch),
    "in_window_graduations": len(in_window_grad),
    "graduations_matched_to_a_window_launch_by_name": matched,
    "matched_pct_of_window_launches": pct(matched, len(in_window_launch)),
    "first_half_launches": len(early_launch),
    "first_half_launches_graduated_by_end": early_matched,
    "first_half_pct": pct(early_matched, len(early_launch)),
    "lag_minutes_launch_to_graduation": {"n": len(lag_minutes), "p10": q(lag_minutes, 0.1),
                                         "median": q(lag_minutes, 0.5), "p90": q(lag_minutes, 0.9)},
    "launch_names_used_more_than_once": dup_names,
    "launches_per_hour_utc": sorted(hour_launch.items()),
    "graduations_per_hour_utc": sorted(hour_grad.items()),
    "launches_per_hour_mean": round(len(in_window_launch) / hours, 1),
    "graduations_per_hour_mean": round(len(in_window_grad) / hours, 1),
}
json.dump(result, open(os.path.join(OUT, "analysis.json"), "w"), indent=1)
print(json.dumps(result, indent=1))
