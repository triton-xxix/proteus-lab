#!/usr/bin/env python3
"""Build docs/ladder/data.json from the Lichess logs (Workshop, 30 Oct 2026).

Reads games/lichess/GAMES.csv (one row per rated game) and CHALLENGES.csv (one row per challenge
sent, accepted or not). Every number on the page comes from here. The games total, result split,
rating and strongest opponent beaten are checked against `lichess.py status`; exits non-zero if
they ever disagree.
"""
import csv
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = "/Users/triton/PROTEUS"
GAMES = os.path.join(ROOT, "games", "lichess", "GAMES.csv")
CHALL = os.path.join(ROOT, "games", "lichess", "CHALLENGES.csv")
OUT = os.path.join(ROOT, "docs", "ladder", "data.json")
VENV = os.path.join(ROOT, ".venv", "bin", "python3")
BANDS = [(0, 1500, "under 1500"), (1500, 2000, "1500 to 1999"), (2000, 2500, "2000 to 2499"), (2500, 9999, "2500 and up")]
SCORE = {"win": 1.0, "draw": 0.5, "loss": 0.0}


def main():
    games = list(csv.DictReader(open(GAMES)))
    chall = list(csv.DictReader(open(CHALL)))
    rows = []
    for g in games:
        rows.append({
            "date": g["finished_utc"][:10], "at": g["finished_utc"], "id": g["game_id"],
            "opponent": g["opponent"], "opp": int(g["opp_rating"]),
            "before": int(g["my_rating_before"]), "after": int(g["my_rating_after"]),
            "colour": g["colour"], "result": g["result"], "status": g["status"],
            "moves": int(g["moves"] or 0), "url": g["url"], "think": g.get("think_s", ""),
            "refusals": int(g["refusals"]) if g.get("refusals") else None,
        })
    rows.sort(key=lambda r: r["at"])
    n = len(rows)
    wins = sum(r["result"] == "win" for r in rows)
    draws = sum(r["result"] == "draw" for r in rows)
    losses = n - wins - draws
    beaten = [r["opp"] for r in rows if r["result"] == "win"]
    bands = []
    for lo, hi, label in BANDS:
        b = [r for r in rows if lo <= r["opp"] < hi]
        bands.append({"label": label, "n": len(b),
                      "wins": sum(r["result"] == "win" for r in b),
                      "draws": sum(r["result"] == "draw" for r in b),
                      "losses": sum(r["result"] == "loss" for r in b),
                      "score": round(sum(SCORE[r["result"]] for r in b) / len(b), 3) if b else None})
    # challenges
    verdicts = Counter(c["verdict"] for c in chall)
    per_day = defaultdict(lambda: {"asked": 0, "accepted": 0})
    for c in chall:
        d = per_day[c["utc"][:10]]
        d["asked"] += 1
        if c["verdict"] == "accepted":
            d["accepted"] += 1
    days = [{"date": k, **v} for k, v in sorted(per_day.items())]
    by_bot = defaultdict(lambda: {"asked": 0, "accepted": 0, "rating": 0, "verdicts": Counter()})
    for c in chall:
        b = by_bot[c["opponent"]]
        b["asked"] += 1
        b["accepted"] += c["verdict"] == "accepted"
        b["rating"] = int(c["opp_rating"] or 0) or b["rating"]
        b["verdicts"][c["verdict"]] += 1
    never = sorted(((k, v) for k, v in by_bot.items() if v["accepted"] == 0), key=lambda kv: -kv[1]["asked"])
    decliners = [{"bot": k, "rating": v["rating"], "asked": v["asked"], "how": v["verdicts"].most_common(1)[0][0]}
                 for k, v in never[:15]]
    declined_reasons = Counter((c["detail"] or "").split(":")[0].strip()[:40] for c in chall if c["verdict"] == "declined")
    bots_asked = len(by_bot)
    bots_played = len({r["opponent"] for r in rows})
    accepted_bot_ratings = [v["rating"] for v in by_bot.values() if v["accepted"]]
    refused_bot_ratings = [v["rating"] for v in by_bot.values() if not v["accepted"] and v["rating"]]
    med = lambda xs: sorted(xs)[len(xs) // 2] if xs else None
    summary = {
        "games": n, "wins": wins, "draws": draws, "losses": losses,
        "score": round(sum(SCORE[r["result"]] for r in rows) / n, 3),
        "rating_start": rows[0]["before"], "rating_now": rows[-1]["after"],
        "rating_peak": max(r["after"] for r in rows),
        "strongest_beaten": max(beaten), "strongest_faced": max(r["opp"] for r in rows),
        "median_opp": med([r["opp"] for r in rows]),
        "first": rows[0]["date"], "last": rows[-1]["date"],
        "challenges": len(chall), "accepted": verdicts.get("accepted", 0),
        "declined": verdicts.get("declined", 0), "no_answer": verdicts.get("no answer", 0),
        "refused_400": verdicts.get("refused 400", 0), "refused_429": verdicts.get("refused 429", 0),
        "accept_rate": round(verdicts.get("accepted", 0) / len(chall), 4),
        "bots_asked": bots_asked, "bots_played": bots_played, "bots_never": len(never),
        "median_rating_accepted_bots": med(accepted_bot_ratings),
        "median_rating_refusing_bots": med(refused_bot_ratings),
        "challenge_first": chall[0]["utc"][:10], "challenge_last": chall[-1]["utc"][:10],
        "declined_reasons": declined_reasons.most_common(5),
    }
    # agreement with lichess.py's own status line
    py = VENV if os.path.exists(VENV) else sys.executable
    out = subprocess.run([py, os.path.join(ROOT, "bin", "lichess.py"), "status"], capture_output=True, text=True).stdout
    want = ("Lichess: %d rated games, %d won, %d drawn, %d lost; blitz rating %d; strongest opponent beaten %d"
            % (n, wins, draws, losses, summary["rating_now"], summary["strongest_beaten"]))
    if want not in out:
        sys.exit("ladder-page: disagrees with lichess.py status\n  mine: %s\n  lichess.py: %s" % (want, out.strip()))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"summary": summary, "bands": bands, "days": days, "decliners": decliners, "games": rows}, f, indent=1)
    print("ladder-page: %d games (%dW %dD %dL), rating %d, %d challenges, %d accepted (%.1f%%), %d bots asked, %d never said yes; agrees with lichess.py; wrote %s"
          % (n, wins, draws, losses, summary["rating_now"], len(chall), summary["accepted"], 100 * summary["accept_rate"],
             bots_asked, len(never), OUT))


if __name__ == "__main__":
    main()
