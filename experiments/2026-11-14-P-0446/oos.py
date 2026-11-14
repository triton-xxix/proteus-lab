"""P-0446: P-0445's fog flag out of sample, 1 to 13 Nov 2026, plus a low-cloud flag.

Same sources and rules as experiments/2026-11-14-P-0445/fog.py. Fog flag: FG or FZFG in a METAR before 10Z.
Low-cloud flag: any BKN, OVC or VV layer at or below 500 ft before 10Z. Error = METAR high minus ICON lead-1
city forecast high (negative = forecast warm). Also re-scores the low-cloud flag on P-0445's in-sample year
so the two flags are compared on the same days.
"""
import json
import pathlib
import re
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
FOG = re.compile(r"(^|\s)(FZ)?FG(\s|$)")


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()


def metar(y1, m1, d1, y2, m2, d2):
    u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=tmpc&data=wxcodes"
         "&data=skyc1&data=skyl1&data=skyc2&data=skyl2&data=skyc3&data=skyl3"
         f"&year1={y1}&month1={m1}&day1={d1}&year2={y2}&month2={m2}&day2={d2}&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    lines = get(u).decode("latin-1").splitlines()
    hdr = lines[0].split(",")
    temps, fog, low = defaultdict(list), defaultdict(bool), defaultdict(bool)
    for line in lines[1:]:
        p = dict(zip(hdr, line.split(",")))
        d, hr = p["valid"][:10], int(p["valid"][11:13])
        if p.get("tmpc"):
            try:
                temps[d].append(float(p["tmpc"]))
            except ValueError:
                pass
        if hr < 10:
            if FOG.search(p.get("wxcodes", "")):
                fog[d] = True
            for i in "123":
                c, l = p.get("skyc" + i, "").strip(), p.get("skyl" + i, "").strip()
                if c in ("BKN", "OVC", "VV") and l:
                    try:
                        if float(l) <= 500:
                            low[d] = True
                    except ValueError:
                        pass
    return {d: max(v) for d, v in temps.items() if len(v) >= 40}, fog, low


def lead1(spans):
    out = {}
    for a, b in spans:
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
    return round(sum(x) / len(x), 3) if x else None


def split(rows, flag):
    a = [r["err"] for r in rows if r[flag]]
    b = [r["err"] for r in rows if not r[flag]]
    big = [r for r in rows if r["err"] <= -2.5]
    gap = round(mean(a) - mean(b), 3) if a and b else None
    return {"flag_n": len(a), "flag_mean": mean(a), "other_n": len(b), "other_mean": mean(b), "gap": gap,
            "warm_misses_2p5": len(big), "caught": sum(1 for r in big if r[flag])}


def build(mh, fog, low, fc, lo, hi):
    return [{"date": d, "fog": fog.get(d, False), "low": low.get(d, False), "either": fog.get(d, False) or low.get(d, False),
             "err": round(mh[d] - fc[d], 2), "metar": mh[d], "fc": round(fc[d], 1)}
            for d in sorted(set(mh) & set(fc)) if lo <= d <= hi]


mh, fog, low = metar(2026, 11, 1, 2026, 11, 14)
fc = lead1([("2026-11-01", "2026-11-13")])
oos = build(mh, fog, low, fc, "2026-11-01", "2026-11-13")
time.sleep(2)
mh2, fog2, low2 = metar(2025, 11, 1, 2026, 11, 1)
fc2 = lead1([("2025-11-01", "2026-04-30"), ("2026-05-01", "2026-10-31")])
ins = build(mh2, fog2, low2, fc2, "2025-11-01", "2026-10-31")
out = {"out_of_sample": {f: split(oos, f) for f in ("fog", "low", "either")},
       "in_sample_year": {f: split(ins, f) for f in ("fog", "low", "either")},
       "oos_rows": oos}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "oos_rows"}, indent=1))
for r in oos:
    print(r)
