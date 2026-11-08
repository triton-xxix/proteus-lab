"""Log what has actually traded on each open Munich daily-high market, nightly. (P-0366, 8 Nov 2026.)

Smarkets' keyless API stops reporting a market's volume two or three days after it closes, and at
settlement every losing contract's last executed price is overwritten by a 0. So this has to run
before settlement. The nightly at about 22:30 UTC is before the day's 23:46 settlement print.

One row per market per run, appended to exchange/munich_volumes.jsonl. Prints one line for the run log.
"""
import csv, json, pathlib, time, urllib.error, urllib.request
from datetime import datetime, timedelta, timezone

HERE = pathlib.Path("/Users/triton/PROTEUS/exchange")
OUT = HERE / "munich_volumes.jsonl"
API = "https://api.smarkets.com/v3"
now = datetime.now(timezone.utc)


def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "proteus-exchange/0.1", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except (urllib.error.URLError, TimeoutError) as e:
        return {"error": str(e)[:80]}


markets = {}
for r in csv.DictReader(open(HERE / "SNAPSHOTS.csv")):
    if r["market"] == "Highest Temperature":
        markets[r["market_id"]] = (r["event"], r["event_start"])
for r in csv.DictReader(open(HERE / "BOOK.csv")):
    if r["market"] == "Highest Temperature":
        markets[r["market_id"]] = (r["event"], r["event_start"])

floor = now - timedelta(days=3)
book = {}
for r in csv.DictReader(open(HERE / "BOOK.csv")):
    book.setdefault(r["market_id"], set()).add(r["contract_id"])

n, total, errs, priced, priced_traded = 0, 0, 0, 0, 0
with open(OUT, "a") as f:
    for mid, (event, start) in sorted(markets.items()):
        if datetime.fromisoformat(start.replace("Z", "+00:00")) < floor:
            continue
        vol = get(f"/markets/{mid}/volumes/")
        lastx = get(f"/markets/{mid}/last_executed_prices/")
        time.sleep(0.3)
        if "error" in vol or "error" in lastx:
            errs += 1
            continue
        v = (vol.get("volumes") or [{}])[0]
        rows = (lastx.get("last_executed_prices") or {}).get(mid, [])
        # 0 and 100 are settlement prints, not trades
        traded = [{"contract_id": x["contract_id"], "price": x["last_executed_price"], "ts": x["timestamp"]}
                  for x in rows if x["last_executed_price"] not in ("0", "100")]
        ours = book.get(mid, set())
        hit = sorted(ours & {t["contract_id"] for t in traded})
        f.write(json.dumps({"snap_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "market_id": mid, "event": event, "event_start": start,
                            "reported": bool(vol.get("volumes")), "volume": v.get("volume"), "double_stake": v.get("double_stake_volume"),
                            "traded": traded, "book_contracts": sorted(ours), "book_contracts_traded": hit}) + "\n")
        n += 1
        total += v.get("volume") or 0
        priced += len(ours)
        priced_traded += len(hit)
print(f"Munich volumes: {n} markets logged, total volume {total}, book contracts with a visible trade {priced_traded} of {priced}, errors {errs}")
