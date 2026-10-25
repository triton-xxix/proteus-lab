"""P-0222: Polymarket resolution lag and dispute settings across 200 recently closed markets (Gamma API, keyless)."""
import collections, json, statistics, time, urllib.request
from datetime import datetime

OUT = "/Users/triton/PROTEUS/experiments/2026-10-25-P-0222/results.json"
URL = "https://gamma-api.polymarket.com/markets?closed=true&limit=100&offset=%d&order=closedTime&ascending=false"


def ts(s):
    if not s:
        return None
    s = s.replace("Z", "+00:00").replace(" ", "T")
    if s.endswith("+00"):
        s += ":00"
    s = s.replace("+00:00:00", "+00:00")
    return datetime.fromisoformat(s)


rows = []
for off in (0, 100):
    req = urllib.request.Request(URL % off, headers={"User-Agent": "proteus-probe/1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        rows += json.load(r)
    time.sleep(1)

lags, sports_lags, other_lags = [], [], []
liveness, bonds, statuses, auto = collections.Counter(), collections.Counter(), collections.Counter(), 0
for m in rows:
    end, closed = ts(m.get("endDate")), ts(m.get("closedTime"))
    if end and closed:
        h = (closed - end).total_seconds() / 3600
        lags.append(h)
        (sports_lags if m.get("sportsMarketType") or m.get("gameStartTime") else other_lags).append(h)
    liveness[m.get("customLiveness", "default")] += 1
    bonds[m.get("umaBond")] += 1
    st = json.loads(m.get("umaResolutionStatuses") or "[]")
    statuses[len(st)] += 1
    auto += bool(m.get("automaticallyResolved"))


def q(xs, p):
    xs = sorted(xs)
    return round(xs[int(p * (len(xs) - 1))], 2) if xs else None


res = {
    "pulled": len(rows), "with_both_dates": len(lags),
    "lag_h_median": q(lags, 0.5), "lag_h_p10": q(lags, 0.1), "lag_h_p90": q(lags, 0.9),
    "share_lag_over_2h": round(sum(h > 2 for h in lags) / len(lags), 3) if lags else None,
    "share_closed_before_end": round(sum(h < 0 for h in lags) / len(lags), 3) if lags else None,
    "sports_n": len(sports_lags), "sports_lag_h_median": q(sports_lags, 0.5),
    "other_n": len(other_lags), "other_lag_h_median": q(other_lags, 0.5),
    "custom_liveness_s": dict(liveness), "uma_bond": {str(k): v for k, v in bonds.items()},
    "proposal_status_list_length": dict(statuses), "automatically_resolved": auto,
    "closed_time_span": [rows[-1].get("closedTime"), rows[0].get("closedTime")],
}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
