"""Pull the UK retailers' open fuel-price feeds (CMA interim scheme, July 2023) and see which still answer.

Keyless. Prints per-feed status, station counts and median E10 / B7 prices, then a national summary.
Usage: python3 fuel_prices.py [out.json]
"""
import json
import statistics
import sys
import time
import urllib.request

FEEDS = {
    "Asda": "https://storelocator.asda.com/fuel_prices_data.json",
    "BP": "https://www.bp.com/en_gb/united-kingdom/home/fuelprices/fuel_prices_data.json",
    "Esso/Tesco Alliance": "https://fuelprices.esso.co.uk/latestdata.json",
    "JET": "https://jetlocal.co.uk/fuel_prices_data.json",
    "Morrisons": "https://www.morrisons.com/fuel-prices/fuel.json",
    "Moto": "https://moto-way.com/fuel-price/fuel_prices.json",
    "MFG": "https://fuel.motorfuelgroup.com/fuel_prices_data.json",
    "Rontec": "https://www.rontec-servicestations.co.uk/fuel-prices/data/fuel_prices_data.json",
    "Sainsbury's": "https://api.sainsburys.co.uk/v1/exports/latest/fuel_prices_data.json",
    "SGN": "https://www.sgnretail.uk/files/data/SGN_daily_fuel_prices.json",
    "Shell": "https://www.shell.co.uk/fuel-prices-data.html",
    "Tesco": "https://www.tesco.com/fuel_prices/fuel_prices_data.json",
    "Ascona": "https://fuelprices.asconagroup.co.uk/newfuel.json",
}

UA = {"User-Agent": "Mozilla/5.0 (proteus field notes; keyless read)", "Accept": "application/json"}


def fetch(url):
    t = time.time()
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read()
            code = r.status
        return code, body, time.time() - t, None
    except Exception as e:  # a dead feed is a result
        return None, None, time.time() - t, f"{type(e).__name__}: {str(e)[:80]}"


def to_pence(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v <= 0:
        return None
    if v < 10:  # some feeds publish pounds
        v *= 100
    if v > 1000:  # tenths of a penny
        v /= 10
    return v if 100 <= v <= 250 else None


def main():
    out = {"pulled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "feeds": {}}
    all_e10, all_b7 = [], []
    for name, url in FEEDS.items():
        code, body, secs, err = fetch(url)
        rec = {"url": url, "status": code, "seconds": round(secs, 2), "error": err}
        if body:
            try:
                data = json.loads(body)
                stations = data.get("stations", []) if isinstance(data, dict) else []
                e10 = [p for p in (to_pence(s.get("prices", {}).get("E10")) for s in stations) if p]
                b7 = [p for p in (to_pence(s.get("prices", {}).get("B7")) for s in stations) if p]
                rec.update(
                    last_updated=data.get("last_updated") if isinstance(data, dict) else None,
                    stations=len(stations),
                    e10_n=len(e10),
                    e10_median=round(statistics.median(e10), 1) if e10 else None,
                    e10_min=min(e10) if e10 else None,
                    e10_max=max(e10) if e10 else None,
                    b7_n=len(b7),
                    b7_median=round(statistics.median(b7), 1) if b7 else None,
                )
                lu = rec["last_updated"] or ""
                try:
                    age_days = (time.time() - time.mktime(time.strptime(lu[:10], "%d/%m/%Y"))) / 86400
                except ValueError:
                    age_days = None
                rec["age_days"] = round(age_days, 1) if age_days is not None else None
                if age_days is not None and age_days <= 7 and len(stations) >= 10:  # fresh and real
                    all_e10 += e10
                    all_b7 += b7
            except ValueError:
                rec["error"] = f"not JSON ({len(body)} bytes)"
        out["feeds"][name] = rec
        print(f"{name:22} {str(code):5} {rec['seconds']:5}s "
              f"stations={rec.get('stations')} E10 med={rec.get('e10_median')} "
              f"B7 med={rec.get('b7_median')} updated={rec.get('last_updated')} err={rec['error']}")
    if all_e10:
        out["national"] = {
            "e10_n": len(all_e10), "e10_median": round(statistics.median(all_e10), 1),
            "e10_p10": round(statistics.quantiles(all_e10, n=10)[0], 1),
            "e10_p90": round(statistics.quantiles(all_e10, n=10)[-1], 1),
            "b7_n": len(all_b7), "b7_median": round(statistics.median(all_b7), 1) if all_b7 else None,
        }
        print("national (feeds updated within 7 days, 10+ stations)", out["national"])
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w") as f:
            json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
