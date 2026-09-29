"""The judgement book, two columns: blind and anchored.

  fixtures            list upcoming fixtures not yet in the book (The Odds API events, no odds, no quota)
  blind  FILE.json    append rows from my blind calls, made before any price is seen; stamps blind_committed_at
  odds                pull the market for rows that have none; stamps odds_seen_at
  anchor FILE.json    fill anchored calls (made after the price) on rows by id; stamps committed_at

The commit order is the proof: a blind row is only counted if its blind commit precedes odds_seen_at.
JSON for blind: [{"home","away","kickoff_utc","p":[h,d,a],"over25","call","note"}]
JSON for anchor: [{"id","p":[h,d,a],"over25","call","note"}]
Key for The Odds API comes from 1Password at run time and is never written.
"""
import csv, json, os, subprocess, sys, datetime, requests

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "JUDGEMENT.csv")
SPORTS = ("soccer_uefa_nations_league",)
COMP = {"soccer_uefa_nations_league": "UEFA Nations League"}
FIELDS = ["id", "committed_at", "kickoff_utc", "competition", "home", "away", "p_home", "p_draw", "p_away", "p_over25",
          "market_home", "market_draw", "market_away", "market_over25", "call", "biggest_lean", "lean_size", "note",
          "result", "home_goals", "away_goals", "brier", "market_brier",
          "blind_home", "blind_draw", "blind_away", "blind_over25", "blind_call", "blind_note", "blind_committed_at",
          "odds_seen_at", "blind_brier"]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def key():
    """The Odds API key: service account first (works in a scheduled run), desktop op as fallback."""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(HERE), "bin"))
        import secrets as proteus_secrets
        k = proteus_secrets.get("The Odds API")
    except Exception:
        k = subprocess.run(["op", "item", "get", "The Odds API", "--vault", "PROTEUS", "--fields", "label=credential", "--reveal"],
                           capture_output=True, text=True).stdout.strip()
    if len(k) != 32:
        sys.exit("The Odds API key not readable from 1Password")
    return k


def load():
    if not os.path.exists(BOOK):
        return []
    with open(BOOK, newline="", encoding="utf-8") as f:
        return [{k: r.get(k, "") for k in FIELDS} for r in csv.DictReader(f)]


