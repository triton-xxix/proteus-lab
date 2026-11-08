"""P-0373: does the Met Office model carry the Heathrow offset P-0323 found for ICON?

Forecasts: Open-Meteo previous-runs API, ukmo_seamless and icon_seamless, 51.47,-0.4543, Sep and Oct 2026,
temperature at lead 0 and lead 1 day, maxed per Europe/London day. Observations: the Ogimet SYNOP files P-0323
saved (03772, 18 UTC 333 1snTxTxTx, the 06 to 18 UTC max), decoded the same way. Same day set for both models.
"""
import json
import pathlib
import urllib.request
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
HERE = pathlib.Path(__file__).parent
URL = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=51.47&longitude=-0.4543"
       "&hourly=temperature_2m,temperature_2m_previous_day1&start_date=2026-09-01&end_date=2026-10-31"
       "&timezone=Europe%2FLondon&models=")
UA = {"User-Agent": "proteus-research/1.0"}

obs = {}
for name in ("202609", "202610"):
    for line in open(f"{ROOT}/sandbox/ogimet-03772-{name}.txt", encoding="latin-1"):
        parts = line.strip().split(",")
        if len(parts) < 7 or parts[0] != "03772" or parts[4] != "18":
            continue
        groups = parts[6].replace("=", "").split()
        if "333" not in groups:
            continue
        sec = groups[groups.index("333") + 1:]
        if "555" in sec:
            sec = sec[:sec.index("555")]
        g = next((x for x in sec if len(x) == 5 and x[0] == "1" and x[1] in "01"), None)
        if g:
            obs[f"{parts[1]}-{parts[2]}-{parts[3]}"] = int(g[2:]) / 10 * (-1 if g[1] == "1" else 1)
print("obs days", len(obs))


def highs(model, var):
    data = json.loads(urllib.request.urlopen(urllib.request.Request(URL + model, headers=UA), timeout=90).read())
    (HERE / f"om-{model}.json").write_text(json.dumps(data))
    h = data["hourly"]
    key = var if var in h else f"{var}_{model}"
    if key not in h:
        raise SystemExit(f"no {var} for {model}: {sorted(h)}")
    dd = defaultdict(list)
    for t, v in zip(h["time"], h[key]):
        if v is not None:
            dd[t[:10]].append(v)
    return {d: max(v) for d, v in dd.items() if len(v) >= 23}


out = {"obs_days": len(obs), "leads": {}}
for lead, var in ((0, "temperature_2m"), (1, "temperature_2m_previous_day1")):
    uk = highs("ukmo_seamless", var)
    ic = highs("icon_seamless", var)
    days = sorted(set(uk) & set(ic) & set(obs))
    row = {"days": len(days), "first_last": [days[0], days[-1]] if days else None,
           "ukmo_days_alone": len(uk), "icon_days_alone": len(ic)}
    if len(days) > 1:
        for label, f in (("ukmo", uk), ("icon", ic)):
            errs = [obs[d] - f[d] for d in days]
            mean = sum(errs) / len(errs)
            sd = (sum((e - mean) ** 2 for e in errs) / (len(errs) - 1)) ** 0.5
            row[label] = {"mean_obs_minus_forecast": round(mean, 2), "sd": round(sd, 2),
                          "se": round(sd / len(errs) ** 0.5, 2), "mae": round(sum(abs(e) for e in errs) / len(errs), 2)}
        row["days_ukmo_closer"] = sum(abs(obs[d] - uk[d]) < abs(obs[d] - ic[d]) for d in days)
        row["days_icon_closer"] = sum(abs(obs[d] - ic[d]) < abs(obs[d] - uk[d]) for d in days)
    out["leads"][lead] = row
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
