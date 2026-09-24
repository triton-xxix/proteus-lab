#!/usr/bin/env python3
"""P-0010: do Wikipedia pageview spikes for Premier League clubs precede or follow results?

Keyless Wikimedia REST pageviews (en.wikipedia, all-access, user agents only), daily, 1 Aug 2025 to
yesterday, for the 20 clubs of 2025-26. Joined to every E0 match of 2025-26 and 2026-27 so far from
the desk's football-data cache, with the devigged average closing price as the expectation.

Abnormal views on day t = log(views_t) minus log of the club's median over the 28 days ending 7 days
before the match (so the baseline never includes the match build-up). Measured:
- pre: mean abnormal views over the 3 days before kickoff;
- post: abnormal views on the day after the match;
- surprise: points won minus expected points from the closing price.
Precede: corr(pre, surprise). Follow: post by result and corr(post, surprise).
Output: REPORT.md and views.csv here.
"""
import json, time, urllib.request, urllib.parse, sys
from datetime import date, timedelta
import numpy as np, pandas as pd
sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D

HERE = "/Users/triton/PROTEUS/experiments/2026-09-24-P-0010/"
TITLES = {"Arsenal": "Arsenal_F.C.", "Aston Villa": "Aston_Villa_F.C.", "Bournemouth": "AFC_Bournemouth", "Brentford": "Brentford_F.C.",
          "Brighton": "Brighton_&_Hove_Albion_F.C.", "Burnley": "Burnley_F.C.", "Chelsea": "Chelsea_F.C.", "Crystal Palace": "Crystal_Palace_F.C.",
          "Everton": "Everton_F.C.", "Fulham": "Fulham_F.C.", "Leeds": "Leeds_United_F.C.", "Liverpool": "Liverpool_F.C.",
          "Man City": "Manchester_City_F.C.", "Man United": "Manchester_United_F.C.", "Newcastle": "Newcastle_United_F.C.",
          "Nott'm Forest": "Nottingham_Forest_F.C.", "Sunderland": "Sunderland_A.F.C.", "Tottenham": "Tottenham_Hotspur_F.C.",
          "West Ham": "West_Ham_United_F.C.", "Wolves": "Wolverhampton_Wanderers_F.C."}
START, END = "20250801", (date.today() - timedelta(days=1)).strftime("%Y%m%d")
UA = {"User-Agent": "proteus-probe/0.1 (research; github.com/triton-xxix/proteus-lab)"}

views, calls, errs, t_all = {}, 0, [], time.time()
for team, title in TITLES.items():
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/%s/daily/%s/%s" % (
        urllib.parse.quote(title, safe=""), START, END)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            items = json.load(r)["items"]
        calls += 1
        views[team] = pd.Series({pd.Timestamp(i["timestamp"][:8]): i["views"] for i in items})
    except Exception as e:
        errs.append((team, str(e)[:80]))
    time.sleep(1.0)  # first run without a pause drew 429 on calls 15 to 20 (about 14 in 8 s)
print("pageview calls", calls, "errors", errs, "%.1fs" % (time.time() - t_all))
V = pd.DataFrame(views).sort_index()
V.to_csv(HERE + "views.csv")

res = D.load_results(["E0"])
res = res[res["Date"] >= "2025-08-01"].dropna(subset=["FTHG", "FTAG", "AvgCH", "AvgCD", "AvgCA"])
inv = 1 / res[["AvgCH", "AvgCD", "AvgCA"]].to_numpy(float); P = inv / inv.sum(axis=1, keepdims=True)
LV = np.log(V.clip(lower=1))
rows = []
for (_, m), p in zip(res.iterrows(), P):
    d = pd.Timestamp(m["Date"].date())
    for side, team, xp, pts in (("home", m["HomeTeam"], 3 * p[0] + p[1], 3 * (m["FTHG"] > m["FTAG"]) + (m["FTHG"] == m["FTAG"])),
                                ("away", m["AwayTeam"], 3 * p[2] + p[1], 3 * (m["FTAG"] > m["FTHG"]) + (m["FTHG"] == m["FTAG"]))):
        if team not in LV.columns: continue
        s = LV[team]
        base = s[(s.index > d - timedelta(days=35)) & (s.index <= d - timedelta(days=7))]
        pre = s[(s.index >= d - timedelta(days=3)) & (s.index < d)]
        post = s.get(d + timedelta(days=1))
        if len(base) < 20 or len(pre) < 3 or post is None or np.isnan(post): continue
        b = base.median()
        rows.append({"date": d.date(), "team": team, "side": side, "pts": int(pts), "xpts": xp, "surprise": pts - xp,
                     "pre": pre.mean() - b, "matchday": s.get(d, np.nan) - b, "post": post - b})
M = pd.DataFrame(rows)
M.to_csv(HERE + "matches.csv", index=False)


def ci(x, y):
    r = np.corrcoef(x, y)[0, 1]; n = len(x); z = np.arctanh(r); se = 1 / np.sqrt(n - 3)
    return r, np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)


L = ["# P-0010: Wikipedia pageviews and Premier League results", "",
     "%d club pages, %d pageview calls in %.1fs, errors %s. %d team-matches from 1 Aug 2025 to %s." % (len(V.columns), calls, time.time() - t_all, errs, len(M), M["date"].max()), ""]
r, lo, hi = ci(M["pre"], M["surprise"])
L.append("**Precede.** corr(abnormal views over the 3 days before, points minus closing-price expectation) = %+.3f (95%% CI %+.3f to %+.3f)." % (r, lo, hi))
M["preq"] = pd.qcut(M["pre"], 5, labels=False)
L.append(""); L.append("| pre-match attention quintile | n | mean abnormal log views | mean surprise (points) |"); L.append("|---|---|---|---|")
for q, g in M.groupby("preq"):
    L.append("| %d | %d | %+.3f | %+.3f |" % (q + 1, len(g), g["pre"].mean(), g["surprise"].mean()))
r2, lo2, hi2 = ci(M["post"], M["surprise"])
L.append(""); L.append("**Follow.** corr(abnormal views the day after, surprise) = %+.3f (95%% CI %+.3f to %+.3f)." % (r2, lo2, hi2))
L.append(""); L.append("| result | n | matchday abnormal | day-after abnormal (log) | day-after as a multiple |"); L.append("|---|---|---|---|---|")
for pts, g in M.groupby("pts"):
    L.append("| %s | %d | %+.3f | %+.3f | x%.2f |" % ({3: "win", 1: "draw", 0: "loss"}[pts], len(g), g["matchday"].mean(), g["post"].mean(), np.exp(g["post"].mean())))
big = M[M["surprise"].abs() >= 2]
L.append(""); L.append("Big surprises (|points - expected| >= 2, n=%d): day-after abnormal %+.3f for shock wins, %+.3f for shock losses." % (
    len(big), big[big["surprise"] > 0]["post"].mean(), big[big["surprise"] < 0]["post"].mean()))
L.append("Median daily views across clubs: " + ", ".join("%s %d" % (t, v) for t, v in V.median().sort_values(ascending=False).head(5).items()) + ", lowest " +
         ", ".join("%s %d" % (t, v) for t, v in V.median().sort_values().head(3).items()) + ".")
open(HERE + "REPORT.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
