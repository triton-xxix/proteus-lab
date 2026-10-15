"""P-0158: P-0153's frozen pairs-laggard rules out of sample, with a day-block shuffle.

Rules are P-0153's, unchanged (12 coins, 90 days hourly, 30-day formation at corr >= 0.70, 60-day
trading, 168 h rolling z, enter |z| >= 2, exit z through 0 or 48 h, 0.2% round trip).

New here, fixed before the first run (15 Oct 2026, Trials):
- Window: the 90 days ending the hour before P-0153's window opened (17 Jul 2026), so no overlap.
  The in-sample window is re-run too, as a check that this code reproduces P-0153.
- Two benchmarks, 2000 books each:
  1. per-trade: P-0153's own, each trade re-entered at an independent random hour (same coin, hold).
  2. day-block: trades grouped by entry day; each book moves every trade of one entry day by the same
     random whole-day offset (keeping hour of day), so trades that overlap in time stay together.
  p = share of books whose mean trade >= the real mean.
- Verdict line: works only if out of sample mean beats random by >= 0.3 pp AND day-block p < 0.10.
"""
import json
import random
import sys
import urllib.request
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

OUT = Path(sys.argv[1])
P153 = json.loads(Path("/Users/triton/PROTEUS/experiments/2026-10-14-P-0153/results.json").read_text())
COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "AVAX", "LINK", "LTC", "DOT", "TRX"]
H = 24 * 90
F = 24 * 30
FEE = 0.002
BOOKS = 2000


def klines(sym, end_ms):
    rows, end = [], end_ms
    while len(rows) < H:
        url = f"https://data-api.binance.vision/api/v3/klines?symbol={sym}USDT&interval=1h&limit=1000&endTime={end}"
        batch = json.load(urllib.request.urlopen(url, timeout=30))
        if not batch:
            break
        rows = batch + rows
        end = batch[0][0] - 1
    rows = rows[-H:]
    return [r[0] for r in rows], np.array([float(r[4]) for r in rows])


def run(end_ms, seed):
    data = {c: klines(c, end_ms) for c in COINS}
    t0 = data["BTC"][0]
    assert len(t0) == H and all(data[c][0] == t0 for c in COINS), "timestamps differ"
    P = {c: data[c][1] for c in COINS}
    rets = {c: np.diff(np.log(P[c])) for c in COINS}
    pairs = []
    for a, b in combinations(COINS, 2):
        r = np.corrcoef(rets[a][:F], rets[b][:F])[0, 1]
        if r >= 0.70:
            pairs.append((a, b, round(float(r), 3)))
    trades = []
    for a, b, _ in pairs:
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
                    if np.sign((s[j] - w2.mean()) / w2.std()) != sign:
                        break
                    j += 1
                ret = P[coin][j] / P[coin][i] * (1 - FEE / 2) ** 2 - 1
                trades.append({"pair": f"{a}-{b}", "coin": coin, "i": i, "hold": j - i, "ret": float(ret)})
                i = j + 1
            else:
                i += 1
    real = np.array([t["ret"] for t in trades])

    def ret_at(t, k):
        return P[t["coin"]][k + t["hold"]] / P[t["coin"]][k] * (1 - FEE / 2) ** 2 - 1

    rng = random.Random(seed)
    per_trade = np.array([np.mean([ret_at(t, rng.randrange(F, H - t["hold"])) for t in trades]) for _ in range(BOOKS)])

    by_day = defaultdict(list)
    for t in trades:
        by_day[(t["i"] - F) // 24].append(t)
    n_days = (H - F) // 24
    block = []
    for _ in range(BOOKS):
        rs = []
        for day, ts in by_day.items():
            nd = rng.randrange(n_days)
            for t in ts:
                k = F + nd * 24 + (t["i"] - F) % 24
                k = min(k, H - 1 - t["hold"])
                rs.append(ret_at(t, k))
        block.append(np.mean(rs))
    block = np.array(block)

    hold_coin = {c: round(100 * float(P[c][-1] / P[c][F] - 1), 2) for c in COINS}
    return {
        "window_start_ms": t0[0], "window_end_ms": t0[-1], "n_pairs": len(pairs), "pairs": pairs,
        "n_trades": len(trades), "entry_days": len(by_day),
        "mean_trade_pct": round(100 * real.mean(), 3), "median_trade_pct": round(100 * float(np.median(real)), 3),
        "win_rate": round(float((real > 0).mean()), 3) if len(real) else None,
        "random_mean_pct": round(100 * per_trade.mean(), 3),
        "edge_pp": round(100 * (real.mean() - per_trade.mean()), 3),
        "p_per_trade": float((per_trade >= real.mean()).mean()),
        "p_day_block": float((block >= real.mean()).mean()),
        "block_sd_pct": round(100 * float(block.std()), 3), "per_trade_sd_pct": round(100 * float(per_trade.std()), 3),
        "trading_window_hold_pct": hold_coin,
        "per_pair": {pr: {"n": len(v), "mean_pct": round(100 * float(np.mean(v)), 3)} for pr, v in
                     {pr: [t["ret"] for t in trades if t["pair"] == pr] for pr in {t["pair"] for t in trades}}.items()},
    }


res = {
    "out_of_sample": run(P153["window_start_ms"] - 1, 15),
    "in_sample_recheck": run(P153["window_end_ms"], 16),
}
(OUT / "results.json").write_text(json.dumps(res, indent=1))
for k, v in res.items():
    print(k, {x: y for x, y in v.items() if x not in ("pairs", "per_pair", "trading_window_hold_pct")})
