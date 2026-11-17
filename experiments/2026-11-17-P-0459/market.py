"""P-0459: did the Polymarket Munich high-temperature market already price the low-cloud warm miss?

For each daily event 1 to 16 Nov 2026 (gamma-api, keyless): every bucket's Yes price at or before 09:00Z
from clob prices-history, normalised to sum 1, gives the market's implied mean high (tails counted at
their edge degree). Truth = the bucket that resolved Yes (EDDM METAR, the market's own rule). Error =
truth minus implied mean (negative = market warm). Low-cloud flag as P-0446: BKN, OVC or VV at or below
500 ft in an EDDM METAR before 10Z (Iowa State, keyless).

    python3 -I experiments/2026-11-17-P-0459/market.py
"""
import calendar
import json
import pathlib
import re
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}


def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())


def low_cloud(y1, m1, d1, y2, m2, d2):
    u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=skyc1&data=skyl1"
         "&data=skyc2&data=skyl2&data=skyc3&data=skyl3"
         f"&year1={y1}&month1={m1}&day1={d1}&year2={y2}&month2={m2}&day2={d2}&tz=UTC&format=onlycomma"
         "&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=180).read()
    lines = raw.decode("latin-1").splitlines()
    hdr = lines[0].split(",")
    low = defaultdict(bool)
    for line in lines[1:]:
        p = dict(zip(hdr, line.split(",")))
        d, hr = p["valid"][:10], int(p["valid"][11:13])
        if hr < 10:
            for i in "123":
                c, l = p.get("skyc" + i, "").strip(), p.get("skyl" + i, "").strip()
                if c in ("BKN", "OVC", "VV") and l:
                    try:
                        if float(l) <= 500:
                            low[d] = True
                    except ValueError:
                        pass
    return low


def degree(title):
    return int(re.match(r"(-?\d+)", title).group(1))


def price_at(token, ts):
    h = get(f"https://clob.polymarket.com/prices-history?market={token}&startTs={ts - 86400 * 3}&endTs={ts}&fidelity=60")
    pts = [x for x in h.get("history", []) if x["t"] <= ts]
    return pts[-1]["p"] if pts else None


rows = []
for day in range(1, 17):
    d = f"2026-11-{day:02d}"
    try:
        ev = get(f"https://gamma-api.polymarket.com/events?slug=highest-temperature-in-munich-on-november-{day}-2026")
    except Exception as e:  # noqa: BLE001
        rows.append({"date": d, "error": str(e)})
        continue
    if not ev:
        rows.append({"date": d, "error": "no event"})
        continue
    ts = calendar.timegm(time.strptime(d + " 09:00", "%Y-%m-%d %H:%M"))
    buckets, truth = [], None
    for m in ev[0]["markets"]:
        g = m["groupItemTitle"]
        deg = degree(g)
        yes = json.loads(m["clobTokenIds"])[0]
        outc = json.loads(m.get("outcomePrices") or "[]")
        if m.get("closed") and outc and float(outc[0]) == 1.0:
            truth = deg
        p = price_at(yes, ts)
        buckets.append({"bucket": g, "deg": deg, "p09z": p})
        time.sleep(0.15)
    priced = [b for b in buckets if b["p09z"] is not None]
    tot = sum(b["p09z"] for b in priced)
    if not priced or tot <= 0 or truth is None:
        rows.append({"date": d, "error": "no prices or unresolved", "buckets": buckets, "truth": truth})
        continue
    imean = sum(b["deg"] * b["p09z"] for b in priced) / tot
    fav = max(priced, key=lambda b: b["p09z"])
    rows.append({"date": d, "truth": truth, "implied_mean": round(imean, 2), "sum_p": round(tot, 3),
                 "fav": fav["deg"], "fav_p": fav["p09z"], "fav_hit": fav["deg"] == truth,
                 "err": round(truth - imean, 2), "priced": len(priced), "n_buckets": len(buckets),
                 "buckets": buckets})
    print(d, "truth", truth, "implied", round(imean, 2), "fav", fav["deg"], fav["p09z"], "sum", round(tot, 3))

low = low_cloud(2026, 11, 1, 2026, 11, 17)
for r in rows:
    r["low"] = low.get(r["date"], False)


def mean(x):
    return round(sum(x) / len(x), 3) if x else None


ok = [r for r in rows if "err" in r]
a = [r["err"] for r in ok if r["low"]]
b = [r["err"] for r in ok if not r["low"]]
summary = {"days_scored": len(ok), "low_n": len(a), "low_mean_err": mean(a), "other_n": len(b),
           "other_mean_err": mean(b), "gap": round(mean(a) - mean(b), 3) if a and b else None,
           "fav_hit": sum(r["fav_hit"] for r in ok), "fav_hit_low": sum(r["fav_hit"] for r in ok if r["low"]),
           "mean_abs_err": mean([abs(r["err"]) for r in ok]),
           "skipped": [{"date": r["date"], "why": r["error"]} for r in rows if "error" in r]}
print(json.dumps(summary, indent=1))
for r in ok:
    print(r["date"], "low" if r["low"] else "   ", "err", r["err"], "fav_hit", r["fav_hit"])
(HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
