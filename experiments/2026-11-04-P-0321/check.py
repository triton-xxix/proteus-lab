"""P-0321: P-0314's question on the pre-2009 cuts. On each Fed target cut in FRED DFEDTAR (single target,
to 16 Dec 2008; sandbox/fred-dfedtar.csv pulled 4 Nov 2026), was SPY above its SMA200 and up over 20 days on the
decision day (last SPY trading day before FRED's effective date)? Random-day control: 10,000 draws of the
same count of SPY trading days from the same span, the share with both conditions, two-sided permutation p.

    python3 -I experiments/2026-11-04-P-0321/check.py
"""
import csv
import datetime
import json
import pathlib
import random
import urllib.request

OUT = pathlib.Path(__file__).parent
UA = {"User-Agent": "Mozilla/5.0 proteus-research"}

cuts, prev = [], None
for row in list(csv.reader(open("/Users/triton/PROTEUS/sandbox/fred-dfedtar.csv")))[1:]:
    if not row[1] or row[1] == ".":
        continue
    v = float(row[1])
    if prev is not None and v < prev:
        cuts.append((row[0], prev, v))
    prev = v

p1 = int(datetime.datetime(1993, 1, 1).timestamp())
p2 = int(datetime.datetime(2009, 3, 1).timestamp())
url = "https://query1.finance.yahoo.com/v8/finance/chart/SPY?period1=%d&period2=%d&interval=1d" % (p1, p2)
res = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))["chart"]["result"][0]
dates = [datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d") for t in res["timestamp"]]
close = res["indicators"]["adjclose"][0]["adjclose"]
first_ok = 200  # first index with a full SMA200 and 20-day look-back


def state(i):
    sma = sum(close[i - 199:i + 1]) / 200
    return close[i] > sma, close[i] / close[i - 20] - 1 > 0, (close[i] / sma - 1) * 100, (close[i] / close[i - 20] - 1) * 100


rows = []
for eff, a, b in cuts:
    earlier = [k for k, d in enumerate(dates) if d < eff]
    if not earlier or earlier[-1] < first_ok:
        continue
    i = earlier[-1]
    above, up, pct, r20 = state(i)
    after = (close[i + 20] / close[i] - 1) * 100 if i + 20 < len(close) else None
    rows.append({"effective": eff, "decision_day": dates[i], "from": a, "to": b, "above_sma200": above,
                 "uptrend_20d": up, "pct_vs_sma200": round(pct, 1), "ret_20d_before": round(r20, 1),
                 "ret_20d_after": None if after is None else round(after, 1)})
for r in rows:
    print(r)
n = len(rows)
both = sum(r["above_sma200"] and r["uptrend_20d"] for r in rows)
lo = min(k for k, d in enumerate(dates) if d >= rows[0]["decision_day"])
hi = max(k for k, d in enumerate(dates) if d <= rows[-1]["decision_day"])
pool = [state(i)[0] and state(i)[1] for i in range(lo, hi + 1)]
base = sum(pool) / len(pool)
rng = random.Random(4)
draws = [sum(rng.choice(pool) for _ in range(n)) for _ in range(10000)]
p_low = sum(1 for d in draws if d <= both) / 10000
summ = {"cuts_in_span": n, "first": rows[0]["decision_day"], "last": rows[-1]["decision_day"],
        "cuts_dropped_before_spy_sma": len(cuts) - n,
        "above_sma200": sum(r["above_sma200"] for r in rows), "uptrend_20d": sum(r["uptrend_20d"] for r in rows),
        "both": both, "both_share": round(both / n, 3), "random_day_both_share": round(base, 3),
        "p_as_low_or_lower": p_low, "p_two_sided": round(min(1.0, 2 * min(p_low, 1 - p_low + sum(1 for d in draws if d == both) / 10000)), 4),
        "mean_20d_after": round(sum(r["ret_20d_after"] for r in rows if r["ret_20d_after"] is not None) / n, 2)}
print(json.dumps(summ))
(OUT / "results.json").write_text(json.dumps({"summary": summ, "rows": rows}, indent=1))
