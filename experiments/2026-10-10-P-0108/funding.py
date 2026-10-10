"""P-0108: do extreme perp funding readings predict next-7-day SPOT returns? BTC and ETH, 2022 on.

Fixed before the run:
  Funding  Binance USD-M fundingRate history (keyless), summed per UTC day (three readings).
  Extreme  today's daily funding against the trailing 180 days only (no look-ahead): top decile = high,
           bottom decile = low. Days with fewer than 180 prior days are skipped.
  Return   spot close (Binance spot daily klines) from that day's close to 7 days later. Spot only.
  Luck     5,000 draws of the same number of days from all eligible days; p = share of draws with a mean
           at or below (high) or at or above (low) the real mean. Overlapping 7-day windows make
           neighbouring days near copies, so p is optimistic; I also report non-overlapping counts.
"""
import json
import time
import urllib.request

import numpy as np
import pandas as pd

OUT = "/Users/triton/PROTEUS/experiments/2026-10-10-P-0108/"
START_MS = int(pd.Timestamp("2021-06-01", tz="UTC").timestamp() * 1000)


def getj(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-p0108"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def funding(sym):
    rows, start = [], START_MS
    while True:
        d = getj("https://fapi.binance.com/fapi/v1/fundingRate?symbol=%s&startTime=%d&limit=1000" % (sym, start))
        if not d:
            break
        rows += d
        if len(d) < 1000:
            break
        start = d[-1]["fundingTime"] + 1
        time.sleep(0.3)
    f = pd.DataFrame(rows)
    f["day"] = pd.to_datetime(f["fundingTime"], unit="ms", utc=True).dt.floor("D")
    return f.assign(r=f["fundingRate"].astype(float)).groupby("day")["r"].sum()


def spot(sym):
    rows, start = [], START_MS
    while True:
        d = getj("https://api.binance.com/api/v3/klines?symbol=%s&interval=1d&startTime=%d&limit=1000" % (sym, start))
        if not d:
            break
        rows += d
        if len(d) < 1000:
            break
        start = d[-1][0] + 1
        time.sleep(0.3)
    s = pd.Series([float(k[4]) for k in rows], index=pd.to_datetime([k[0] for k in rows], unit="ms", utc=True))
    return s


def main():
    rng = np.random.default_rng(108)
    res = {}
    for sym in ("BTCUSDT", "ETHUSDT"):
        fd, px = funding(sym), spot(sym)
        df = pd.DataFrame({"f": fd, "c": px}).dropna()
        df["fwd7"] = df["c"].shift(-7) / df["c"] - 1
        hi_th = df["f"].rolling(180, min_periods=180).quantile(0.9).shift(1)
        lo_th = df["f"].rolling(180, min_periods=180).quantile(0.1).shift(1)
        df = df[(df.index >= "2022-01-01") & hi_th.reindex(df.index).notna() & df["fwd7"].notna()]
        hi = df["f"] >= hi_th.reindex(df.index)
        lo = df["f"] <= lo_th.reindex(df.index)
        allr = df["fwd7"].to_numpy()
        out = {"days": int(len(df)), "span": [str(df.index[0].date()), str(df.index[-1].date())],
               "all_mean_pct": round(float(allr.mean() * 100), 3)}
        for name, mask, side in (("high_funding", hi, "below"), ("low_funding", lo, "above")):
            x = df.loc[mask, "fwd7"].to_numpy()
            draws = np.array([allr[rng.choice(allr.size, x.size, replace=False)].mean() for _ in range(5000)])
            p = (draws <= x.mean()).mean() if side == "below" else (draws >= x.mean()).mean()
            days = df.index[mask]
            nonover, last = 0, None
            for d in days:
                if last is None or (d - last).days >= 7:
                    nonover += 1
                    last = d
            out[name] = {"n": int(x.size), "non_overlapping": nonover, "mean_pct": round(float(x.mean() * 100), 3),
                         "win_pct": round(float((x > 0).mean() * 100), 1), "p_" + side: round(float(p), 4)}
        res[sym] = out
        print(sym, out)
    json.dump(res, open(OUT + "results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
