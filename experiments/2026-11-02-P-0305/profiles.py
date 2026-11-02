"""P-0305: can a bot's public profile say in advance that it will decline another bot ("nobot")?
Two groups from my own logs: bots that declined me with reason nobot (games/lichess/CHALLENGES.csv) and bots
that played me (GAMES.csv), minus any in both. One keyless POST to lichess.org/api/users (up to 300 ids),
then per field: each group's median, and the best single threshold's accuracy at splitting the two.

    python3 -I experiments/2026-11-02-P-0305/profiles.py
"""
import csv
import json
import statistics as st
import time
import urllib.request

ROOT = "/Users/triton/PROTEUS"
EXP = ROOT + "/experiments/2026-11-02-P-0305"
nobot = {r["opponent"].lower() for r in csv.DictReader(open(ROOT + "/games/lichess/CHALLENGES.csv"))
         if r["verdict"] == "declined" and r["detail"].strip() == "nobot"}
played = {r["opponent"].lower() for r in csv.DictReader(open(ROOT + "/games/lichess/GAMES.csv"))}
both = nobot & played
nobot -= both
played -= both
ids = sorted(nobot | played)[:300]
req = urllib.request.Request("https://lichess.org/api/users", data=",".join(ids).encode(),
                             headers={"Content-Type": "text/plain", "Accept": "application/json"})
users = json.load(urllib.request.urlopen(req, timeout=60))
json.dump(users, open(ROOT + "/sandbox/p0305-users.json", "w"))
now = time.time() * 1000


def feats(u):
    perfs = u.get("perfs", {})
    g = lambda k: perfs.get(k, {}).get("games", 0)  # noqa: E731
    c = u.get("count", {})
    allg = c.get("all", 0) or 0
    return {
        "games_all": allg,
        "rated_share": (c.get("rated", 0) / allg) if allg else 0,
        "bullet_share": g("bullet") / max(1, g("bullet") + g("blitz") + g("rapid") + g("classical")),
        "classical_share": g("classical") / max(1, g("bullet") + g("blitz") + g("rapid") + g("classical")),
        "age_days": (now - u.get("createdAt", now)) / 86400000,
        "days_since_seen": (now - u.get("seenAt", now)) / 86400000,
        "blitz_rating": perfs.get("blitz", {}).get("rating", 0),
        "has_bio": 1 if (u.get("profile") or {}).get("bio") else 0,
        "bio_mentions_bot": 1 if "bot" in ((u.get("profile") or {}).get("bio") or "").lower() else 0,
        "is_bot_title": 1 if u.get("title") == "BOT" else 0,
    }


rows = []
for u in users:
    uid = u["id"]
    grp = "nobot" if uid in nobot else "played" if uid in played else None
    if grp and not u.get("disabled"):
        rows.append((grp, feats(u)))
res = {"nobot_ids": len(nobot), "played_ids": len(played), "in_both_dropped": sorted(both),
       "returned": len(users), "kept": {"nobot": sum(g == "nobot" for g, _ in rows),
                                        "played": sum(g == "played" for g, _ in rows)}, "fields": {}}
n = len(rows)
for f in rows[0][1]:
    a = [x[f] for g, x in rows if g == "nobot"]
    b = [x[f] for g, x in rows if g == "played"]
    best = (0, None, None)
    for t in sorted({x[f] for _, x in rows}):
        for side in ("ge", "lt"):
            right = sum(1 for g, x in rows if (g == "nobot") == ((x[f] >= t) if side == "ge" else (x[f] < t)))
            if right > best[0]:
                best = (right, t, side)
    res["fields"][f] = {"nobot_median": round(st.median(a), 3), "played_median": round(st.median(b), 3),
                        "best_split_accuracy": round(best[0] / n, 3), "nobot_if": "%s %s" % (best[2], round(best[1], 3))}
    print(f, res["fields"][f])
base = max(res["kept"].values()) / n
res["base_rate_accuracy"] = round(base, 3)
print("kept", res["kept"], "base rate", round(base, 3))
json.dump(res, open(EXP + "/results.json", "w"), indent=1)
