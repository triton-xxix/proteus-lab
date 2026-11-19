#!/usr/bin/env python3
"""How many logged Lichess challenges went to accounts that were not there?
Keyless: one POST to api/users with every opponent in CHALLENGES.csv. No challenge is sent."""
import csv, json, os, time, urllib.request
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = "/Users/triton/PROTEUS/games/lichess/CHALLENGES.csv"

rows = list(csv.DictReader(open(LOG)))
by = defaultdict(Counter)
last_ask = {}
for r in rows:
    o = r["opponent"].lower()
    by[o][r["verdict"]] += 1
    last_ask[o] = r["utc"]
names = sorted(by)
req = urllib.request.Request("https://lichess.org/api/users", ",".join(names).encode(),
                             {"Content-Type": "text/plain", "User-Agent": "probe/1.0"})
users = {u["id"]: u for u in json.loads(urllib.request.urlopen(req, timeout=40).read())}
now = time.time() * 1000
out = []
for n in names:
    u = users.get(n)
    c = by[n]
    seen_d = round((now - u["seenAt"]) / 86400000, 1) if u and u.get("seenAt") else None
    state = ("missing" if not u else "closed" if u.get("disabled") else "tos" if u.get("tosViolation")
             else "absent30" if seen_d is None or seen_d > 30 else "absent7" if seen_d > 7 else "present")
    out.append({"name": n, "state": state, "seen_days_ago": seen_d, "asks": sum(c.values()), "accepted": c["accepted"],
                "declined": c["declined"], "no_answer": c["no answer"], "refused": c["refused 400"] + c["refused 429"],
                "last_ask": last_ask[n]})
tot = len(rows)
acc = sum(r["accepted"] for r in out)
states = Counter()
asks = Counter()
accs = Counter()
for r in out:
    states[r["state"]] += 1
    asks[r["state"]] += r["asks"]
    accs[r["state"]] += r["accepted"]
gone = [s for s in states if s != "present" and s != "absent7"]
gone_asks = sum(asks[s] for s in gone)
never = [r for r in out if r["accepted"] == 0]
summary = {"challenges": tot, "opponents": len(names), "accepted": acc, "acceptance_rate": round(acc / tot, 4),
           "opponents_by_state": dict(states), "asks_by_state": dict(asks), "accepted_by_state": dict(accs),
           "asks_to_gone_accounts": gone_asks, "share_of_asks_to_gone": round(gone_asks / tot, 4),
           "acceptance_rate_without_gone": round((acc - sum(accs[s] for s in gone)) / max(1, tot - gone_asks), 4),
           "never_accepted_opponents": len(never), "asks_to_never_accepted": sum(r["asks"] for r in never),
           "never_accepted_but_present": sum(1 for r in never if r["state"] == "present"),
           "asks_to_never_accepted_but_present": sum(r["asks"] for r in never if r["state"] == "present"),
           "top_wasted": [[r["name"], r["state"], r["seen_days_ago"], r["asks"]] for r in
                          sorted(never, key=lambda r: -r["asks"])[:8]],
           "note": "seenAt is last seen online, not last rated game; asks made while an account was still active count as gone if it has left since"}
json.dump({"rows": out, "summary": summary}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(summary))
