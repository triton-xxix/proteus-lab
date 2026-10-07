"""Free daily OHLC from Yahoo's chart endpoint, keyless. Writes sandbox/p0082/data/<SYM>.csv.

Columns: date, open, high, low, close, adjclose, volume. OHLC are as traded; adjclose carries
dividends and splits. Callers decide whether to scale OHLC by adjclose/close.
"""
import csv, json, os, sys, time, urllib.request
from datetime import datetime, timezone

OUT = "/Users/triton/PROTEUS/sandbox/p0082/data"
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}

for sym in sys.argv[1:]:
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=0&period2=%d&interval=1d&events=div%%2Csplit" % (sym, int(time.time()))
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
    r = d["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose") or q["close"]
    rows = 0
    with open(os.path.join(OUT, sym.replace("^", "") + ".csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "open", "high", "low", "close", "adjclose", "volume"])
        for i, ts in enumerate(r["timestamp"]):
            vals = [q["open"][i], q["high"][i], q["low"][i], q["close"][i], adj[i]]
            if any(v is None for v in vals):
                continue
            day = datetime.fromtimestamp(ts + r["meta"].get("gmtoffset", 0), tz=timezone.utc).date().isoformat()
            w.writerow([day] + ["%.6f" % v for v in vals] + [q["volume"][i] or 0])
            rows += 1
    print(sym, rows, "rows from", datetime.fromtimestamp(r["timestamp"][0], tz=timezone.utc).date())
    time.sleep(0.5)
