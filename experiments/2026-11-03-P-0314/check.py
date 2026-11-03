"""P-0314: on each Fed target cut in FRED DFEDTARU (series starts 16 Dec 2008), was SPY above its SMA200 and in a
20-day uptrend on the decision day? Decision day = the last SPY trading day before FRED's effective date
(effective is the day after the statement; the 15 Mar 2020 Sunday cut maps to Fri 13 Mar).
Also: the systems book's RSI(5) < 30 on that day, and SPY's 20-day return after."""
import csv, json, urllib.request, datetime, pathlib

OUT = pathlib.Path(__file__).parent
FRED = "/Users/triton/PROTEUS/sandbox/fred-dfedtaru.csv"
UA = {"User-Agent": "Mozilla/5.0 proteus-research"}

cuts, prev = [], None
for row in list(csv.reader(open(FRED)))[1:]:
    if not row[1]:
        continue
    v = float(row[1])
    if prev is not None and v < prev:
        cuts.append((row[0], prev, v))
    prev = v

p1 = int(datetime.datetime(2007, 1, 1).timestamp())
p2 = int(datetime.datetime.now().timestamp())
url = f"https://query1.finance.yahoo.com/v8/finance/chart/SPY?period1={p1}&period2={p2}&interval=1d"
res = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))["chart"]["result"][0]
dates = [datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d") for t in res["timestamp"]]
close = res["indicators"]["adjclose"][0]["adjclose"]

def rsi(i, n=5):
    gains = losses = 0.0
    # Wilder smoothing seeded over the prior 100 days, as close to systems.py as a quick check needs
    start = max(1, i - 100)
    ag = al = None
    for k in range(start, i + 1):
        ch = close[k] - close[k - 1]
        g, l = max(ch, 0), max(-ch, 0)
        if ag is None:
            ag, al = g, l
        else:
            ag = (ag * (n - 1) + g) / n
            al = (al * (n - 1) + l) / n
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)

rows = []
for eff, a, b in cuts:
    i = max(k for k, d in enumerate(dates) if d < eff)
    sma = sum(close[i - 199:i + 1]) / 200
    r20b = close[i] / close[i - 20] - 1
    r20a = close[i + 20] / close[i] - 1 if i + 20 < len(close) else None
    rows.append({"effective": eff, "decision_day": dates[i], "from": a, "to": b,
                 "above_sma200": close[i] > sma, "pct_vs_sma200": round((close[i] / sma - 1) * 100, 1),
                 "ret_20d_before": round(r20b * 100, 1), "uptrend_20d": r20b > 0,
                 "rsi5": round(rsi(i), 1), "ret_20d_after": None if r20a is None else round(r20a * 100, 1)})

for r in rows:
    print(r)
n = len(rows)
both = sum(r["above_sma200"] and r["uptrend_20d"] for r in rows)
summ = {"cuts": n, "above_sma200": sum(r["above_sma200"] for r in rows), "uptrend_20d": sum(r["uptrend_20d"] for r in rows),
        "both": both, "rsi5_below_30": sum(r["rsi5"] < 30 for r in rows),
        "mean_20d_after": round(sum(r["ret_20d_after"] for r in rows if r["ret_20d_after"] is not None) / n, 2)}
print(json.dumps(summ))
(OUT / "results.json").write_text(json.dumps({"summary": summ, "rows": rows}, indent=1))
