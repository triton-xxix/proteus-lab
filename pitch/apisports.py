#!/usr/bin/env python3
"""API-Football (api-sports.io) as a third fixtures source for the Pitch, with bookmaker odds.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/pitch/apisports.py fetch
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/pitch/apisports.py check

The key is Luke's ("Api-Sports" in his vault, named for Proteus 30 Sep 2026). It is on the Free plan,
checked 30 Sep: 100 requests a day; seasons 2022 to 2024 only when asked by league and season; but
asked by date it returns live, current fixtures and odds for yesterday, today and tomorrow. So this
is a one-day-ahead feed: `fetch` pulls today and tomorrow, keeps the nine Pitch leagues, adds each
fixture's average 1X2 and over/under 2.5 odds across bookmakers, maps team names onto football-data's
names, and writes cache/apisports.json. `data.load_fixtures()` reads it after football-data and before
fixturedownload. `check` prints what the plan allows today without spending more than three requests.
"""
import difflib
import json
import os
import statistics as st
import sys
from datetime import datetime, timedelta, timezone

import requests

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = HERE + "/cache/apisports.json"
NAMES = HERE + "/apisports-names.json"
B = "https://v3.football.api-sports.io"
# Checked by hand 30 Sep 2026 against football-data's names in the Pitch's results.
OVERRIDES = {"SP1|Athletic Club": "Ath Bilbao", "SP1|Atletico Madrid": "Ath Madrid", "D1|Borussia Mönchengladbach": "M'gladbach",
             "D1|FSV Mainz 05": "Mainz", "D1|Eintracht Frankfurt": "Ein Frankfurt", "F1|Paris Saint Germain": "Paris SG",
             "F1|Stade Brestois 29": "Brest", "F1|Saint Etienne": "St Etienne", "P1|Vitória SC": "Guimaraes",
             "P1|Sporting CP": "Sp Lisbon", "P1|SC Braga": "Sp Braga", "N1|Fortuna Sittard": "For Sittard",
             "E1|Stoke City": "Stoke", "E0|Manchester United": "Man United", "E0|Manchester City": "Man City",
             "E0|Nottingham Forest": "Nott'm Forest", "E0|Wolverhampton Wanderers": "Wolves", "SC0|Heart Of Midlothian": "Hearts"}
LEAGUE_DIV = {39: "E0", 40: "E1", 140: "SP1", 78: "D1", 135: "I1", 61: "F1", 88: "N1", 94: "P1", 179: "SC0"}

def _vault():
    """bin/secrets.py by file path: on sys.path it would shadow the standard library's secrets module,
    which numpy imports (found 30 Sep 2026)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("proteus_secrets", "/Users/triton/PROTEUS/bin/secrets.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod



def headers():
    vault = _vault()
    return {"x-apisports-key": vault.get("Api-Sports", vault="Tritons World")}


def get(path, h, **params):
    r = requests.get(B + path, headers=h, params=params, timeout=30)
    d = r.json()
    return d.get("errors"), d.get("response") or [], r.headers.get("x-ratelimit-requests-remaining")


def team_names():
    """football-data's team names per Div, from the results the Pitch already holds."""
    sys.path.insert(0, HERE)
    import data as D
    res = D.load_results(D.LEAGUES)
    out = {}
    for div, g in res.groupby("Div"):
        out[div] = sorted(set(g["HomeTeam"]) | set(g["AwayTeam"]))
    return out


