"""P-0383: is ICON's cold bias on the day's high the same at a second UK airport?

Station identity first (NOAA's station list), because 03776 came from memory. Then Ogimet SYNOP Sep and Oct 2026, the P-0323
decode of the 18 UTC 333 1snTxTxTx group, against icon_seamless previous-runs at the station's own coordinates, on Heathrow's 61 days.
"""
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
HERE = pathlib.Path(__file__).parent
BLOCK = "03776"
UA = {"User-Agent": "proteus-research/1.0"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()


def dms(s):
    s = s.strip()
    hemi = s[-1]
    p = s[:-1].split("-")
    v = int(p[0]) + int(p[1]) / 60 + (int(p[2]) / 3600 if len(p) > 2 else 0)
    return -v if hemi in "SW" else v


# NOAA's station list did not resolve from this machine on 9 Nov. Identity is instead tested below: the block's TX against
# EGKK and EGLL METAR daily highs from Iowa State's keyless archive. Coordinates are Gatwick's published ARP.
name, lat, lon = "Gatwick (block from memory, tested below)", 51.148, -0.190


def metar_highs(icao):
    u = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station={icao}&data=tmpc&year1=2026&month1=9&day1=1"
         "&year2=2026&month2=11&day2=1&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    t = get(u).decode("latin-1").splitlines()
    (HERE / f"iem-{icao}.csv").write_text("\n".join(t))
    m = defaultdict(list)
    for line in t[1:]:
        p = line.split(",")
        if len(p) >= 3 and p[2]:
            try:
                m[p[1][:10]].append(float(p[2]))
            except ValueError:
                pass
    return {k: max(v) for k, v in m.items() if len(v) >= 12}


def decode(text, block):
    out = {}
    for line in text.splitlines():
        parts = line.strip().split(",")
        if len(parts) < 7 or parts[0] != block or parts[4] != "18":
            continue
        groups = parts[6].replace("=", "").split()
        if "333" not in groups:
            continue
        sec = groups[groups.index("333") + 1:]
        if "555" in sec:
            sec = sec[:sec.index("555")]
        g = next((x for x in sec if len(x) == 5 and x[0] == "1" and x[1] in "01"), None)
        if g:
            out[f"{parts[1]}-{parts[2]}-{parts[3]}"] = int(g[2:]) / 10 * (-1 if g[1] == "1" else 1)
    return out


obs = {}
for ym, end in (("202609", "30"), ("202610", "31")):
    t = get(f"https://www.ogimet.com/cgi-bin/getsynop?block={BLOCK}&begin={ym}010000&end={ym}{end}2359").decode("latin-1")
    (HERE / f"ogimet-{BLOCK}-{ym}.txt").write_text(t)
    obs.update(decode(t, BLOCK))
    time.sleep(3)
print("obs days", len(obs))

ident = {}
for icao in ("EGKK", "EGLL"):
    mh = metar_highs(icao)
    shared = sorted(set(mh) & set(obs))
    diffs = [abs(obs[x] - mh[x]) for x in shared]
    ident[icao] = {"days": len(shared), "mean_abs_diff": round(sum(diffs) / len(diffs), 3) if diffs else None}
    time.sleep(2)
print("identity", ident)

hobs = {}
for ym in ("202609", "202610"):
    hobs.update(decode(open(f"{ROOT}/sandbox/ogimet-03772-{ym}.txt", encoding="latin-1").read(), "03772"))

URL = (f"https://previous-runs-api.open-meteo.com/v1/forecast?latitude={lat:.4f}&longitude={lon:.4f}"
       "&hourly=temperature_2m,temperature_2m_previous_day1&start_date=2026-09-01&end_date=2026-10-31"
       "&timezone=Europe%2FLondon&models=icon_seamless")
d = json.loads(get(URL))
(HERE / "om-icon.json").write_text(json.dumps(d))
# Heathrow forecast from P-0382's saved pull
hd = json.load(open(f"{ROOT}/experiments/2026-11-09-P-0382/om-raw.json"))["heathrow"]


def highs(dd, var):
    h = dd["hourly"]
    key = var if var in h else f"{var}_icon_seamless"
    m = defaultdict(list)
    for t, v in zip(h["time"], h[key]):
        if v is not None:
            m[t[:10]].append(v)
    return {k: max(v) for k, v in m.items() if len(v) >= 23}


def stat(e):
    n = len(e)
    mean = sum(e) / n
    sd = (sum((x - mean) ** 2 for x in e) / (n - 1)) ** 0.5
    return {"mean": round(mean, 2), "sd": round(sd, 2), "se": round(sd / n ** 0.5, 2), "n": n}


out = {"station": {"block": BLOCK, "name": name, "lat": lat, "lon": lon, "model_elevation_m": d.get("elevation"), "model_point": [d["latitude"], d["longitude"]]},
       "obs_days": len(obs), "identity_check": ident, "leads": {}}
for lead, var in ((0, "temperature_2m"), (1, "temperature_2m_previous_day1")):
    g = highs(d, var)
    h = highs(hd, var)
    days = sorted(set(g) & set(h) & set(obs) & set(hobs))
    ge = [obs[x] - g[x] for x in days]
    he = [hobs[x] - h[x] for x in days]
    paired = [a - b for a, b in zip(ge, he)]
    out["leads"][lead] = {"days": len(days), "first_last": [days[0], days[-1]] if days else None, "gatwick": stat(ge), "heathrow": stat(he),
                          "gatwick_minus_heathrow": stat(paired), "corr_of_errors": round(float(__import__("numpy").corrcoef(ge, he)[0, 1]), 3)}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
