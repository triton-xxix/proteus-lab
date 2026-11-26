"""P-0575: capture tomorrow's AIFS (ECMWF AI ensemble, 50 members) and NCEP GEFS (30 members) bands for
Munich's daily high, once a night, before it is knowable. Twin of P-0368's capture.py.

Open-Meteo's past_days reaches back only to 23 Nov 2026 for both models (checked 26 Nov), so a past-only
bias fit like P-0561's is not possible; the only honest record is a forward one. Appends one row per
target day per model to exchange/aifs_gefs_band.jsonl. A day already captured is left alone.
`score` prints coverage against DWD 03379 (WMO 10865) for each, raw and +0.5C, beside ICON-EPS on the
same days.

  python3 capture.py          append tomorrow's rows
  python3 capture.py score    print coverage so far
"""
import datetime
import importlib.util
import json
import os
import sys
import urllib.request

ROOT = "/Users/triton/PROTEUS"
LOG = ROOT + "/exchange/aifs_gefs_band.jsonl"
GLOBAL = ROOT + "/exchange/icon_eps_band.jsonl"
URL = ("https://ensemble-api.open-meteo.com/v1/ensemble?latitude=48.137&longitude=11.575"
       "&daily=temperature_2m_max&models=ecmwf_aifs025,gfs_seamless&forecast_days=3&timezone=Europe%2FBerlin")
MODELS = {"aifs": "ecmwf_aifs025_ensemble", "gefs": "ncep_gefs_seamless"}
MIN_MEMBERS = {"aifs": 40, "gefs": 25}
SHIFT = 0.5


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
    have = {(r["day"], r["model"]) for r in rows()}
    daily = json.load(urllib.request.urlopen(URL, timeout=30))["daily"]
    i = daily["time"].index(tomorrow)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    for name, suffix in MODELS.items():
        if (tomorrow, name) in have:
            print("already captured %s %s" % (name, tomorrow))
            continue
        members = [daily[k][i] for k in daily if "member" in k and k.endswith(suffix) and daily[k][i] is not None]
        if len(members) < MIN_MEMBERS[name]:
            print("only %d %s members for %s, nothing written" % (len(members), name, tomorrow))
            continue
        row = {"day": tomorrow, "model": name, "captured_utc": now, "n": len(members),
               "control": daily.get("temperature_2m_max_" + suffix, [None] * (i + 1))[i],
               "p10": round(pct(members, 0.1), 2), "p50": round(pct(members, 0.5), 2),
               "p90": round(pct(members, 0.9), 2), "min": min(members), "max": max(members)}
        with open(LOG, "a") as f:
            f.write(json.dumps(row) + "\n")
        print("captured %s %s: p10 %.2f p50 %.2f p90 %.2f (n %d)" % (name, tomorrow, row["p10"], row["p50"], row["p90"], row["n"]))


def score():
    spec = importlib.util.spec_from_file_location(
        "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
    mfe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mfe)
    obs = mfe.observed("10865")
    glob = {r["day"]: r for r in rows(GLOBAL)}

    def inside(r, s):
        return r["p10"] + s <= obs[r["day"]] <= r["p90"] + s
    for name in MODELS:
        done = [r for r in rows() if r["model"] == name and r["day"] in obs and r["day"] in glob]
        print("%s scored %d days: inside raw %d, +%.1fC %d. ICON-EPS same days raw %d, +%.1fC %d (calibrated: 80%% inside)" % (
            name, len(done), sum(inside(r, 0) for r in done), SHIFT, sum(inside(r, SHIFT) for r in done),
            sum(inside(glob[r["day"]], 0) for r in done), SHIFT, sum(inside(glob[r["day"]], SHIFT) for r in done)))


if __name__ == "__main__":
    score() if sys.argv[1:] == ["score"] else capture()
