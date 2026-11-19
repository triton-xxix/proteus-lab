"""P-0492: which Lichess bots online now are worth a morning challenge?

1. api/bot/online (ndjson, nb=500): every bot online now.
2. Keep those with a non-provisional blitz rating within 300 of mine.
3. Split by whether they are in games/lichess/GAMES.csv (played) and what CHALLENGES.csv says about
   them (last verdict on file).
4. For the unplayed ones, api/user/<name>/rating-history: was there a blitz point in the last 7 days?

    python3 census.py

Keyless, read only, standard library. Sends no challenge.
"""
import csv, json, sys, time, urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path("/Users/triton/PROTEUS")
GAMES = ROOT / "games" / "lichess" / "GAMES.csv"
CHALL = ROOT / "games" / "lichess" / "CHALLENGES.csv"
HALT = ROOT / "HALT"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) proteus-census/0.1"
WINDOW = 300
MAX_HISTORY = 45


def get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def main():
    if HALT.exists():
        print("HALT")
        return 1
    games = list(csv.DictReader(GAMES.open()))
    played = {g["opponent"].lower() for g in games}
    mine = int([g for g in games if g.get("my_rating_after")][-1]["my_rating_after"])
    last_verdict, declines = {}, {}
    for c in csv.DictReader(CHALL.open()):
        name = c["opponent"].lower()
        last_verdict[name] = c["verdict"]
        if c["verdict"] != "accepted":
            declines[name] = declines.get(name, 0) + 1

    raw = get("https://lichess.org/api/bot/online?nb=500", "application/x-ndjson")
    bots = [json.loads(line) for line in raw.splitlines() if line.strip()]
    rated = []
    for b in bots:
        bl = (b.get("perfs") or {}).get("blitz") or {}
        if "rating" in bl:
            rated.append({"name": b["id"], "blitz": bl["rating"], "games": bl.get("games", 0),
                          "prov": bool(bl.get("prov")), "disabled": bool(b.get("disabled")),
                          "tos": bool(b.get("tosViolation"))})
    near = [b for b in rated if abs(b["blitz"] - mine) <= WINDOW]
    settled = [b for b in near if not b["prov"] and not b["tos"]]
    # busiest first: P-0290 found games played is what separates bots that accept
    unplayed = sorted([b for b in settled if b["name"] not in played], key=lambda b: -b["games"])
    today = datetime.now(timezone.utc).date()
    for b in unplayed[:MAX_HISTORY]:
        b["challenged_before"] = b["name"] in last_verdict
        b["last_verdict"] = last_verdict.get(b["name"])
        b["refusals_on_file"] = declines.get(b["name"], 0)
        # rating-history answers 200 with an empty list for bots (first run, 45 of 45), so the
        # last rated blitz game from the games export stands in for "a blitz point in 7 days".
        try:
            raw_g = get("https://lichess.org/api/games/user/" + b["name"] + "?max=1&rated=true&perfType=blitz&moves=false",
                        "application/x-ndjson")
            line = next((ln for ln in raw_g.splitlines() if ln.strip()), None)
            if line:
                g = json.loads(line)
                last = datetime.fromtimestamp(g["lastMoveAt"] / 1000, timezone.utc).date()
                b["last_rated_blitz"] = last.isoformat()
                b["days_since_blitz"] = (today - last).days
                opp = [p for p in g.get("players", {}).values() if (p.get("user") or {}).get("id") != b["name"]]
                if opp and opp[0].get("user"):
                    b["last_opp_is_bot"] = opp[0]["user"].get("title") == "BOT"
                    b["last_opp_rating"] = opp[0].get("rating")
            else:
                b["history_error"] = "no rated blitz game returned"
        except Exception as e:
            b["history_error"] = str(e)[:100]
        print(json.dumps(b), flush=True)
        time.sleep(1.2)

    checked = unplayed[:MAX_HISTORY]
    active = [b for b in checked if b.get("days_since_blitz", 999) <= 7]
    fresh = [b for b in active if not b["challenged_before"]]
    summary = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "my_blitz": mine,
        "bots_online": len(bots),
        "with_blitz_rating": len(rated),
        "within_300_any": len(near),
        "within_300_settled": len(settled),
        "of_those_played": len(settled) - len(unplayed),
        "of_those_unplayed": len(unplayed),
        "unplayed_checked": len(checked),
        "unplayed_active_7d": len(active),
        "unplayed_active_never_challenged": len(fresh),
        "unplayed_active_challenged_and_refused": len(active) - len(fresh),
        "unplayed_active_last_opp_was_bot": sum(1 for b in active if b.get("last_opp_is_bot")),
        "fresh_last_opp_was_bot": sum(1 for b in fresh if b.get("last_opp_is_bot")),
        "history_errors": sum(1 for b in checked if "history_error" in b),
        "try_these": sorted(((b["name"], b["blitz"], b["games"], b.get("last_opp_is_bot")) for b in fresh), key=lambda t: -t[2]),
        "refused_before": sorted((b["name"], b["blitz"], b["last_verdict"], b["refusals_on_file"]) for b in active if b["challenged_before"]),
        "online_blitz_quartiles": [sorted(b["blitz"] for b in rated)[int(len(rated) * q)] for q in (0.25, 0.5, 0.75)] if rated else None,
        "online_above_2000": sum(1 for b in rated if b["blitz"] >= 2000 and not b["prov"]),
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "unplayed": checked}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
