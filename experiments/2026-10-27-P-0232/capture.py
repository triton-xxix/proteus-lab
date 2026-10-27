"""P-0232: capture tomorrow's ICON-EPS band for Munich's daily high, once a night, before it is knowable.

Appends one row per target day to exchange/icon_eps_band.jsonl (under exchange/ so the nightly's step 4
commit carries it, and the commit timestamp proves it came before the day). A day already captured is
left alone, so a second run in a night adds nothing. Scoring is `score` mode: each captured day that DWD
03379 (Stadt) has observed, inside the raw 10 to 90 band and inside the band shifted +0.5C.

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
LOG = ROOT + "/exchange/icon_eps_band.jsonl"
URL = ("https://ensemble-api.open-meteo.com/v1/ensemble?latitude=48.137&longitude=11.575"
       "&daily=temperature_2m_max&models=icon_seamless&forecast_days=3&timezone=Europe%2FBerlin")
SHIFT = 0.5


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def rows():
    if not os.path.exists(LOG):
        return []
    return [json.loads(line) for line in open(LOG) if line.strip()]


def capture():
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    if any(r["day"] == tomorrow for r in rows()):
        print("already captured %s" % tomorrow)
        return
    daily = json.load(urllib.request.urlopen(URL, timeout=30))["daily"]
    i = daily["time"].index(tomorrow)
    members = [daily[k][i] for k in daily if k.startswith("temperature_2m_max_member") and daily[k][i] is not None]
    if len(members) < 30:
        print("only %d members for %s, nothing written" % (len(members), tomorrow))
        return
    row = {"day": tomorrow, "captured_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
           "n": len(members), "control": daily["temperature_2m_max"][i],
           "p10": round(pct(members, 0.1), 2), "p50": round(pct(members, 0.5), 2),
           "p90": round(pct(members, 0.9), 2), "min": min(members), "max": max(members)}
    with open(LOG, "a") as f:
        f.write(json.dumps(row) + "\n")
    print("captured %s: p10 %.2f p90 %.2f width %.2f (n %d)" % (
        tomorrow, row["p10"], row["p90"], row["p90"] - row["p10"], row["n"]))


def score():
    spec = importlib.util.spec_from_file_location(
        "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
    mfe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mfe)
    obs = mfe.observed("10865")  # WMO id; maps to DWD 03379 Stadt
    done = [r for r in rows() if r["day"] in obs]
    raw = sum(r["p10"] <= obs[r["day"]] <= r["p90"] for r in done)
    shifted = sum(r["p10"] + SHIFT <= obs[r["day"]] <= r["p90"] + SHIFT for r in done)
    above = sum(obs[r["day"]] > r["p90"] for r in done)
    print("scored %d of %d captured: inside raw %d, inside +%.1fC %d, above band %d (calibrated: 80%% inside)"
          % (len(done), len(rows()), raw, SHIFT, shifted, above))


if __name__ == "__main__":
    score() if sys.argv[1:] == ["score"] else capture()
