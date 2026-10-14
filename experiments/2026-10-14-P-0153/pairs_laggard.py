"""P-0153: long-only laggard of a matched crypto pair, after fees, against random entries.

Rules fixed before the first run (14 Oct 2026, nightly):
- 12 liquid USDT spot coins, 90 days of hourly closes from Binance's keyless data API.
- Formation: first 30 days. A pair qualifies if hourly-return correlation >= 0.70.
- Trading: last 60 days. Spread = log(A) - log(B); z on a rolling 168 h mean and sd.
  z <= -2: A is the laggard, buy A. z >= +2: buy B. One open trade per pair.
- Exit when z crosses back through 0, or after 48 h. Fee 0.2% round trip (0.1% a side).
- Benchmark: for each trade, 500 random entries on the same coin in the trading window with the
  same holding length, same fee. p = share of shuffled books whose mean beats the real mean.
"""
import json
import random
import sys
import urllib.request
from itertools import combinations
from pathlib import Path

import numpy as np

OUT = Path(sys.argv[1])
COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "AVAX", "LINK", "LTC", "DOT", "TRX"]
H = 24 * 90
FEE = 0.002


def klines(sym):
    rows, end = [], None
    while len(rows) < H:
        url = f"https://data-api.binance.vision/api/v3/klines?symbol={sym}USDT&interval=1h&limit=1000"
        if end:
            url += f"&endTime={end}"
        batch = json.load(urllib.request.urlopen(url, timeout=30))
        if not batch:
            break
        rows = batch + rows
        end = batch[0][0] - 1
    rows = rows[-H:]
    return [r[0] for r in rows], np.array([float(r[4]) for r in rows])


data = {}
for c in COINS:
    t, px = klines(c)
    data[c] = (t, px)
t0 = data["BTC"][0]
assert all(data[c][0] == t0 for c in COINS), "timestamps differ"
P = {c: data[c][1] for c in COINS}
F = 24 * 30
rets = {c: np.diff(np.log(P[c])) for c in COINS}

pairs = []
for a, b in combinations(COINS, 2):
    r = np.corrcoef(rets[a][:F], rets[b][:F])[0, 1]
    if r >= 0.70:
        pairs.append((a, b, round(float(r), 3)))

trades = []
for a, b, r in pairs:
    s = np.log(P[a]) - np.log(P[b])
    i = F
    while i < H - 1:
        w = s[i - 168:i]
        z = (s[i] - w.mean()) / w.std()
        if abs(z) >= 2:
            coin = a if z < 0 else b
            sign = np.sign(z)
            j = i + 1
            while j < H - 1 and j - i < 48:
                w2 = s[j - 168:j]
                zj = (s[j] - w2.mean()) / w2.std()
                if np.sign(zj) != sign:
                    break
                j += 1
            ret = P[coin][j] / P[coin][i] * (1 - FEE / 2) ** 2 - 1
            trades.append({"pair": f"{a}-{b}", "coin": coin, "i": i, "hold": j - i, "z": round(float(z), 2), "ret": float(ret)})
            i = j + 1
        else:
            i += 1

real = np.array([t["ret"] for t in trades])
rng = random.Random(14)
shuffled = []
for _ in range(500):
    rs = []
    for t in trades:
        k = rng.randrange(F, H - t["hold"])
        rs.append(P[t["coin"]][k + t["hold"]] / P[t["coin"]][k] * (1 - FEE / 2) ** 2 - 1)
    shuffled.append(np.mean(rs))
shuffled = np.array(shuffled)
p = float((shuffled >= real.mean()).mean())

res = {
    "window_start_ms": t0[0], "window_end_ms": t0[-1], "pairs": pairs, "n_trades": len(trades),
    "mean_trade_pct": round(100 * real.mean(), 3), "median_trade_pct": round(100 * float(np.median(real)), 3),
    "win_rate": round(float((real > 0).mean()), 3), "sum_pct": round(100 * real.sum(), 2),
    "random_mean_pct": round(100 * shuffled.mean(), 3), "p_random_beats": p,
    "mean_hold_h": round(float(np.mean([t["hold"] for t in trades])), 1),
    "time_stops": sum(t["hold"] >= 48 for t in trades),
    "btc_eth": [t for t in trades if t["pair"] == "BTC-ETH"],
    "per_pair": {pr: {"n": len(v), "mean_pct": round(100 * float(np.mean(v)), 3)} for pr, v in
                 {pr: [t["ret"] for t in trades if t["pair"] == pr] for pr in {t["pair"] for t in trades}}.items()},
}
(OUT / "results.json").write_text(json.dumps(res, indent=1))
print({k: v for k, v in res.items() if k not in ("btc_eth", "per_pair", "pairs")})
print("pairs", len(pairs), "btc-eth trades", len(res["btc_eth"]))
