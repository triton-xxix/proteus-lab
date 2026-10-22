"""P-0191: Kaggle Time Series lesson 4 says the partial autocorrelation picks the lags worth using.
Applied to the systems book: PACF of daily log returns for the nine index ETFs, on the same Yahoo
2y daily bars systems.py fetches (its own bars() function, imported). For each ETF: lags 1-10,
count outside the 95% band (+-1.96/sqrt(n)), the sign and size of lag 1, and whether lag 1 is
negative, which is the direction RSI(5) and IBS mean reversion bet on. Pure Python, no numpy.
Usage: python3 pacf.py
"""
import json
import math
import os
import sys
import time

sys.path.insert(0, "/Users/triton/PROTEUS/systems")
import systems  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-22-P-0191"
MAXLAG = 10


def acf(x, maxlag):
    n = len(x)
    m = sum(x) / n
    d = [v - m for v in x]
    c0 = sum(v * v for v in d) / n
    return [1.0] + [sum(d[i] * d[i - k] for i in range(k, n)) / n / c0 for k in range(1, maxlag + 1)]


def pacf(rho, maxlag):
    """Durbin-Levinson from the autocorrelations: phi_kk for k = 1..maxlag."""
    out = []
    phi_prev = []
    for k in range(1, maxlag + 1):
        if k == 1:
            phi_kk = rho[1]
            phi = [phi_kk]
        else:
            num = rho[k] - sum(phi_prev[j] * rho[k - 1 - j] for j in range(k - 1))
            den = 1 - sum(phi_prev[j] * rho[j + 1] for j in range(k - 1))
            phi_kk = num / den
            phi = [phi_prev[j] - phi_kk * phi_prev[k - 2 - j] for j in range(k - 1)] + [phi_kk]
        out.append(phi_kk)
        phi_prev = phi
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {"fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "markets": {}}
    for sym in systems.BASKET:
        b = systems.bars(sym)
        closes = [r[4] for r in b]
        rets = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
        n = len(rets)
        band = 1.96 / math.sqrt(n)
        rho = acf(rets, MAXLAG)
        p = pacf(rho, MAXLAG)
        outside = [k + 1 for k, v in enumerate(p) if abs(v) > band]
        res["markets"][sym] = {
            "bars": len(b), "first": b[0][0], "last": b[-1][0], "n_returns": n, "band": round(band, 4),
            "acf_1": round(rho[1], 4),
            "pacf": {str(k + 1): round(v, 4) for k, v in enumerate(p)},
            "lags_outside_95": outside, "n_outside": len(outside),
            "lag1_negative": p[0] < 0, "lag1_outside": abs(p[0]) > band,
        }
        print(sym, "n", n, "band", round(band, 4), "pacf1", round(p[0], 4), "outside", outside)
        time.sleep(1)
    ms = res["markets"]
    res["summary"] = {
        "etfs": len(ms),
        "lag1_negative": sum(1 for m in ms.values() if m["lag1_negative"]),
        "lag1_outside_band": sum(1 for m in ms.values() if m["lag1_outside"]),
        "mean_lags_outside_per_etf": round(sum(m["n_outside"] for m in ms.values()) / len(ms), 2),
        "chance_rate_per_etf": round(0.05 * MAXLAG, 2),
        "mean_pacf1": round(sum(m["pacf"]["1"] for m in ms.values()) / len(ms), 4),
        "pooled_lag_counts": {str(k): sum(1 for m in ms.values() if k in m["lags_outside_95"]) for k in range(1, MAXLAG + 1)},
    }
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=2)
    print(json.dumps(res["summary"], indent=1))


if __name__ == "__main__":
    main()
