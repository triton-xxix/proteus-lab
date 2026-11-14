"""P-0450: order-book depth at the favourite degree on open Munich daily-high markets (Smarkets v3, keyless).

Markets: every "Highest Temperature" market_id in exchange/SNAPSHOTS.csv whose event_start is today or later.
For each, /markets/<id>/quotes/ gives every contract's bid and offer levels with quantity. Favourite = the
contract with the highest best bid (ties: lowest offer). Recorded: the first three offer levels at the
favourite, raw. Conversion (an assumption, stated in the README): Smarkets quantity is in 1/10,000 of a
contract and price in 1/100 of a percent, so a level's back stake in GBP = quantity * price / 1e8, and its
payout = quantity / 1e4. A 10 GBP back walks the offer levels from best upward; the average price paid is
reported against the best offer.
"""
import csv
import json
import pathlib
import time
import urllib.request
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).parent
API = "https://api.smarkets.com/v3"
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get(path):
    r = urllib.request.Request(API + path, headers={"User-Agent": "proteus-exchange/0.1", "Accept": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.load(resp)


markets = {}
for r in csv.DictReader(open("/Users/triton/PROTEUS/exchange/SNAPSHOTS.csv")):
    if r["market"] == "Highest Temperature" and r["event_start"][:10] >= today:
        markets[r["market_id"]] = r["event"]

out = {"pulled_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "markets": []}
for mid, ev in sorted(markets.items()):
    try:
        q = get(f"/markets/{mid}/quotes/")
    except Exception as e:
        out["markets"].append({"market_id": mid, "event": ev, "error": str(e)[:80]})
        continue
    time.sleep(0.5)
    best = None
    for cid, side in q.items():
        bids = sorted(side.get("bids", []), key=lambda x: -x["price"])
        offers = sorted([o for o in side.get("offers", []) if o["price"] < 9999], key=lambda x: x["price"])
        bb = bids[0]["price"] if bids else -1
        bo = offers[0]["price"] if offers else 99999
        key = (bb, -bo)
        if best is None or key > best[0]:
            best = (key, cid, bids, offers)
    if best is None:
        out["markets"].append({"market_id": mid, "event": ev, "contracts": 0})
        continue
    _, cid, bids, offers = best
    levels = [{"price_pct": o["price"] / 100, "quantity": o["quantity"], "stake_gbp": round(o["quantity"] * o["price"] / 1e8, 2)} for o in offers]
    need, spent, payout = 10.0, 0.0, 0.0
    for lv in levels:
        take = min(need - spent, lv["stake_gbp"])
        spent += take
        payout += take / (lv["price_pct"] / 100)
        if spent >= need - 1e-9:
            break
    avg = round(100 * spent / payout, 2) if payout else None
    out["markets"].append({"market_id": mid, "event": ev, "contracts": len(q), "favourite": cid,
                           "best_bid_pct": bids[0]["price"] / 100 if bids else None,
                           "offer_levels": levels[:3], "offer_levels_total": len(levels),
                           "stake_on_best_offer_gbp": levels[0]["stake_gbp"] if levels else 0,
                           "stake_on_all_offers_gbp": round(sum(l["stake_gbp"] for l in levels), 2),
                           "ten_gbp_back": {"filled_gbp": round(spent, 2), "avg_price_pct": avg,
                                            "best_offer_pct": levels[0]["price_pct"] if levels else None}})
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