def mapper():
    known = json.load(open(NAMES)) if os.path.exists(NAMES) else {}
    known = {k: v for k, v in known.items() if v is not None}   # retry misses each run
    known.update(OVERRIDES)
    names = team_names()

    def m(div, name):
        key = "%s|%s" % (div, name)
        if key in known:
            return known[key]
        cands = names.get(div, [])
        simple = lambda x: " ".join(w for w in x.lower().replace(".", "").replace("-", " ").split()
                                    if w not in ("fc", "afc", "sc", "cf", "ac", "as", "vfl", "vfb", "sv", "fsv", "1", "1899", "cp"))
        s_name = simple(name)
        hit = next((c for c in cands if simple(c) == s_name), None)
        if hit is None:                                   # "Stoke" inside "Stoke City", "Freiburg" inside "SC Freiburg"
            inside = [c for c in cands if simple(c) and (simple(c) in s_name.split() or simple(c) == s_name.split()[0])]
            hit = inside[0] if len(inside) == 1 else None
        if hit is None:
            best = difflib.get_close_matches(s_name, [simple(c) for c in cands], n=1, cutoff=0.8)
            hit = next((c for c in cands if simple(c) == best[0]), None) if best else None
        known[key] = hit      # None recorded too, so a miss is visible and can be fixed by hand
        return hit
    return m, known


def avg_odds(resp):
    h, d, a, o, u = [], [], [], [], []
    for bk in (resp[0]["bookmakers"] if resp else []):
        for bet in bk["bets"]:
            vals = {v["value"]: float(v["odd"]) for v in bet["values"]}
            if bet["name"] == "Match Winner" and {"Home", "Draw", "Away"} <= set(vals):
                h.append(vals["Home"]); d.append(vals["Draw"]); a.append(vals["Away"])
            if bet["name"] == "Goals Over/Under" and "Over 2.5" in vals and "Under 2.5" in vals:
                o.append(vals["Over 2.5"]); u.append(vals["Under 2.5"])
    f = lambda x: round(st.mean(x), 3) if x else None
    return {"AvgH": f(h), "AvgD": f(d), "AvgA": f(a), "Avg>2.5": f(o), "Avg<2.5": f(u), "bookmakers": len(resp[0]["bookmakers"]) if resp else 0}


def fetch():
    h = headers(); m, known = mapper()
    today = datetime.now(timezone.utc).date()
    rows, unmapped, left = [], [], None
    for day in (today, today + timedelta(days=1)):
        err, fx, left = get("/fixtures", h, date=day.isoformat())
        if err:
            print("fixtures %s: %s" % (day, err)); continue
        for f in fx:
            div = LEAGUE_DIV.get(f["league"]["id"])
            if not div or f["fixture"]["status"]["short"] not in ("NS", "TBD"):
                continue
            hn, an = m(div, f["teams"]["home"]["name"]), m(div, f["teams"]["away"]["name"])
            if not hn or not an:
                unmapped.append("%s: %s v %s" % (div, f["teams"]["home"]["name"], f["teams"]["away"]["name"])); continue
            err, od, left = get("/odds", h, fixture=f["fixture"]["id"])
            ko = datetime.fromisoformat(f["fixture"]["date"]).astimezone(timezone.utc)
            rows.append({"Div": div, "fixture_id": f["fixture"]["id"], "kickoff_utc": ko.strftime("%Y-%m-%dT%H:%M:%SZ"),
                         "HomeTeam": hn, "AwayTeam": an, "api_home": f["teams"]["home"]["name"], "api_away": f["teams"]["away"]["name"],
                         **avg_odds(od)})
    json.dump(known, open(NAMES, "w"), indent=1, sort_keys=True)
    json.dump({"fetched": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "rows": rows, "unmapped": unmapped},
              open(CACHE, "w"), indent=1)
    print("apisports: %d fixtures in the nine leagues for today and tomorrow, %d with odds, %d unmapped; requests left today %s"
          % (len(rows), sum(1 for r in rows if r["AvgH"]), len(unmapped), left))
    for u in unmapped:
        print("  unmapped", u)


def check():
    h = headers()
    err, st_, left = get("/status", h)
    print("plan:", json.dumps(st_.get("subscription") if isinstance(st_, dict) else st_), "requests left", left)
    err, live, left = get("/fixtures", h, live="all")
    print("live now:", len(live), "matches;", "errors", err)
    err, fx, left = get("/fixtures", h, league=39, season=datetime.now().year)
    print("current season by league:", len(fx), "errors", err)


if __name__ == "__main__":
    {"fetch": fetch, "check": check}[sys.argv[1] if len(sys.argv) > 1 else "fetch"]()