def save(rows):
    with open(BOOK, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def events(k):
    out = []
    for s in SPORTS:
        r = requests.get("https://api.the-odds-api.com/v4/sports/%s/events" % s, params={"apiKey": k}, timeout=30)
        r.raise_for_status()
        for e in r.json():
            out.append((e["commence_time"], e["home_team"], e["away_team"], s))
    return out


def cmd_fixtures():
    rows = load()
    have = {(r["home"], r["away"], r["kickoff_utc"]) for r in rows}
    n = 0
    for ko, h, a, s in sorted(events(key())):
        if (h, a, ko) not in have:
            print(ko, h, "v", a)
            n += 1
    print(n, "fixtures not in the book. No odds were requested.")


def cmd_blind(path):
    rows = load()
    calls = json.load(open(path))
    ev = {(h, a): ko for ko, h, a, s in events(key())}
    comp = {(h, a): COMP[s] for ko, h, a, s in events(key())}
    nxt = max([int(r["id"][2:]) for r in rows] + [0]) + 1
    stamp = now()
    for c in calls:
        kk = (c["home"], c["away"])
        if kk not in ev:
            sys.exit("not an upcoming fixture: %s v %s" % kk)
        if any(r["home"] == c["home"] and r["away"] == c["away"] and r["kickoff_utc"] == ev[kk] for r in rows):
            sys.exit("already in the book: %s v %s" % kk)
        p = c["p"]
        if abs(sum(p) - 1) > 0.011:
            sys.exit("probabilities do not sum to 1: %s v %s" % kk)
        rows.append({**{k: "" for k in FIELDS}, "id": "J-%04d" % nxt, "kickoff_utc": ev[kk], "competition": comp[kk],
                     "home": c["home"], "away": c["away"], "blind_home": p[0], "blind_draw": p[1], "blind_away": p[2],
                     "blind_over25": c["over25"], "blind_call": c["call"], "blind_note": c["note"], "blind_committed_at": stamp})
        nxt += 1
    save(rows)
    print(len(calls), "blind rows added at", stamp, "- commit now, before pulling odds")


def cmd_odds():
    rows = load()
    k = key()
    need = [r for r in rows if not r["market_home"] and r["kickoff_utc"] > now()]
    if not need:
        print("no rows need odds"); return
    stamp = now()
    filled = 0
    for s in SPORTS:
        r = requests.get("https://api.the-odds-api.com/v4/sports/%s/odds" % s,
                         params={"apiKey": k, "regions": "uk", "markets": "h2h,totals", "oddsFormat": "decimal"}, timeout=30)
        r.raise_for_status()
        print(s, "quota used", r.headers.get("x-requests-used"), "remaining", r.headers.get("x-requests-remaining"))
        raw = os.path.join(HERE, "cache")
        os.makedirs(raw, exist_ok=True)
        open(os.path.join(raw, "odds-%s-%s.json" % (s, stamp.replace(":", ""))), "w").write(r.text)
        for e in r.json():
            for row in need:
                if row["home"] != e["home_team"] or row["away"] != e["away_team"] or row["market_home"]:
                    continue
                ph = pd = pa = n = 0; tot = {}
                for b in e["bookmakers"]:
                    for m in b["markets"]:
                        if m["key"] == "h2h":
                            o = {x["name"]: x["price"] for x in m["outcomes"]}
                            inv = {kk: 1 / v for kk, v in o.items()}; ss = sum(inv.values())
                            ph += inv[e["home_team"]] / ss; pd += inv["Draw"] / ss; pa += inv[e["away_team"]] / ss; n += 1
                        if m["key"] == "totals":
                            for x in m["outcomes"]:
                                if x.get("point") == 2.5:
                                    tot.setdefault(x["name"], []).append(1 / x["price"])
                if not n:
                    continue
                mo = ""
                if tot.get("Over") and tot.get("Under"):
                    ov = sum(tot["Over"]) / len(tot["Over"]); un = sum(tot["Under"]) / len(tot["Under"]); mo = round(ov / (ov + un), 3)
                row.update(market_home=round(ph / n, 3), market_draw=round(pd / n, 3), market_away=round(pa / n, 3),
                           market_over25=mo, odds_seen_at=stamp)
                filled += 1
    save(rows)
    print(filled, "rows given market lines at", stamp, "(%d books averaged per row varies)" % 0)
    for r in need:
        if r["odds_seen_at"] == stamp:
            print(r["id"], r["home"], "v", r["away"], "H %.2f D %.2f A %.2f O2.5 %s" % (r["market_home"], r["market_draw"], r["market_away"], r["market_over25"]),
                  "| blind H %s D %s A %s" % (r["blind_home"], r["blind_draw"], r["blind_away"]))


def cmd_anchor(path):
    rows = load()
    by = {r["id"]: r for r in rows}
    stamp = now()
    n = 0
    for c in json.load(open(path)):
        r = by[c["id"]]
        if r["p_home"]:
            sys.exit("%s already anchored" % c["id"])
        if not r["market_home"]:
            sys.exit("%s has no market line yet; run odds first" % c["id"])
        p = c["p"]
        if abs(sum(p) - 1) > 0.011:
            sys.exit("probabilities do not sum to 1: %s" % c["id"])
        d = {"home": p[0] - float(r["market_home"]), "draw": p[1] - float(r["market_draw"]), "away": p[2] - float(r["market_away"])}
        best = max(d, key=d.get)
        r.update(p_home=p[0], p_draw=p[1], p_away=p[2], p_over25=c["over25"], call=c["call"], note=c["note"],
                 biggest_lean=best, lean_size=round(d[best], 3), committed_at=stamp)
        n += 1
    save(rows)
    print(n, "rows anchored at", stamp, "- commit now")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "fixtures":
        cmd_fixtures()
    elif a[0] == "blind":
        cmd_blind(a[1])
    elif a[0] == "odds":
        cmd_odds()
    elif a[0] == "anchor":
        cmd_anchor(a[1])
    else:
        sys.exit(__doc__)
