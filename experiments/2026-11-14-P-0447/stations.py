"""P-0447: P-0446's low-cloud flag at Heathrow and Paris CDG, with EDDM re-run for the permutation it lacked.

Flag: any BKN, OVC or VV layer at or below 500 ft in a METAR before 10Z. Error = METAR day high (40+ reports)
minus Open-Meteo previous-runs icon_seamless lead-1 day high at the airport point (UTC days, 23+ hours),
1 Nov 2025 to 31 Oct 2026. Negative = forecast warm. Permutation shuffles the flag within calendar month,
10,000 times, one-sided. EDDM here uses the city point as in P-0446 for comparability.
"""
import json
import pathlib
import random
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
STATIONS = {"EGLL": (51.4775, -0.4614), "LFPG": (49.0097, 2.5479), "EDDM": (48.1370, 11.5750)}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=240).read()


def metar(st):
    u = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station={st}&data=tmpc"
         "&data=skyc1&data=skyl1&data=skyc2&data=skyl2&data=skyc3&data=skyl3"
         "&year1=2025&month1=11&day1=1&year2=2026&month2=11&day2=1&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    lines = get(u).decode("latin-1").splitlines()
    hdr = lines[0].split(",")
    temps, low = defaultdict(list), defaultdict(bool)
    for line in lines[1:]:
        p = dict(zip(hdr, line.split(",")))
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


def lead1(lat, lon):
    out = {}
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


def mean(x):
    return sum(x) / len(x) if x else float("nan")


def test(rows):
    a = [r["err"] for r in rows if r["low"]]
    b = [r["err"] for r in rows if not r["low"]]
    gap = mean(a) - mean(b)
    by_month = defaultdict(list)
    for r in rows:
        by_month[r["date"][:7]].append(r)
    rng = random.Random(447)
    hits = 0
    for _ in range(10000):
        sa, sb = [], []
        for ms in by_month.values():
            lab = [r["low"] for r in ms]
            rng.shuffle(lab)
            for r, l in zip(ms, lab):
                (sa if l else sb).append(r["err"])
        if mean(sa) - mean(sb) <= gap:
            hits += 1
    big = [r for r in rows if r["err"] <= -2.5]
    return {"days": len(rows), "flag_n": len(a), "flag_mean": round(mean(a), 3), "other_mean": round(mean(b), 3),
            "gap": round(gap, 3), "perm_p": round((hits + 1) / 10001, 4),
            "warm_misses_2p5": len(big), "caught": sum(1 for r in big if r["low"]),
            "flag_share_of_days": round(len(a) / len(rows), 3)}


out = {}
for st, (lat, lon) in STATIONS.items():
    mh, low = metar(st)
    time.sleep(2)
    fc = lead1(lat, lon)
    rows = [{"date": d, "low": low.get(d, False), "err": mh[d] - fc[d]}
            for d in sorted(set(mh) & set(fc)) if "2025-11-01" <= d <= "2026-10-31"]
    out[st] = test(rows)
    print(st, out[st])
(HERE / "results.json").write_text(json.dumps(out, indent=1))
