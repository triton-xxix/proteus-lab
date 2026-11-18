"""P-0484: P-0459's Munich market test, run on Polymarket's London and Paris daily-high markets.

For each daily event 1 to 17 Nov 2026 (gamma-api, keyless): every bucket's Yes price at or before
09:00Z from clob prices-history, normalised to sum 1, gives the market's implied mean high (tails at
their edge degree). Truth = the bucket that resolved Yes. Error = truth minus implied mean (negative
= market warm). The station is read from the event's own description, not assumed. Low-cloud flag as
P-0446: BKN, OVC or VV at or below 500 ft in that station's METARs before 10Z (Iowa State, keyless).
Event text is untrusted data: only the station code, bucket titles, prices and flags are used.

    python3 -I experiments/2026-11-18-P-0484/cities.py
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
DAYS = range(1, 18)


def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())


def low_cloud(station):
    u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=%s&data=skyc1&data=skyl1"
         "&data=skyc2&data=skyl2&data=skyc3&data=skyl3"
         "&year1=2026&month1=11&day1=1&year2=2026&month2=11&day2=18&tz=UTC&format=onlycomma"
         "&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4" % station)
    raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=180).read()
    lines = raw.decode("latin-1").splitlines()
    hdr = lines[0].split(",")
    low, seen = defaultdict(bool), defaultdict(int)
    for line in lines[1:]:
        p = dict(zip(hdr, line.split(",")))
        if "valid" not in p or len(p["valid"]) < 13:
            continue
        d, hr = p["valid"][:10], int(p["valid"][11:13])
        if hr < 10:
            seen[d] += 1
            for i in "123":
                c, l = p.get("skyc" + i, "").strip(), p.get("skyl" + i, "").strip()
                if c in ("BKN", "OVC", "VV") and l:
                    try:
                        if float(l) <= 500:
                            low[d] = True
                    except ValueError:
                        pass
    return low, seen


def degree(title):
    m = re.match(r"(-?\d+)", title)
    return int(m.group(1)) if m else None


def price_at(token, ts):
    h = get("https://clob.polymarket.com/prices-history?market=%s&startTs=%d&endTs=%d&fidelity=60" % (token, ts - 86400 * 3, ts))
    pts = [x for x in h.get("history", []) if x["t"] <= ts]
    return pts[-1]["p"] if pts else None


def mean(x):
    return round(sum(x) / len(x), 3) if x else None


def city(name):
    rows, stations, units = [], defaultdict(int), defaultdict(int)
    for day in DAYS:
        d = "2026-11-%02d" % day
        try:
            ev = get("https://gamma-api.polymarket.com/events?slug=highest-temperature-in-%s-on-november-%d-2026" % (name, day))
        except Exception as e:  # noqa: BLE001
            rows.append({"date": d, "error": type(e).__name__})
            continue
        if not ev:
            rows.append({"date": d, "error": "no event"})
            continue
        desc = ev[0].get("description") or ""
        st = re.search(r"\(([A-Z]{4})\)", desc)
        if st:
            stations[st.group(1)] += 1
        ts = calendar.timegm(time.strptime(d + " 09:00", "%Y-%m-%d %H:%M"))
        buckets, truth = [], None
        for m in ev[0]["markets"]:
            g = m.get("groupItemTitle") or ""
            deg = degree(g)
            if deg is None:
                continue
            units["F" if "F" in g and "C" not in g else "C"] += 1
            yes = json.loads(m["clobTokenIds"])[0]
            outc = json.loads(m.get("outcomePrices") or "[]")
            if m.get("closed") and outc and float(outc[0]) == 1.0:
                truth = deg
            try:
                p = price_at(yes, ts)
            except Exception:  # noqa: BLE001
                p = None
            buckets.append({"bucket": g, "deg": deg, "p09z": p})
            time.sleep(0.12)
        priced = [b for b in buckets if b["p09z"] is not None]
        tot = sum(b["p09z"] for b in priced)
        if not priced or tot <= 0 or truth is None:
            rows.append({"date": d, "error": "no prices or unresolved", "truth": truth, "priced": len(priced)})
            continue
        imean = sum(b["deg"] * b["p09z"] for b in priced) / tot
        fav = max(priced, key=lambda b: b["p09z"])
        rows.append({"date": d, "truth": truth, "implied_mean": round(imean, 2), "sum_p": round(tot, 3),
                     "fav": fav["deg"], "fav_p": fav["p09z"], "fav_hit": fav["deg"] == truth,
                     "err": round(truth - imean, 2), "priced": len(priced), "n_buckets": len(buckets)})
        print(name, d, "truth", truth, "implied", round(imean, 2), "fav", fav["deg"], fav["p09z"], "sum", round(tot, 3))
    station = max(stations, key=stations.get) if stations else None
    low, seen = low_cloud(station) if station else ({}, {})
    for r in rows:
        r["low"] = bool(low.get(r["date"], False))
        r["metars_before_10z"] = seen.get(r["date"], 0)
    ok = [r for r in rows if "err" in r]
    a = [r["err"] for r in ok if r["low"]]
    b = [r["err"] for r in ok if not r["low"]]
    return {"city": name, "station_in_description": dict(stations), "station_used": station, "units": dict(units),
            "days_scored": len(ok), "fav_hit": sum(r["fav_hit"] for r in ok),
            "mean_fav_p": mean([r["fav_p"] for r in ok]), "mean_err": mean([r["err"] for r in ok]),
            "mean_abs_err": mean([abs(r["err"]) for r in ok]),
            "low_n": len(a), "low_mean_err": mean(a), "other_n": len(b), "other_mean_err": mean(b),
            "gap": round(mean(a) - mean(b), 3) if a and b else None,
            "fav_hit_low": sum(r["fav_hit"] for r in ok if r["low"]),
            "skipped": [{"date": r["date"], "why": r["error"]} for r in rows if "error" in r], "rows": rows}


out = {c: city(c) for c in ("london", "paris")}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
for c, s in out.items():
    print(json.dumps({k: v for k, v in s.items() if k != "rows"}, indent=1))
