#!/usr/bin/env python3
"""P-0017: fill the six clubs P-0010 lost to 429, and measure the Wikimedia pageviews quota from here.

Every call is logged with its wall time, status and the rate-limit headers. Pacing 2 s. On a 429 the
script reads Retry-After (default 30 s, capped at 90 s), sleeps, and retries the same title. Hard
caps: 40 calls, 8 minutes. Then merges with P-0010's views.csv and reruns P-0010's two headline
numbers on all 20 clubs. Output: calls.csv, views.csv, matches.csv, REPORT.md here.
"""
import json, sys, time, urllib.parse, urllib.request
from datetime import date, timedelta
import numpy as np, pandas as pd
sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D

HERE = "/Users/triton/PROTEUS/experiments/2026-09-25-P-0017/"
OLD = "/Users/triton/PROTEUS/experiments/2026-09-24-P-0010/views.csv"
MISSING = {"Newcastle": "Newcastle_United_F.C.", "Nott'm Forest": "Nottingham_Forest_F.C.", "Sunderland": "Sunderland_A.F.C.",
           "Tottenham": "Tottenham_Hotspur_F.C.", "West Ham": "West_Ham_United_F.C.", "Wolves": "Wolverhampton_Wanderers_F.C."}
START, END = "20250801", (date.today() - timedelta(days=1)).strftime("%Y%m%d")
UA = {"User-Agent": "proteus-probe/0.1 (research; github.com/triton-xxix/proteus-lab)"}
HDRS = ("retry-after", "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset", "ratelimit", "ratelimit-policy", "x-cache", "server")

log, views, t0 = [], {}, time.time()
queue = list(MISSING.items())
while queue and len(log) < 40 and time.time() - t0 < 480:
    team, title = queue[0]
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/%s/daily/%s/%s" % (
        urllib.parse.quote(title, safe=""), START, END)
    t = time.time()
    rec = {"n": len(log) + 1, "t": round(t - t0, 1), "team": team}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            rec["status"] = r.status
            rec.update({h: r.headers.get(h) for h in HDRS if r.headers.get(h)})
            items = json.load(r)["items"]
        views[team] = pd.Series({pd.Timestamp(i["timestamp"][:8]): i["views"] for i in items})
        rec["days"] = len(items)
        queue.pop(0)
        wait = 2.0
    except urllib.error.HTTPError as e:
        rec["status"] = e.code
        rec.update({h: e.headers.get(h) for h in HDRS if e.headers.get(h)})
        rec["body"] = e.read()[:160].decode("utf-8", "replace")
        try:
            wait = min(90.0, float(e.headers.get("retry-after") or 30))
        except ValueError:
            wait = 30.0
    except Exception as e:
        rec["status"] = None
        rec["body"] = str(e)[:160]
        wait = 10.0
    rec["latency"] = round(time.time() - t, 2)
    rec["slept_after"] = wait
    log.append(rec)
    print(rec, flush=True)
    time.sleep(wait)

pd.DataFrame(log).to_csv(HERE + "calls.csv", index=False)
V = pd.read_csv(OLD, index_col=0, parse_dates=True)
for team, s in views.items():
    V[team] = s
V = V.sort_index()
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
        rows.append({"date": d.date(), "team": team, "pts": int(pts), "surprise": pts - xp, "pre": pre.mean() - b, "post": post - b})
M = pd.DataFrame(rows)
M.to_csv(HERE + "matches.csv", index=False)


def ci(x, y):
    r = np.corrcoef(x, y)[0, 1]; z = np.arctanh(r); se = 1 / np.sqrt(len(x) - 3)
    return r, np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)


L = ["# P-0017 numbers", "", "%d clubs now, %d team-matches. Calls this run: %d, statuses %s, %.0fs." % (
    V.shape[1], len(M), len(log), pd.Series([c["status"] for c in log]).value_counts().to_dict(), time.time() - t0)]
L.append("Precede: r = %+.3f (CI %+.3f to %+.3f). Follow: r = %+.3f (CI %+.3f to %+.3f)." % (*ci(M["pre"], M["surprise"]), *ci(M["post"], M["surprise"])))
for pts, g in M.groupby("pts"):
    L.append("%s: n %d, day-after x%.2f" % ({3: "win", 1: "draw", 0: "loss"}[pts], len(g), np.exp(g["post"].mean())))
open(HERE + "numbers.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
