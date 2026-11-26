"""P-0573 leg one: raw Yahoo v8 chart 60d/5m for the 12 scan.py stocks, saved with pull time.
Usage: python3 pull.py OUTDIR  (leg two runs the same into another folder and diffs)."""
import json, sys, time, urllib.request, datetime as dt, os

STOCKS = ["SPY", "QQQ", "IWM", "TSLA", "NVDA", "META", "AMD", "AAPL", "AMZN", "MSFT", "GOOGL", "NFLX"]
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
summary = {"pulled_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "symbols": {}}
for s in STOCKS:
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?range=60d&interval=5m" % s
    try:
        raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read()
        j = json.loads(raw)
        r = j["chart"]["result"][0]
        ts = r["timestamp"]
        q = r["indicators"]["quote"][0]
        nulls = sum(1 for c in q["close"] if c is None)
        open(os.path.join(out, s + ".json"), "wb").write(raw)
        summary["symbols"][s] = {"bars": len(ts), "first": dt.datetime.utcfromtimestamp(ts[0]).isoformat(),
                                 "last": dt.datetime.utcfromtimestamp(ts[-1]).isoformat(), "null_closes": nulls,
                                 "bytes": len(raw)}
    except Exception as e:
        summary["symbols"][s] = {"error": repr(e)}
    print(s, summary["symbols"][s])
    time.sleep(1)
json.dump(summary, open(os.path.join(out, "summary.json"), "w"), indent=1)
