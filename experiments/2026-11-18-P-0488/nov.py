"""P-0488: the nightly's Munich recipe on 17 days it has not seen.

Recipe (tasks/nightly.md): icon_seamless at 48.137, 11.575, timezone Europe/Berlin, the local day's
high at lead 1, nothing added, rounded to the whole degree. Truth: the highest EDDM METAR
temperature on the same local day (Iowa State archive, whole degrees, 40+ reports), which is what
the market is taken to settle on (P-0334). Error = METAR high minus forecast (negative = forecast
warm). Lead 2 is scored beside it because three of the last four book calls were made at lead 2.
Keyless: two requests.

    python3 -I experiments/2026-11-18-P-0488/nov.py
"""
import json
import math
import pathlib
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=240).read()


u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=tmpc"
     "&year1=2026&month1=10&day1=31&year2=2026&month2=11&day2=18&tz=Europe%2FBerlin&format=onlycomma&latlon=no"
     "&missing=empty&trace=empty&report_type=3&report_type=4")
lines = get(u).decode("latin-1").splitlines()
hdr = lines[0].split(",")
temps = defaultdict(list)
for line in lines[1:]:
    p = dict(zip(hdr, line.split(",")))
    if p.get("tmpc") and len(p.get("valid", "")) >= 13:
        try:
            temps[p["valid"][:10]].append(float(p["tmpc"]))
        except ValueError:
            pass
truth = {d: max(v) for d, v in temps.items() if len(v) >= 40}

h = json.loads(get("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=48.1370&longitude=11.5750"
                   "&hourly=temperature_2m_previous_day1,temperature_2m_previous_day2"
                   "&start_date=2026-11-01&end_date=2026-11-17&timezone=Europe%2FBerlin&models=icon_seamless"))["hourly"]


def day_high(prefix):
    key = next(k for k in h if k.startswith(prefix))
    m = defaultdict(list)
    for t, v in zip(h["time"], h[key]):
        if v is not None:
            m[t[:10]].append(v)
    return {k: max(v) for k, v in m.items() if len(v) >= 23}


def half_up(x):
    return math.floor(x + 0.5)


def score(fc):
    rows = [{"date": d, "metar_high": truth[d], "forecast": round(fc[d], 2), "err": round(truth[d] - fc[d], 2),
             "called_degree": half_up(fc[d]), "hit": half_up(fc[d]) == round(truth[d])}
            for d in sorted(set(truth) & set(fc)) if "2026-11-01" <= d <= "2026-11-17"]
    e = [r["err"] for r in rows]
    n = len(e)
    m = sum(e) / n
    se = math.sqrt(sum((x - m) ** 2 for x in e) / (n - 1) / n)
    miss = [round(truth[r["date"]]) - r["called_degree"] for r in rows]
    return {"days": n, "bias": round(m, 3), "se": round(se, 3), "mean_abs_err": round(sum(abs(x) for x in e) / n, 3),
            "exact_degree_hits": sum(r["hit"] for r in rows),
            "truth_above_call": sum(1 for x in miss if x > 0), "truth_below_call": sum(1 for x in miss if x < 0),
            "within_one_degree": sum(1 for x in miss if abs(x) <= 1),
            "hits_if_one_degree_subtracted": sum(1 for r in rows if half_up(r["forecast"] - 1.0) == round(r["metar_high"])),
            "hits_if_half_degree_subtracted": sum(1 for r in rows if half_up(r["forecast"] - 0.5) == round(r["metar_high"])),
            "rows": rows}


out = {"lead1": score(day_high("temperature_2m_previous_day1")), "lead2": score(day_high("temperature_2m_previous_day2"))}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
for k, v in out.items():
    print(k, json.dumps({a: b for a, b in v.items() if a != "rows"}))
    for r in v["rows"]:
        print("  ", r["date"], "metar", r["metar_high"], "fc", r["forecast"], "err", r["err"], "HIT" if r["hit"] else "")
