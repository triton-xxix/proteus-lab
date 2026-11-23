"""Score P-0552 (Geminids 2026 pageviews) against PREREG.md. Keyless.

Usage: python3 -I score.py OUT_JSON
Fetches en.wikipedia `Geminids` user daily views 1 Nov to 31 Dec of a year (default 2026).
With --history it saves 2023 to 2025 instead.
"""
import json, math, statistics as st, sys, urllib.request

UA = {"User-Agent": "proteus-probe/0.1 (keyless research)"}

def views(year):
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/"
           f"all-access/user/Geminids/daily/{year}1101/{year}1231")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return {x["timestamp"][:8]: x["views"] for x in json.load(r)["items"]}

def summary(year):
    by = views(year)
    nov = [v for k, v in by.items() if k[4:6] == "11"]
    base = st.median(nov)
    dec = sorted((k, v) for k, v in by.items() if k[4:6] == "12")
    peak = max(dec, key=lambda kv: kv[1])
    first10 = next((int(k[6:]) for k, v in dec if v > 10 * base), None)
    return {"year": year, "nov_median": base, "first_10x_day": first10,
            "peak_day": int(peak[0][6:]), "peak_views": peak[1], "dec_days": len(dec)}

def main():
    out = sys.argv[1]
    if "--history" in sys.argv:
        json.dump([summary(y) for y in (2023, 2024, 2025)], open(out, "w"), indent=1)
        print(open(out).read()); return
    s = summary(2026)
    p1 = {14: 0.55, 13: 0.40}.get(s["peak_day"], 0.05)
    d = s["first_10x_day"]
    p3 = 0.45 if d == 10 else 0.30 if d == 11 else 0.15 if d is not None and d <= 9 else 0.10
    hits = [s["peak_day"] == 14, d == 10]
    inside = 7000 <= s["peak_views"] <= 17000
    res = dict(s, call1_hit=hits[0], call1_logp=math.log(p1), call3_hit=hits[1],
               call3_logp=math.log(p3), call2_abs_err=abs(s["peak_views"] - 11000),
               call2_inside=inside, top_picks_hit=sum(hits),
               passed=(sum(hits) >= 1 and inside))  # two of three: call 2 counts as one when inside
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res))

main()
