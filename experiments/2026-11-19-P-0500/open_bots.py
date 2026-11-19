#!/usr/bin/env python3
"""Which of P-0492's 30 unchallenged bots look most open to a new opponent?
Keyless Lichess game export, 20 rated blitz games each, paced 3 s. No challenge is sent."""
import json, os, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/triton/PROTEUS/experiments/2026-11-19-P-0492/results.json"
URL = "https://lichess.org/api/games/user/%s?max=20&rated=true&perfType=blitz"
ME = 2983


def games(name):
    req = urllib.request.Request(URL % name, headers={"Accept": "application/x-ndjson", "User-Agent": "probe/1.0"})
    for i in range(3):
        try:
            raw = urllib.request.urlopen(req, timeout=40).read().decode()
            return [json.loads(l) for l in raw.splitlines() if l.strip()], None
        except Exception as e:
            err = str(e)
            time.sleep(20 * (i + 1))
    return [], err


rows = []
for name, blitz, total, _ in json.load(open(SRC))["summary"]["try_these"]:
    gs, err = games(name)
    time.sleep(3)
    if not gs:
        rows.append({"name": name, "blitz": blitz, "err": err or "no games"})
        continue
    opps = []
    for g in gs:
        for side in ("white", "black"):
            p = g["players"][side]
            u = p.get("user") or {}
            if u.get("id", "").lower() != name.lower():
                opps.append({"id": u.get("id"), "bot": u.get("title") == "BOT", "rating": p.get("rating")})
    rated = [o for o in opps if o["rating"]]
    span_d = (gs[0]["createdAt"] - gs[-1]["createdAt"]) / 86400000
    last_d = (time.time() * 1000 - gs[0]["createdAt"]) / 86400000
    rows.append({"name": name, "blitz": blitz, "games": len(gs), "distinct_opponents": len({o["id"] for o in opps}),
                 "bot_share": round(sum(o["bot"] for o in opps) / len(opps), 2),
                 "within_200": round(sum(1 for o in rated if abs(o["rating"] - blitz) <= 200) / max(1, len(rated)), 2),
                 "opp_rating_min": min(o["rating"] for o in rated), "opp_rating_max": max(o["rating"] for o in rated),
                 "would_reach_me": min(o["rating"] for o in rated) <= ME <= max(o["rating"] for o in rated),
                 "games_per_day": round(len(gs) / span_d, 1) if span_d > 0 else None, "days_since_last": round(last_d, 2)})
    print(rows[-1])
ok = [r for r in rows if "games" in r]
ranked = sorted(ok, key=lambda r: (-r["distinct_opponents"], r["days_since_last"]))
summary = {"asked": len(rows), "answered": len(ok), "errors": len(rows) - len(ok),
           "ten_or_more_distinct": sum(1 for r in ok if r["distinct_opponents"] >= 10),
           "three_or_fewer_distinct": sum(1 for r in ok if r["distinct_opponents"] <= 3),
           "all_bot_opponents": sum(1 for r in ok if r["bot_share"] == 1.0),
           "my_rating_inside_their_range": sum(1 for r in ok if r["would_reach_me"]),
           "top_five": [[r["name"], r["blitz"], r["distinct_opponents"], r["games_per_day"]] for r in ranked[:5]]}
json.dump({"rows": rows, "summary": summary}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(summary))
