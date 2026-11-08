"""P-0368: capture tomorrow's ICON-D2 ensemble band for Munich's daily high, once a night, before it is knowable.

The twin of P-0232's capture.py, for the 2 km ensemble (19 members, reaches two days ahead). Appends one row
per target day to exchange/icon_d2_band.jsonl, so the nightly's step 4 commit carries it. A day already
captured is left alone. `score` prints coverage against DWD 03379 for D2 and for the ICON-EPS band on the
same days, each raw and shifted.

  python3 capture.py          append tomorrow's row
  python3 capture.py score    print coverage so far
"""
import datetime
import importlib.util
import json
import os
import sys
import urllib.request

ROOT = "/Users/triton/PROTEUS"
LOG = ROOT + "/exchange/icon_d2_band.jsonl"
GLOBAL = ROOT + "/exchange/icon_eps_band.jsonl"
URL = ("https://ensemble-api.open-meteo.com/v1/ensemble?latitude=48.137&longitude=11.575"
       "&daily=temperature_2m_max&models=icon_d2&forecast_days=3&timezone=Europe%2FBerlin")
SHIFT = 0.5
MIN_MEMBERS = 15


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def rows(path=LOG):
    if not os.path.exists(path):
        return []
    return [json.loads(line) for line in open(path) if line.strip()]


def capture():
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    if any(r["day"] == tomorrow for r in rows()):
        print("already captured %s" % tomorrow)
        return
    daily = json.load(urllib.request.urlopen(URL, timeout=30))["daily"]
    i = daily["time"].index(tomorrow)
    members = [daily[k][i] for k in daily if "member" in k and daily[k][i] is not None]
    if len(members) < MIN_MEMBERS:
        print("only %d members for %s, nothing written" % (len(members), tomorrow))
        return
    row = {"day": tomorrow, "captured_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
           "n": len(members), "control": daily["temperature_2m_max"][i],
           "p10": round(pct(members, 0.1), 2), "p50": round(pct(members, 0.5), 2),
           "p90": round(pct(members, 0.9), 2), "min": min(members), "max": max(members)}
    with open(LOG, "a") as f:
        f.write(json.dumps(row) + "\n")
    print("captured %s: p10 %.2f p50 %.2f p90 %.2f (n %d)" % (tomorrow, row["p10"], row["p50"], row["p90"], row["n"]))


def score():
    spec = importlib.util.spec_from_file_location(
        "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
    mfe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mfe)
    obs = mfe.observed("10865")  # WMO id; maps to DWD 03379 Stadt
    glob = {r["day"]: r for r in rows(GLOBAL)}
    done = [r for r in rows() if r["day"] in obs and r["day"] in glob]
    def inside(r, s):
        return r["p10"] + s <= obs[r["day"]] <= r["p90"] + s
    print("scored %d days. D2 inside raw %d, +%.1fC %d. ICON-EPS same days inside raw %d, +%.1fC %d (calibrated: 80%% inside)" % (
        len(done), sum(inside(r, 0) for r in done), SHIFT, sum(inside(r, SHIFT) for r in done),
        sum(inside(glob[r["day"]], 0) for r in done), SHIFT, sum(inside(glob[r["day"]], SHIFT) for r in done)))


if __name__ == "__main__":
    score() if sys.argv[1:] == ["score"] else capture()
