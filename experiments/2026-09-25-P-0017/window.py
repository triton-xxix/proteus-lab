#!/usr/bin/env python3
"""P-0017 part 2: where does the 429 start, and how long until it clears? Small and capped.
Burst: up to 24 one-day requests for club pages at 0.5 s spacing, stopping at the first 429. Then one
request every 15 s until a 200 (at most 12, so 3 minutes). Output: window.csv here.
"""
import time, urllib.parse, urllib.request
import pandas as pd

HERE = "/Users/triton/PROTEUS/experiments/2026-09-25-P-0017/"
TITLES = ["Arsenal_F.C.", "Aston_Villa_F.C.", "AFC_Bournemouth", "Brentford_F.C.", "Brighton_&_Hove_Albion_F.C.", "Burnley_F.C.",
          "Chelsea_F.C.", "Crystal_Palace_F.C.", "Everton_F.C.", "Fulham_F.C.", "Leeds_United_F.C.", "Liverpool_F.C.",
          "Manchester_City_F.C.", "Manchester_United_F.C.", "Newcastle_United_F.C.", "Nottingham_Forest_F.C.", "Sunderland_A.F.C.",
          "Tottenham_Hotspur_F.C.", "West_Ham_United_F.C.", "Wolverhampton_Wanderers_F.C.", "Leicester_City_F.C.", "Ipswich_Town_F.C.",
          "Southampton_F.C.", "Luton_Town_F.C."]
UA = {"User-Agent": "proteus-probe/0.1 (research; github.com/triton-xxix/proteus-lab)"}
log, t0 = [], time.time()


def call(title, phase):
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/%s/daily/20260920/20260920" % urllib.parse.quote(title, safe="")
    rec = {"n": len(log) + 1, "phase": phase, "t": round(time.time() - t0, 1), "title": title}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            rec["status"] = r.status
    except urllib.error.HTTPError as e:
        rec["status"] = e.code
        rec["retry_after"] = e.headers.get("retry-after")
        rec["body"] = e.read()[:120].decode("utf-8", "replace")
    except Exception as e:
        rec["status"] = None
        rec["body"] = str(e)[:120]
    log.append(rec)
    print(rec, flush=True)
    return rec["status"]


hit = None
for i, t in enumerate(TITLES):
    if call(t, "burst") == 429:
        hit = i + 1
        break
    time.sleep(0.5)
if hit:
    for k in range(12):
        time.sleep(15)
        if call(TITLES[0], "recover") == 200:
            break
pd.DataFrame(log).to_csv(HERE + "window.csv", index=False)
print("first 429 at call", hit, "of the burst; total calls", len(log), "in %.0fs" % (time.time() - t0))
