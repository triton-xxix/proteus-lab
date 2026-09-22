#!/usr/bin/env python3
"""The Pitch: score committed predictions against results and closing odds.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/pitch/score.py

For each unscored row whose match now has a result in the cache: result, goals, Brier score on 1X2
(sum of squared errors over the three outcomes, so 0 is perfect and a coin flip scores about 0.67 on
three outcomes; bin/score.py reports the mean), the market's Brier on the same match from the
closing average odds (AvgCH/AvgCD/AvgCA) with overround removed, closing-line value for the backed
side (model probability minus closing implied probability), and paper P&L. Rows committed after
kickoff are marked result=LATE and excluded from every average.
"""
import csv
import os
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D  # noqa: E402

ROOT = "/Users/triton/PROTEUS/"
PRED = ROOT + "pitch/PREDICTIONS.csv"
FIELDS = ["id", "committed_at", "kickoff_utc", "competition", "home", "away", "p_home", "p_draw", "p_away", "p_over25",
          "market_home", "market_draw", "market_away", "market_over25", "backed", "stake_gbp", "odds_taken",
          "result", "home_goals", "away_goals", "brier", "market_brier", "clv", "pnl_gbp"]


def implied(oh, od, oa):
    try:
        ih, id_, ia = 1 / float(oh), 1 / float(od), 1 / float(oa)
        s = ih + id_ + ia
        return ih / s, id_ / s, ia / s
    except Exception:
        return None


def brier(p, outcome):
    o = {"H": (1, 0, 0), "D": (0, 1, 0), "A": (0, 0, 1)}[outcome]
    return round(sum((pi - oi) ** 2 for pi, oi in zip(p, o)), 4)


def main():
    if not os.path.exists(PRED):
        print("no predictions"); return
    rows = list(csv.DictReader(open(PRED)))
    res = D.load_results()
    if res.empty:
        print("no results"); return
    res["key"] = res["Date"].dt.strftime("%Y-%m-%d") + "|" + res["HomeTeam"] + "|" + res["AwayTeam"]
    by_key = {r["key"]: r for _, r in res.iterrows()}
    scored = 0
    for r in rows:
        if r.get("result"):
            continue
        if r["committed_at"] >= r["kickoff_utc"]:
            r["result"] = "LATE"; continue
        # kickoff is UTC; the CSV date is the local match date. Try the UTC date and the day after.
        d = r["kickoff_utc"][:10]
        m = by_key.get("%s|%s|%s" % (d, r["home"], r["away"]))
        if m is None:
            import datetime as dt
            d2 = (dt.date.fromisoformat(d) + dt.timedelta(days=1)).isoformat()
            m = by_key.get("%s|%s|%s" % (d2, r["home"], r["away"]))
        if m is None:
            continue
        hg, ag = int(m["FTHG"]), int(m["FTAG"])
        outcome = "H" if hg > ag else ("A" if ag > hg else "D")
        p = (float(r["p_home"]), float(r["p_draw"]), float(r["p_away"]))
        r["result"], r["home_goals"], r["away_goals"] = outcome, hg, ag
        r["brier"] = brier(p, outcome)
        closing = implied(m.get("AvgCH"), m.get("AvgCD"), m.get("AvgCA")) or implied(m.get("AvgH"), m.get("AvgD"), m.get("AvgA"))
        if closing:
            r["market_brier"] = brier(closing, outcome)
        if r.get("backed"):
            side = {"home": 0, "draw": 1, "away": 2}[r["backed"]]
            if closing:
                r["clv"] = round(p[side] - closing[side], 4)
            won = {"home": "H", "draw": "D", "away": "A"}[r["backed"]] == outcome
            st = float(r["stake_gbp"] or 0); od = float(r["odds_taken"] or 0)
            r["pnl_gbp"] = round(st * (od - 1), 2) if won else round(-st, 2)
        else:
            r["pnl_gbp"] = 0.0
        scored += 1
    with open(PRED, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS); w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    print("scored", scored, "of", len(rows))


if __name__ == "__main__":
    main()
