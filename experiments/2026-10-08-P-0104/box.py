"""P-0104: the five-rule 15m/5m box strategy on two years of BTCUSDT, after costs.

The reel's five rules, made mechanical before the first run (my reading where the reel is loose):
1. Bias from 15m: the last completed 15m close above its 50-period EMA allows longs only; below, shorts only.
2. Impulse box on 5m: a three-candle fair-value gap. Short: candle 3's high below candle 1's low; the
   box is [candle 3 high, candle 1 low]. Long is the mirror.
3. The impulse must break structure: candle 2 closes below the last 5m fractal swing low (2 bars each
   side, known 2 bars after) for a short; above the last swing high for a long.
4. Return to the box, then entry: the first candle to trade into the box is candle A; enter at the close
   of the first later candle that closes below candle A's low (short) or above its high (long).
   Stop at candle A's high (short) or low (long). Void if a candle closes beyond the box's far edge
   before entry, or 48 bars (4 hours) pass after the box without entry.
5. Take profit at 2R. Stop first if both hit in one bar. 288 bars maximum, then out at the close.
One live setup per side at a time. Costs 0.10% of price per round trip, charged in R.
"""
import json
import pathlib
import statistics
import time
import urllib.request
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).parent
COST = 0.001


def fetch():
    out = []
    t = int(datetime(2024, 10, 8, tzinfo=timezone.utc).timestamp() * 1000)
    end = int(datetime(2026, 10, 8, tzinfo=timezone.utc).timestamp() * 1000)
    while t < end:
        url = "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000&startTime=%d" % t
        rows = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
        if not rows:
            break
        out += [(r[0], float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if r[0] < end]
        t = rows[-1][0] + 1
        time.sleep(0.05)
    return out


def main():
    b = fetch()
    n = len(b)
    # 15m closes and EMA50, known at the close of each 15m block
    bias = [0] * n
    ema, k = None, 2 / 51
    cnt = 0
    for i in range(n):
        if (b[i][0] // 60000) % 15 == 10:  # last 5m bar of a 15m block
            c = b[i][4]
            ema = c if ema is None else ema + k * (c - ema)
            cnt += 1
            cur = (1 if c > ema else -1) if cnt > 50 else 0
        bias[i] = cur if cnt > 50 else 0
    sh = [False] * n
    sl = [False] * n
    for i in range(2, n - 2):
        sh[i] = b[i][2] > max(b[i - 2][2], b[i - 1][2], b[i + 1][2], b[i + 2][2])
        sl[i] = b[i][3] < min(b[i - 2][3], b[i - 1][3], b[i + 1][3], b[i + 2][3])
    last_h = last_l = None
    trades = []
    setup = {1: None, -1: None}
    busy_until = -1
    for i in range(4, n - 1):
        kk = i - 2
        if sh[kk]:
            last_h = b[kk][2]
        if sl[kk]:
            last_l = b[kk][3]
        t, o, h, l, c = b[i]
        # new boxes formed by candles i-2, i-1, i
        if last_l is not None and bias[i] < 0 and b[i][2] < b[i - 2][3] and b[i - 1][4] < last_l:
            setup[-1] = {"top": b[i - 2][3], "bot": b[i][2], "made": i, "A": None}
        if last_h is not None and bias[i] > 0 and b[i][3] > b[i - 2][2] and b[i - 1][4] > last_h:
            setup[1] = {"top": b[i][3], "bot": b[i - 2][2], "made": i, "A": None}
        for side in (1, -1):
            s = setup[side]
            if not s or s["made"] == i:
                continue
            if i - s["made"] > 48 or (side < 0 and c > s["top"]) or (side > 0 and c < s["bot"]):
                setup[side] = None
                continue
            if s["A"] is None:
                if (side < 0 and h >= s["bot"]) or (side > 0 and l <= s["top"]):
                    s["A"] = (h, l)
                continue
            ah, al = s["A"]
            if i <= busy_until:
                continue
            if (side < 0 and c < al) or (side > 0 and c > ah):
                entry, stop = c, (ah if side < 0 else al)
                risk = abs(entry - stop)
                setup[side] = None
                if risk < entry * 0.0003:
                    continue
                tgt = entry + 2 * risk * side
                r = None
                for j in range(i + 1, min(i + 289, n)):
                    _, oo, hh, ll, cc = b[j]
                    if (side > 0 and ll <= stop) or (side < 0 and hh >= stop):
                        r = -1.0
                        break
                    if (side > 0 and hh >= tgt) or (side < 0 and ll <= tgt):
                        r = 2.0
                        break
                if r is None:
                    j = min(i + 288, n - 1)
                    r = (b[j][4] - entry) / risk * side
                busy_until = j
                trades.append({"t": datetime.fromtimestamp(t / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M"),
                               "side": side, "gross_R": round(r, 3), "net_R": round(r - COST * entry / risk, 3),
                               "risk_pct": round(100 * risk / entry, 3)})
    g = [x["gross_R"] for x in trades]
    m = [x["net_R"] for x in trades]
    half = len(trades) // 2
    res = {"bars": n, "trades": len(trades),
           "win_rate": round(sum(x > 0 for x in g) / len(g), 3) if g else None,
           "mean_gross_R": round(statistics.mean(g), 3) if g else None,
           "mean_net_R": round(statistics.mean(m), 3) if m else None,
           "median_risk_pct": round(statistics.median(x["risk_pct"] for x in trades), 3) if trades else None,
           "first_half_trades_net_R": round(statistics.mean(m[:half]), 3) if half else None,
           "second_half_trades_net_R": round(statistics.mean(m[half:]), 3) if half else None}
    print(json.dumps(res))
    (HERE / "result.json").write_text(json.dumps(res, indent=1))
    (HERE / "trades.json").write_text(json.dumps(trades))


if __name__ == "__main__":
    main()
