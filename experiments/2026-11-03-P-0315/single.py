"""P-0315: P-0305's split rerun from single-profile pulls (/api/user/<id>), which carry `count` and
playTime.human that the /api/users batch left out. Same two groups, same best-single-threshold accuracy."""
import csv, json, statistics as st, time, urllib.request, urllib.error

ROOT = "/Users/triton/PROTEUS"
EXP = ROOT + "/experiments/2026-11-03-P-0315"
nobot = {r["opponent"].lower() for r in csv.DictReader(open(ROOT + "/games/lichess/CHALLENGES.csv"))
         if r["verdict"] == "declined" and r["detail"].strip() == "nobot"}
played = {r["opponent"].lower() for r in csv.DictReader(open(ROOT + "/games/lichess/GAMES.csv"))}
both = nobot & played
nobot -= both
played -= both
users, errors = [], {}
for uid in sorted(nobot | played):
    try:
        req = urllib.request.Request("https://lichess.org/api/user/" + uid, headers={"Accept": "application/json"})
        users.append(json.load(urllib.request.urlopen(req, timeout=20)))
    except urllib.error.HTTPError as e:
        errors[uid] = e.code
        if e.code == 429:
            print("429, stopping")
            break
    time.sleep(1)
json.dump(users, open(ROOT + "/sandbox/p0315-single-users.json", "w"))

def feats(u):
    c = u.get("count", {})
    pt = u.get("playTime", {})
    allg = c.get("all", 0) or 0
    return {
        "games_all": allg,
        "rated_count": c.get("rated", 0),
        "rated_share": c.get("rated", 0) / allg if allg else 0,
        "human_time_share": pt.get("human", 0) / pt["total"] if pt.get("total") else 0,
        "play_hours": pt.get("total", 0) / 3600,
        "draw_share": c.get("draw", 0) / allg if allg else 0,
        "win_share": c.get("win", 0) / allg if allg else 0,
    }

rows = [("nobot" if u["id"] in nobot else "played", feats(u)) for u in users
        if not u.get("disabled") and u["id"] in nobot | played]
n = len(rows)
res = {"nobot_ids": len(nobot), "played_ids": len(played), "errors": errors,
       "kept": {"nobot": sum(g == "nobot" for g, _ in rows), "played": sum(g == "played" for g, _ in rows)}, "fields": {}}
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
res["base_rate_accuracy"] = round(max(res["kept"].values()) / n, 3)
print("kept", res["kept"], "base rate", res["base_rate_accuracy"], "errors", errors)
json.dump(res, open(EXP + "/results.json", "w"), indent=1)
