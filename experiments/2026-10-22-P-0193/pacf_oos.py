"""P-0193: P-0191 out of sample. Same nine ETFs, Yahoo chart endpoint with range=5y (the only change
from systems.bars(): the range), split into the prior window 2022-10-23 to 2024-10-22 and the
live window 2024-10-23 on. PACF lags 1-10 by Durbin-Levinson on daily log returns, 95% band
+-1.96/sqrt(n). Question: does lag 3 stay outside the band in 4 of 9, and lag 1 negative in 9 of 9?
Usage: python3 pacf_oos.py
"""
import json
import math
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, "/Users/triton/PROTEUS/systems")
import systems  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-22-P-0193"
MAXLAG = 10
SPLIT = "2024-10-23"
START = "2022-10-23"


def bars5y(sym):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?range=5y&interval=1d" % sym
    for attempt in range(3):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    r = d["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    off = r["meta"].get("gmtoffset", 0)
    out = []
    for i, ts in enumerate(r["timestamp"]):
        c = q["close"][i]
        if c is None:
            continue
        out.append((datetime.fromtimestamp(ts + off, tz=timezone.utc).date().isoformat(), float(c)))
    return out


def acf(x, maxlag):
    n = len(x)
    m = sum(x) / n
    d = [v - m for v in x]
    c0 = sum(v * v for v in d) / n
    return [1.0] + [sum(d[i] * d[i - k] for i in range(k, n)) / n / c0 for k in range(1, maxlag + 1)]


def pacf(rho, maxlag):
    out, phi_prev = [], []
    for k in range(1, maxlag + 1):
        if k == 1:
            phi_kk, phi = rho[1], [rho[1]]
        else:
            num = rho[k] - sum(phi_prev[j] * rho[k - 1 - j] for j in range(k - 1))
            den = 1 - sum(phi_prev[j] * rho[j + 1] for j in range(k - 1))
            phi_kk = num / den
            phi = [phi_prev[j] - phi_kk * phi_prev[k - 2 - j] for j in range(k - 1)] + [phi_kk]
        out.append(phi_kk)
        phi_prev = phi
    return out


def window(closes_dated, lo, hi):
    cs = [c for d, c in closes_dated if lo <= d < hi]
    rets = [math.log(cs[i] / cs[i - 1]) for i in range(1, len(cs))]
    n = len(rets)
    band = 1.96 / math.sqrt(n)
    p = pacf(acf(rets, MAXLAG), MAXLAG)
    outside = [k + 1 for k, v in enumerate(p) if abs(v) > band]
    return {"n_returns": n, "band": round(band, 4), "pacf": {str(k + 1): round(v, 4) for k, v in enumerate(p)},
            "lags_outside_95": outside, "lag1_negative": p[0] < 0, "lag3_outside": 3 in outside,
            "lag1_outside": 1 in outside}


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {"fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "markets": {}}
    for sym in systems.BASKET:
        b = bars5y(sym)
        res["markets"][sym] = {"bars_5y": len(b), "first": b[0][0], "last": b[-1][0],
                               "prior": window(b, START, SPLIT), "live": window(b, SPLIT, "2099")}
        pr, lv = res["markets"][sym]["prior"], res["markets"][sym]["live"]
        print(sym, "prior n", pr["n_returns"], "pacf1", pr["pacf"]["1"], "pacf3", pr["pacf"]["3"], "outside", pr["lags_outside_95"],
              "| live pacf1", lv["pacf"]["1"], "outside", lv["lags_outside_95"])
        time.sleep(1)
    ms = res["markets"]
    for w in ("prior", "live"):
        res["summary_" + w] = {
            "lag1_negative": sum(1 for m in ms.values() if m[w]["lag1_negative"]),
            "lag1_outside": sum(1 for m in ms.values() if m[w]["lag1_outside"]),
            "lag3_outside": sum(1 for m in ms.values() if m[w]["lag3_outside"]),
            "mean_pacf1": round(sum(m[w]["pacf"]["1"] for m in ms.values()) / 9, 4),
            "mean_pacf3": round(sum(m[w]["pacf"]["3"] for m in ms.values()) / 9, 4),
            "mean_lags_outside_per_etf": round(sum(len(m[w]["lags_outside_95"]) for m in ms.values()) / 9, 2),
            "pooled_lag_counts": {str(k): sum(1 for m in ms.values() if k in m[w]["lags_outside_95"]) for k in range(1, MAXLAG + 1)},
        }
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=2)
    print(json.dumps({"prior": res["summary_prior"], "live": res["summary_live"]}, indent=1))


if __name__ == "__main__":
    main()
