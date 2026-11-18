"""P-0487: can the Munich low-cloud morning be flagged the night before, from the forecast alone?

Truth flag (P-0446): any BKN, OVC or VV layer at or below 500 ft in an EDDM METAR before 10Z.
Error: METAR day high (40+ reports) minus icon_seamless lead-1 day high at the city point
(48.137, 11.575), UTC days with 23+ hours, 1 Nov 2025 to 31 Oct 2026. Negative = forecast warm.

Forecast flags, each fixed before the run:
  A  lead-1 TOTAL cloud cover, mean of 06Z to 09Z, at or above 95%  (known the night before)
  B  latest-run LOW cloud cover, mean of 06Z to 09Z, at or above 90% (NOT known the night before:
     the previous-runs API's plain `cloud_cover_low` is the most recent run; an upper bound on what
     the model itself can say, since `cloud_cover_low_previous_day1` is all null for icon_seamless)
For each: how many METAR-flag days it catches, how many of its own days are real, and the mean
error on its days against the rest. Keyless: Iowa State METAR archive, Open-Meteo previous-runs.

    python3 -I experiments/2026-11-18-P-0487/flag.py
"""
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
LAT, LON = 48.1370, 11.5750
SPANS = (("2025-11-01", "2026-04-30"), ("2026-05-01", "2026-10-31"))


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=240).read()


def metar():
    u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=tmpc"
         "&data=skyc1&data=skyl1&data=skyc2&data=skyl2&data=skyc3&data=skyl3"
         "&year1=2025&month1=11&day1=1&year2=2026&month2=11&day2=1&tz=UTC&format=onlycomma&latlon=no"
         "&missing=empty&trace=empty&report_type=3&report_type=4")
    lines = get(u).decode("latin-1").splitlines()
    hdr = lines[0].split(",")
    temps, low = defaultdict(list), defaultdict(bool)
    for line in lines[1:]:
        p = dict(zip(hdr, line.split(",")))
        if len(p.get("valid", "")) < 13:
            continue
        d, hr = p["valid"][:10], int(p["valid"][11:13])
        if p.get("tmpc"):
            try:
                temps[d].append(float(p["tmpc"]))
            except ValueError:
                pass
        if hr < 10:
            for i in "123":
                c, l = p.get("skyc" + i, "").strip(), p.get("skyl" + i, "").strip()
                if c in ("BKN", "OVC", "VV") and l:
                    try:
                        if float(l) <= 500:
                            low[d] = True
                    except ValueError:
                        pass
    return {d: max(v) for d, v in temps.items() if len(v) >= 40}, low


def forecast():
    high, tot, lowc, nulls = {}, {}, {}, 0
    for a, b in SPANS:
        h = json.loads(get("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=%.4f&longitude=%.4f"
                           "&hourly=temperature_2m_previous_day1,cloud_cover_previous_day1,cloud_cover_low,cloud_cover_low_previous_day1"
                           "&start_date=%s&end_date=%s&timezone=UTC&models=icon_seamless" % (LAT, LON, a, b)))["hourly"]
        t2 = defaultdict(list)
        cc = defaultdict(list)
        cl = defaultdict(list)
        for i, t in enumerate(h["time"]):
            d, hr = t[:10], int(t[11:13])
            v = h["temperature_2m_previous_day1"][i]
            if v is not None:
                t2[d].append(v)
            if h["cloud_cover_low_previous_day1"][i] is None:
                nulls += 1
            if 6 <= hr <= 9:
                if h["cloud_cover_previous_day1"][i] is not None:
                    cc[d].append(h["cloud_cover_previous_day1"][i])
                if h["cloud_cover_low"][i] is not None:
                    cl[d].append(h["cloud_cover_low"][i])
        high.update({k: max(v) for k, v in t2.items() if len(v) >= 23})
        tot.update({k: sum(v) / len(v) for k, v in cc.items() if len(v) == 4})
        lowc.update({k: sum(v) / len(v) for k, v in cl.items() if len(v) == 4})
        total_hours = len(h["time"])
        time.sleep(2)
    return high, tot, lowc, nulls


def mean(x):
    return round(sum(x) / len(x), 3) if x else None


def score(rows, key):
    f = [r for r in rows if r[key]]
    nf = [r for r in rows if not r[key]]
    truth = [r for r in rows if r["metar_low"]]
    caught = sum(1 for r in truth if r[key])
    real = sum(1 for r in f if r["metar_low"])
    big = [r for r in rows if r["err"] <= -2.5]
    return {"flagged_days": len(f), "share_of_days": round(len(f) / len(rows), 3),
            "metar_low_days_caught": caught, "recall": round(caught / len(truth), 3) if truth else None,
            "precision": round(real / len(f), 3) if f else None,
            "mean_err_flagged": mean([r["err"] for r in f]), "mean_err_rest": mean([r["err"] for r in nf]),
            "gap": round(mean([r["err"] for r in f]) - mean([r["err"] for r in nf]), 3) if f and nf else None,
            "warm_misses_2p5_caught": sum(1 for r in big if r[key]), "warm_misses_2p5": len(big)}


mh, low = metar()
time.sleep(2)
high, tot, lowc, nulls = forecast()
rows = []
for d in sorted(set(mh) & set(high) & set(tot) & set(lowc)):
    if "2025-11-01" <= d <= "2026-10-31":
        rows.append({"date": d, "err": round(mh[d] - high[d], 2), "metar_low": bool(low.get(d, False)),
                     "A_total_lead1": tot[d] >= 95.0, "B_low_latest": lowc[d] >= 90.0,
                     "total_lead1": round(tot[d], 1), "low_latest": round(lowc[d], 1)})
rows_metar = [dict(r, M=r["metar_low"]) for r in rows]
out = {"days": len(rows), "metar_low_days": sum(r["metar_low"] for r in rows),
       "lead1_low_cloud_null_hours": nulls,
       "truth_flag_same_morning_METAR": score(rows_metar, "M"),
       "A_lead1_total_cloud_95": score(rows, "A_total_lead1"),
       "B_latest_run_low_cloud_90": score(rows, "B_low_latest"),
       "winter_only_Nov_to_Feb": {
           "days": sum(1 for r in rows if r["date"][5:7] in ("11", "12", "01", "02")),
           "A": score([r for r in rows if r["date"][5:7] in ("11", "12", "01", "02")], "A_total_lead1"),
           "B": score([r for r in rows if r["date"][5:7] in ("11", "12", "01", "02")], "B_low_latest")},
       "rows": rows}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
