#!/usr/bin/env python3
"""The Pitch: commit probabilities for upcoming E0 and E1 fixtures before kickoff.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/pitch/predict.py --upcoming [--days 8]

Refreshes data, fits Dixon-Coles as of today, and appends one row per fixture in the window that
has no row yet. Market probabilities come from the fixtures file's average odds with the overround
removed proportionally. Paper stake: quarter Kelly where model minus market exceeds 3 points on the
1X2 side, else no bet. committed_at is now (UTC); score.py excludes any row committed after kickoff.
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D  # noqa: E402
import model as M  # noqa: E402

ROOT = "/Users/triton/PROTEUS/"
PRED = ROOT + "pitch/PREDICTIONS.csv"
PARAMS = ROOT + "pitch/cache/params.json"
FIELDS = ["id", "committed_at", "kickoff_utc", "competition", "home", "away", "p_home", "p_draw", "p_away", "p_over25",
          "market_home", "market_draw", "market_away", "market_over25", "backed", "stake_gbp", "odds_taken",
          "result", "home_goals", "away_goals", "brier", "market_brier", "clv", "pnl_gbp"]
EDGE = 0.03
KELLY_FRACTION = 0.25
BANKROLL = 100.0


def implied(oh, od, oa):
    try:
        ih, id_, ia = 1 / float(oh), 1 / float(od), 1 / float(oa)
        s = ih + id_ + ia
        return round(ih / s, 4), round(id_ / s, 4), round(ia / s, 4)
    except Exception:
        return None, None, None


def implied2(o1, o2):
    try:
        a, b = 1 / float(o1), 1 / float(o2)
        return round(a / (a + b), 4)
    except Exception:
        return None


def kelly(p, odds):
    b = odds - 1
    f = (p * b - (1 - p)) / b
    return max(0.0, f)


def load_pred():
    return list(csv.DictReader(open(PRED))) if os.path.exists(PRED) else []


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--upcoming", action="store_true"); ap.add_argument("--days", type=int, default=8)
    ap.add_argument("--no-refresh", action="store_true")
    a = ap.parse_args()
    if not a.upcoming:
        ap.print_help(); return
    if not a.no_refresh:
        D.refresh()
    res = D.load_results(); fx = D.load_fixtures()
    if res.empty or fx.empty:
        print("no data"); return
    params = M.fit(res)
    os.makedirs(ROOT + "pitch/cache", exist_ok=True)
    json.dump(params, open(PARAMS, "w"))
    now = datetime.now(timezone.utc)
    existing = load_pred()
    have = {(r["kickoff_utc"][:10], r["home"], r["away"]) for r in existing}
    realised = sum(float(r["pnl_gbp"]) for r in existing if r.get("pnl_gbp"))
    bankroll = BANKROLL + realised
    new = []
    for _, f in fx.iterrows():
        ko = f["Kickoff"]
        if ko is None or ko != ko:
            continue
        ko = ko.tz_localize("Europe/London").tz_convert("UTC")
        if not (now <= ko <= now + timedelta(days=a.days)):
            continue
        key = (ko.strftime("%Y-%m-%d"), f["HomeTeam"], f["AwayTeam"])
        if key in have:
            continue
        pr = M.predict(params, f["HomeTeam"], f["AwayTeam"])
        if not pr:
            print("skip unknown team", f["HomeTeam"], f["AwayTeam"]); continue
        mh, md, ma = implied(f.get("AvgH"), f.get("AvgD"), f.get("AvgA"))
        mo = implied2(f.get("Avg>2.5"), f.get("Avg<2.5"))
        backed, stake, odds_taken = "", "", ""
        if mh is not None:
            sides = [("home", pr["p_home"], mh, f.get("AvgH")), ("draw", pr["p_draw"], md, f.get("AvgD")), ("away", pr["p_away"], ma, f.get("AvgA"))]
            best = max(sides, key=lambda s: s[1] - s[2])
            if best[1] - best[2] > EDGE:
                fr = kelly(best[1], float(best[3])) * KELLY_FRACTION
                st = round(min(bankroll * fr, 10.0), 2)
                if st >= 0.5:
                    backed, stake, odds_taken = best[0], st, best[3]
        new.append({
            "id": "P-%04d" % (len(existing) + len(new) + 1), "committed_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "kickoff_utc": ko.strftime("%Y-%m-%dT%H:%M:%SZ"), "competition": f["Div"], "home": f["HomeTeam"], "away": f["AwayTeam"],
            "p_home": pr["p_home"], "p_draw": pr["p_draw"], "p_away": pr["p_away"], "p_over25": pr["p_over25"],
            "market_home": mh, "market_draw": md, "market_away": ma, "market_over25": mo,
            "backed": backed, "stake_gbp": stake, "odds_taken": odds_taken,
        })
    with open(PRED, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if not existing and os.path.getsize(PRED) == 0:
            w.writeheader()
        for r in new:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    print("model as of", params["as_of"], "matches", params["n_matches"], "converged", params["converged"])
    print("new predictions", len(new), "backed", sum(1 for r in new if r["backed"]))


if __name__ == "__main__":
    main()
