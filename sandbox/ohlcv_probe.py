"""What GeckoTerminal's keyless OHLCV actually serves for a pool a day old: resolution, reach, gaps, rate."""
import time
import requests

GT = "https://api.geckoterminal.com/api/v2/networks/solana/pools/"
POOL = "Hhe2TY1dGPr7SdMJC2hTACq7dTxfr5f6BF3n2nWwkoce"  # FUNKOS pumpswap, G-0001
for tf, agg in (("minute", 1), ("minute", 5), ("hour", 1)):
    t0 = time.time()
    r = requests.get(GT + POOL + "/ohlcv/" + tf, params={"aggregate": agg, "limit": 1000, "currency": "usd", "token": "base"},
                     headers={"Accept": "application/json"}, timeout=30)
    dt = time.time() - t0
    if r.status_code != 200:
        print(tf, agg, "HTTP", r.status_code, r.text[:200]); continue
    j = r.json()
    rows = j["data"]["attributes"]["ohlcv_list"]  # [ts, o, h, l, c, v], newest first
    ts = sorted(x[0] for x in rows)
    gaps = [b - a for a, b in zip(ts, ts[1:])]
    step = 60 * agg * (60 if tf == "hour" else 1)
    print("%s/%d: %d candles in %.2fs, from %s to %s, missing steps %d, largest gap %d min, meta %s" % (
        tf, agg, len(rows), dt, time.strftime("%m-%d %H:%M", time.gmtime(ts[0])), time.strftime("%m-%d %H:%M", time.gmtime(ts[-1])),
        sum(1 for g in gaps if g > step), max(gaps) // 60 if gaps else 0, j.get("meta", {}).get("base", {}).get("symbol")))
    time.sleep(2.5)

# how far back does minute data reach? page with before_timestamp from the entry time
entry = 1790235367  # 2026-09-24T07:36:07Z
r = requests.get(GT + POOL + "/ohlcv/minute", params={"aggregate": 1, "limit": 1000, "currency": "usd", "token": "base",
                 "before_timestamp": entry + 1000 * 60}, timeout=30)
rows = r.json()["data"]["attributes"]["ohlcv_list"] if r.status_code == 200 else []
print("paged from entry:", r.status_code, len(rows), "candles",
      time.strftime("%m-%d %H:%M", time.gmtime(min(x[0] for x in rows))) if rows else "-", "to",
      time.strftime("%m-%d %H:%M", time.gmtime(max(x[0] for x in rows))) if rows else "-")
lo = min(rows, key=lambda x: x[3]) if rows else None
if lo:
    print("lowest low in that page %.3g at %s; entry price 0.0004064; stop level 0.0002032" % (lo[3], time.strftime("%m-%d %H:%M", time.gmtime(lo[0]))))
    first = sorted(rows)
    hit = next((x for x in first if x[0] >= entry and x[3] <= 0.0002032), None)
    print("first minute candle at or after entry with low <= stop:", hit and (time.strftime("%m-%d %H:%M", time.gmtime(hit[0])), hit[1:5]))
