"""P-0565: did Munich's gappy straddle ladders settle cleanly, and what do tonight's ladders miss?

Settled side: the 23, 24 and 25 Nov ladders P-0553 found with missing degrees (its nov23_results.json and
open_results.json), their winners in exchange/munich_outcomes.jsonl, and the highest EDDM METAR temperature
for each local (Europe/Berlin) day from aviationweather.gov (keyless, last 96 h; whole degrees, as the market
reads, D-023).
Open side: the two ladders listed tonight by exchange.py markets (names only, no prices), with the
icon_seamless day high at 48.137,11.575, timezone Europe/Berlin (the nightly's recipe).
"""
import datetime, json, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("/Users/triton/PROTEUS")
HERE = Path(__file__).resolve().parent
BER = ZoneInfo("Europe/Berlin")
UA = {"User-Agent": "proteus-probe/1"}

p553 = ROOT / "experiments/2026-11-23-P-0553"
gaps = {r["market_id"]: r for f in ("nov23_results.json", "open_results.json") for r in json.loads((p553 / f).read_text())}
day_of = {"180152672": "2026-11-23", "180443002": "2026-11-24", "180722282": "2026-11-25"}
winners = {}
for line in open(ROOT / "exchange/munich_outcomes.jsonl"):
    if line.strip():
        r = json.loads(line)
        winners[r["market_id"]] = r["winner"]

met = json.load(urllib.request.urlopen(urllib.request.Request(
    "https://aviationweather.gov/api/data/metar?ids=EDDM&hours=96&format=json", headers=UA), timeout=30))
hi, n = {}, {}
for m in met:
    if m.get("temp") is None:
        continue
    d = datetime.datetime.fromtimestamp(m["obsTime"], datetime.timezone.utc).astimezone(BER).date().isoformat()
    hi[d] = max(hi.get(d, -99), m["temp"])
    n[d] = n.get(d, 0) + 1

settled = []
for mid, d in day_of.items():
    g = gaps[mid]
    listed = [x for x in range(g["low_bin"], g["high_bin"] + 1) if x not in g["missing"]]
    w = winners.get(mid)
    wdeg = int(w.replace("°C", "").split()[0]) if w and w[0] in "-0123456789" else w
    h = hi.get(d)
    settled.append({"day": d, "market_id": mid, "missing": g["missing"], "bins": [g["low_bin"], g["high_bin"]],
                    "metar_high": h, "metar_obs": n.get(d), "metar_high_listed": (h in listed) if h is not None else None,
                    "winner": w, "winner_matches_metar": (wdeg == h) if (h is not None and isinstance(wdeg, int)) else None})

# tonight's ladders, from the markets listing at 23:33Z (names only)
tonight = {"2026-11-26": {"listed": [0, -1, 2, -3, 4], "low_open": -5, "high_open": 5},
           "2026-11-27": {"listed": [0, -1, -2, -3, -4], "low_open": -5, "high_open": 5}}
om = json.load(urllib.request.urlopen(urllib.request.Request(
    "https://api.open-meteo.com/v1/forecast?latitude=48.137&longitude=11.575&daily=temperature_2m_max"
    "&models=icon_seamless&timezone=Europe%2FBerlin&forecast_days=3", headers=UA), timeout=30))["daily"]
icon = dict(zip(om["time"], om["temperature_2m_max"]))
open_rows = []
for d, t in tonight.items():
    inner = list(range(t["low_open"] + 1, t["high_open"]))
    missing = [x for x in inner if x not in t["listed"]]
    pt = icon.get(d)
    near = round(pt) if pt is not None else None
    # whole degrees within 1.5 C of ICON's point: the plausible winners
    plausible = [x for x in inner if pt is not None and abs(x - pt) <= 1.5]
    open_rows.append({"day": d, "listed": sorted(t["listed"]), "missing": missing, "icon_point": pt, "icon_rounded": near,
                      "icon_rounded_missing": near in missing, "plausible_within_1p5": plausible,
                      "plausible_missing": [x for x in plausible if x in missing]})

out = {"settled": settled, "tonight": open_rows, "metar_days": {d: [hi[d], n[d]] for d in sorted(hi)}}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
for r in settled:
    print("SETTLED", json.dumps(r))
for r in open_rows:
    print("OPEN", json.dumps(r))
