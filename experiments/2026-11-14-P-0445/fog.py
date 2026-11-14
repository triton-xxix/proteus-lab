"""P-0445: does a morning fog code at EDDM mark days when ICON lead 1 runs warm on the day high?

Same data as experiments/2026-11-11-P-0418/points.py (Iowa State EDDM METAR, Open-Meteo previous-runs
icon_seamless lead 1 at the city point 48.137,11.575, maxed per UTC day, 1 Nov 2025 to 31 Oct 2026).
A fog day has FG or FZFG (not BCFG, MIFG, PRFG) in any METAR report 00Z to 09Z. Error = METAR high minus
forecast high, so negative means the forecast ran warm.

Fog is seasonal and P-0417 found the bias is seasonal, so the permutation shuffles the fog label only
within each calendar month (10,000 shuffles), which keeps the month mix fixed.
"""
import json
import pathlib
import random
import re
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
START, END = "2025-11-01", "2026-10-31"
FOG = re.compile(r"(^|\s)(FZ)?FG(\s|$)")


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()


def metar():
    u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=tmpc&data=wxcodes&year1=2025&month1=11&day1=1"
         "&year2=2026&month2=11&day2=1&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    lines = get(u).decode("latin-1").splitlines()
    hdr = lines[0].split(",")
    temps, fog = defaultdict(list), defaultdict(bool)
    for line in lines[1:]:
        p = dict(zip(hdr, line.split(",")))
        d, hr = p["valid"][:10], int(p["valid"][11:13])
        if p.get("tmpc"):
            try:
                temps[d].append(float(p["tmpc"]))
            except ValueError:
                pass
        if hr < 10 and FOG.search(p.get("wxcodes", "")):
            fog[d] = True
    return {d: max(v) for d, v in temps.items() if len(v) >= 40}, fog


def lead1():
    out = {}
    for a, b in (("2025-11-01", "2026-04-30"), ("2026-05-01", "2026-10-31")):
        h = json.loads(get("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=48.1370&longitude=11.5750"
                           f"&hourly=temperature_2m_previous_day1&start_date={a}&end_date={b}&timezone=UTC&models=icon_seamless"))["hourly"]
        key = next(k for k in h if k.startswith("temperature_2m_previous_day1"))
        m = defaultdict(list)
        for t, v in zip(h["time"], h[key]):
            if v is not None:
                m[t[:10]].append(v)
        out.update({k: max(v) for k, v in m.items() if len(v) >= 23})
        time.sleep(2)
    return out


def mean(x):
    return sum(x) / len(x) if x else float("nan")


mh, fog = metar()
fc = lead1()
rows = [{"date": d, "month": d[:7], "fog": fog.get(d, False), "err": round(mh[d] - fc[d], 2)}
        for d in sorted(set(mh) & set(fc)) if START <= d <= END]
f = [r["err"] for r in rows if r["fog"]]
c = [r["err"] for r in rows if not r["fog"]]
gap = mean(f) - mean(c)

by_month = defaultdict(list)
for r in rows:
    by_month[r["month"]].append(r)
random.seed(445)
N, hits = 10000, 0
for _ in range(N):
    sf, sc = [], []
    for ms in by_month.values():
        labels = [r["fog"] for r in ms]
        random.shuffle(labels)
        for r, lab in zip(ms, labels):
            (sf if lab else sc).append(r["err"])
    if mean(sf) - mean(sc) <= gap:
        hits += 1
p_one = (hits + 1) / (N + 1)

months = {}
for m, ms in sorted(by_month.items()):
    mf = [r["err"] for r in ms if r["fog"]]
    mc = [r["err"] for r in ms if not r["fog"]]
    months[m] = {"fog_n": len(mf), "fog_mean": round(mean(mf), 2) if mf else None,
                 "clear_n": len(mc), "clear_mean": round(mean(mc), 2) if mc else None}
big = [r for r in rows if r["err"] <= -2.5]
out = {"days": len(rows), "fog_days": len(f), "clear_days": len(c),
       "fog_mean_err": round(mean(f), 3), "clear_mean_err": round(mean(c), 3), "gap": round(gap, 3),
       "fog_mae": round(mean([abs(e) for e in f]), 3), "clear_mae": round(mean([abs(e) for e in c]), 3),
       "perm_p_one_sided_within_month": round(p_one, 4), "shuffles": N,
       "warm_misses_2p5": {"n": len(big), "fog": sum(1 for r in big if r["fog"])},
       "months": months, "rows": rows}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print({k: v for k, v in out.items() if k not in ("rows", "months")})
for m, v in months.items():
    print(m, v)
