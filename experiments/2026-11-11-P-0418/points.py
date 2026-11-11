"""P-0418: which Munich forecast point is nearer the EDDM METAR day high, by month, Nov 2025 to Oct 2026?

P-0417's method (Iowa State METAR day high, at least 12 reports; Open-Meteo previous-runs icon_seamless
temperature_2m_previous_day1 maxed per UTC day). Three forecasts for each day: the city point the book
uses (48.137,11.575), the airport point (48.3538,11.7861) and the mean of the two. Each month is cut in
two (days 1 to 15, 16 on) to ask whether the point that was nearer in one half is nearer in the other.
"""
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
START, END = "2025-11-01", "2026-10-31"
NAMES = ("city", "airport", "mean")


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()


def metar_highs():
    u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=tmpc&year1=2025&month1=11&day1=1"
         "&year2=2026&month2=11&day2=1&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    m = defaultdict(list)
    for line in get(u).decode("latin-1").splitlines()[1:]:
        p = line.split(",")
        if len(p) >= 3 and p[2]:
            try:
                m[p[1][:10]].append(float(p[2]))
            except ValueError:
                pass
    return {k: max(v) for k, v in m.items() if len(v) >= 12}


def lead1_highs(lat, lon):
    out = {}
    # two pulls: a year of hourly values in one call timed out for nobody yet, but keep each small
    for a, b in (("2025-11-01", "2026-04-30"), ("2026-05-01", "2026-10-31")):
        h = json.loads(get(f"https://previous-runs-api.open-meteo.com/v1/forecast?latitude={lat:.4f}&longitude={lon:.4f}"
                           f"&hourly=temperature_2m_previous_day1&start_date={a}&end_date={b}&timezone=UTC&models=icon_seamless"))["hourly"]
        key = next(k for k in h if k.startswith("temperature_2m_previous_day1"))
        m = defaultdict(list)
        for t, v in zip(h["time"], h[key]):
            if v is not None:
                m[t[:10]].append(v)
        out.update({k: max(v) for k, v in m.items() if len(v) >= 23})
        time.sleep(2)
    return out


def score(errs):
    n = len(errs)
    if not n:
        return {"n": 0}
    return {"n": n, "bias": round(sum(errs) / n, 2), "mae": round(sum(abs(e) for e in errs) / n, 3),
            "exact_degree": round(sum(1 for e in errs if abs(e) < 0.5) / n, 3), "within_1": round(sum(1 for e in errs if abs(e) < 1.5) / n, 3)}


mh = metar_highs()
time.sleep(2)
city, air = lead1_highs(48.137, 11.575), lead1_highs(48.3538, 11.7861)
days = sorted(d for d in set(mh) & set(city) & set(air) if START <= d <= END)
err = {d: {"city": mh[d] - city[d], "airport": mh[d] - air[d], "mean": mh[d] - (city[d] + air[d]) / 2} for d in days}

out = {"days": len(days), "year": {n: score([err[d][n] for d in days]) for n in NAMES}, "months": {}}
agree, follow, always = 0, [], {n: [] for n in NAMES}
months = sorted({d[:7] for d in days})
for mth in months:
    ds = [d for d in days if d[:7] == mth]
    h1, h2 = [d for d in ds if int(d[8:]) <= 15], [d for d in ds if int(d[8:]) > 15]
    row = {n: score([err[d][n] for d in ds]) for n in NAMES}
    w1 = min(NAMES, key=lambda n: score([err[d][n] for d in h1])["mae"])
    w2 = min(NAMES, key=lambda n: score([err[d][n] for d in h2])["mae"])
    row["nearest_first_half"], row["nearest_second_half"] = w1, w2
    agree += w1 == w2
    follow += [err[d][w1] for d in h2]
    for n in NAMES:
        always[n] += [err[d][n] for d in h2]
    out["months"][mth] = row
out["first_half_winner_is_second_half_winner"] = "%d of %d months" % (agree, len(months))
out["second_halves"] = {"follow_the_first_half_winner": score(follow), **{"always_" + n: score(always[n]) for n in NAMES}}
# last month's winner carried into the next month, the only version usable live
carry, base = [], {n: [] for n in NAMES}
for prev, cur in zip(months, months[1:]):
    w = min(NAMES, key=lambda n: out["months"][prev][n]["mae"])
    ds = [d for d in days if d[:7] == cur]
    carry += [err[d][w] for d in ds]
    for n in NAMES:
        base[n] += [err[d][n] for d in ds]
out["carry_last_months_winner"] = {"carried": score(carry), **{"always_" + n: score(base[n]) for n in NAMES}}
# before and after the airport sensor break P-0355 found at 19 Apr 2026
for label, ds in (("to_2026-04-19", [d for d in days if d <= "2026-04-19"]), ("from_2026-04-20", [d for d in days if d > "2026-04-19"])):
    out[label] = {n: score([err[d][n] for d in ds]) for n in NAMES}
(HERE / "results.json").write_text(json.dumps(out, indent=1))

print("days", len(days))
print("year", json.dumps(out["year"]))
for mth in months:
    r = out["months"][mth]
    print(mth, " ".join("%s bias %+.2f mae %.2f" % (n, r[n]["bias"], r[n]["mae"]) for n in NAMES), "| halves:", r["nearest_first_half"], r["nearest_second_half"])
print("agree", out["first_half_winner_is_second_half_winner"])
print("second halves", json.dumps(out["second_halves"]))
print("carry", json.dumps(out["carry_last_months_winner"]))
print("break", json.dumps(out["to_2026-04-19"]), json.dumps(out["from_2026-04-20"]))
