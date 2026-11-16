#!/usr/bin/env python3
"""Build docs/ladder/data.json from the Lichess logs (Workshop, 30 Oct 2026).

Reads games/lichess/GAMES.csv (one row per rated game) and CHALLENGES.csv (one row per challenge
sent, accepted or not). Every number on the page comes from here. The games total, result split,
rating and strongest opponent beaten are checked against `lichess.py status`; exits non-zero if
they ever disagree.
"""
import csv
import datetime
import json
import re
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


REFUSAL_KINDS = [
    ("cap", "daily bot-game cap", re.compile(r"played (\d+) games against other bots today, please wait until (\d{4}-\d\d-\d\dT[\d:.]+Z)")),
    ("closed", "does not accept challenges", re.compile(r"does not accept challenges")),
    ("friends", "only accepts friends", re.compile(r"only accepts challenges from friends")),
    ("rate", "rate limit on my account (429)", re.compile(r"[Tt]oo many requests")),
]


def ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def refusal_split(chall):
    """Split Lichess's own refusals by the reason text (Workshop, 16 Nov 2026, BACKLOG ladder item).

    A cap refusal names the reset time, so a later ask to the same bot before that time was always
    going to be refused: those are counted as `wasted`. Exits if any refusal fits no kind or two."""
    refused = [c for c in chall if c["verdict"].startswith("refused")]
    kinds = {k: {"kind": k, "label": lab, "asks": 0, "bots": set(), "per_bot": Counter()} for k, lab, _ in REFUSAL_KINDS}
    cap_games, waits, resets = [], [], defaultdict(list)
    for c in refused:
        hits = [(k, rx.search(c["detail"] or "")) for k, _, rx in REFUSAL_KINDS]
        hits = [(k, m) for k, m in hits if m]
        if len(hits) != 1:
            sys.exit("ladder-page: refusal fits %d kinds: %s %s" % (len(hits), c["utc"], (c["detail"] or "")[:80]))
        k, m = hits[0]
        K = kinds[k]
        K["asks"] += 1
        K["bots"].add(c["opponent"])
        K["per_bot"][c["opponent"]] += 1
        if k == "cap":
            cap_games.append(int(m.group(1)))
            at, until = ts(c["utc"]), ts(m.group(2))
            waits.append((until - at).total_seconds() / 3600)
            resets[c["opponent"]].append((at, until))
    # asks to a capped bot after a cap refusal and before its stated reset
    wasted = 0
    for c in refused:
        if c["opponent"] in resets and c["verdict"] == "refused 400":
            at = ts(c["utc"])
            if any(a < at < u for a, u in resets[c["opponent"]]):
                wasted += 1
    capped = kinds["cap"]["bots"]
    later_yes = {c["opponent"] for c in chall if c["opponent"] in capped and c["verdict"] == "accepted"
                 and any(a < ts(c["utc"]) for a, _ in resets[c["opponent"]])}
    out = []
    for k, _, _ in REFUSAL_KINDS:
        K = kinds[k]
        days = sorted(c["utc"][:10] for c in refused if c["opponent"] in K["bots"] and [
            kk for kk, _, rx in REFUSAL_KINDS if rx.search(c["detail"] or "")] == [k])
        out.append({"kind": k, "label": K["label"], "asks": K["asks"], "bots": len(K["bots"]),
                    "first": days[0] if days else None, "last": days[-1] if days else None,
                    "top": [[b, n] for b, n in K["per_bot"].most_common(5)]})
    if sum(r["asks"] for r in out) != len(refused):
        sys.exit("ladder-page: refusal kinds do not sum to the refusals")
    med = lambda xs: sorted(xs)[len(xs) // 2] if xs else None
    return {"total": len(refused), "kinds": out,
            "cap_games_stated": dict(Counter(cap_games).most_common()),
            "cap_wait_hours_median": round(med(waits), 1) if waits else None,
            "cap_wasted": wasted, "capped_bots": len(capped), "capped_bots_later_yes": len(later_yes),
            "capped_bots_later_yes_names": sorted(later_yes)}


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
    # who accepts at what strength (Workshop, 10 Nov 2026): every challenge by the opponent's rating
    # when asked, and by its gap to mine, split by verdict. "Sent" excludes Lichess's own 400/429
    # refusals, which never reached the bot.
    VERD = ["accepted", "declined", "no answer", "refused 400", "refused 429"]
    def outcome_rows(edges, key):
        out = []
        for lo, hi, label in edges:
            cs = [c for c in chall if c["opp_rating"] and lo <= key(c) < hi]
            vc = Counter(c["verdict"] for c in cs)
            sent = sum(vc[v] for v in ("accepted", "declined", "no answer"))
            out.append({"label": label, "asked": len(cs), "bots": len({c["opponent"] for c in cs}),
                        **{v: vc.get(v, 0) for v in VERD},
                        "other": len(cs) - sum(vc.get(v, 0) for v in VERD),
                        "sent": sent, "accept_of_sent": round(vc["accepted"] / sent, 4) if sent else None})
        return out
    STR = [(0, 2000, "under 2000"), (2000, 2400, "2000 to 2399"), (2400, 2700, "2400 to 2699"),
           (2700, 2900, "2700 to 2899"), (2900, 3000, "2900 to 2999"), (3000, 9999, "3000 and up")]
    GAP = [(-9999, -500, "500+ below me"), (-500, -200, "200 to 499 below"), (-200, -50, "50 to 199 below"),
           (-50, 9999, "within 50, or above")]
    by_strength = outcome_rows(STR, lambda c: int(c["opp_rating"]))
    by_gap = outcome_rows(GAP, lambda c: int(c["opp_rating"]) - int(c["my_rating"] or c["opp_rating"]))
    rated = sum(1 for c in chall if c["opp_rating"])
    if sum(r["asked"] for r in by_strength) != rated or sum(r["asked"] for r in by_gap) != rated:
        sys.exit("ladder-page: strength or gap bands do not cover every rated challenge")
    if sum(r["accepted"] for r in by_strength) != sum(1 for c in chall if c["opp_rating"] and c["verdict"] == "accepted"):
        sys.exit("ladder-page: strength bands lose an accepted challenge")
    refusals = refusal_split(chall)
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
        json.dump({"summary": summary, "bands": bands, "days": days, "decliners": decliners,
                   "by_strength": by_strength, "by_gap": by_gap, "challenges_rated": rated,
                   "refusals": refusals, "games": rows}, f, indent=1)
    print("ladder-page: %d games (%dW %dD %dL), rating %d, %d challenges, %d accepted (%.1f%%), %d bots asked, %d never said yes; agrees with lichess.py; wrote %s"
          % (n, wins, draws, losses, summary["rating_now"], len(chall), summary["accepted"], 100 * summary["accept_rate"],
             bots_asked, len(never), OUT))


if __name__ == "__main__":
    main()
