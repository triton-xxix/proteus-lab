"""P-0279: who do the bots that always decline my Lichess bot actually play?

From games/lichess/CHALLENGES.csv: opponents asked at least 3 times whose verdicts were only
'declined' or 'no answer' (never 'accepted'; 'refused 4xx' rows are the API's own cap errors and are
not counted as an answer). For the 24 most-asked, pull their last 60 rated games keyless from
lichess.org/api/games/user/<bot> (NDJSON; the endpoint 404s to a bare curl user agent, so a browser
one is sent) and record: games a day over the span, median opponent rating, share of bot opponents,
and the rating gap to mine (3035). Run with python3 -I.
"""
import csv
import json
import statistics
import time
import urllib.request

ROOT = "/Users/triton/PROTEUS"
OUT = ROOT + "/experiments/2026-11-01-P-0279/results.json"
MY_RATING = 3035
UA = {"User-Agent": "Mozilla/5.0 (proteus-probe; research)", "Accept": "application/x-ndjson"}

asks, accepted, answered = {}, {}, {}
for r in csv.DictReader(open(ROOT + "/games/lichess/CHALLENGES.csv")):
    o = r["opponent"].lower()
    asks[o] = asks.get(o, 0) + 1
    if r["verdict"] == "accepted":
        accepted[o] = accepted.get(o, 0) + 1
    if r["verdict"] in ("declined", "no answer"):
        answered[o] = answered.get(o, 0) + 1
decliners = sorted((o for o in asks if accepted.get(o, 0) == 0 and answered.get(o, 0) >= 3),
                   key=lambda o: -asks[o])[:24]
print("opponents asked", len(asks), "never accepted with 3+ declines or silences", len([o for o in asks if accepted.get(o, 0) == 0 and answered.get(o, 0) >= 3]), "taking", len(decliners), flush=True)

rows = []
for o in decliners:
    rec = {"bot": o, "asked": asks[o], "declined_or_silent": answered[o]}
    try:
        req = urllib.request.Request(f"https://lichess.org/api/games/user/{o}?max=60&rated=true&moves=false", headers=UA)
        with urllib.request.urlopen(req, timeout=60) as resp:
            lines = [l for l in resp.read().decode("utf-8").splitlines() if l.strip()]
        games = [json.loads(l) for l in lines]
        opp_r, bot_opp, times = [], 0, []
        for g in games:
            p = g.get("players", {})
            side = "white" if (p.get("white", {}).get("user", {}).get("id") == o) else "black"
            other = p.get("black" if side == "white" else "white", {})
            if other.get("rating") is not None:
                opp_r.append(other["rating"])
            if (other.get("user") or {}).get("title") == "BOT":
                bot_opp += 1
            times.append(g.get("createdAt", 0))
        span_days = (max(times) - min(times)) / 86400000 if len(times) > 1 else None
        rec.update({"games": len(games), "span_days": round(span_days, 1) if span_days else None,
                    "games_per_day": round(len(games) / span_days, 1) if span_days else None,
                    "opp_rating_median": statistics.median(opp_r) if opp_r else None,
                    "opp_rating_min_max": [min(opp_r), max(opp_r)] if opp_r else None,
                    "bot_opponent_share": round(bot_opp / len(games), 2) if games else None,
                    "gap_to_me_median": (statistics.median(opp_r) - MY_RATING) if opp_r else None,
                    "last_game_utc": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(max(times) / 1000)) if times else None})
    except Exception as e:  # noqa: BLE001
        rec["error"] = f"{type(e).__name__}: {e}"[:100]
    rows.append(rec)
    print(rec, flush=True)
    time.sleep(1.5)

ok = [r for r in rows if r.get("games")]
res = {"decliners": len(rows), "fetched": len(ok),
       "median_opp_rating_across_bots": statistics.median(r["opp_rating_median"] for r in ok if r["opp_rating_median"]) if ok else None,
       "median_games_per_day": statistics.median(r["games_per_day"] for r in ok if r["games_per_day"]) if ok else None,
       "bots_whose_median_opponent_is_within_200_of_me": sum(1 for r in ok if r["gap_to_me_median"] is not None and abs(r["gap_to_me_median"]) <= 200),
       "bots_playing_mostly_bots": sum(1 for r in ok if (r["bot_opponent_share"] or 0) >= 0.5),
       "bots_idle_60_games_over_30d": sum(1 for r in ok if (r["span_days"] or 0) > 30),
       "rows": rows}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
