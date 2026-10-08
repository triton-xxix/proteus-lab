"""P-0103: does waiting for one extra sweep (an "inducement") after a structure shift beat entering
on the shift itself? BTCUSDT 5m, Binance, last 90 days to 8 Oct 2026.

Rules, fixed before the first run:
- Swing high/low: a 5-bar fractal (2 bars each side), known 2 bars after it prints.
- Bullish shift: structure was bearish (last known swing low below the one before it) and a bar
  closes above the last known swing high. Bearish shift is the mirror. One shift per swing.
- A (shift entry): buy at the next bar's open. Stop at the lowest low between the last swing low and
  the shift bar. Target 2R. Exit at stop or target, stop first if both in one bar; 288 bars (a day)
  maximum, then out at that close.
- B (inducement entry): after the same shift, wait for the first swing low that forms after the shift
  (a pullback). Then wait for a bar whose low trades below that pullback low and whose close is back
  above it (the sweep). Buy at the next bar's open, stop at that sweep bar's low, target 2R, same
  exits. Abandon if A's stop is hit first or 288 bars pass with no sweep.
- Costs: 0.10% of price per round trip, charged in R (cost / risk distance).
Prints trades, win rate and mean R after costs for both. Writes result.json.
"""
import json
import pathlib
import statistics
import time
import urllib.request
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).parent
COST = 0.001
MAXB = 288


def bars():
    out = []
    t = int(datetime(2026, 7, 10, tzinfo=timezone.utc).timestamp() * 1000)
    end = int(datetime(2026, 10, 8, tzinfo=timezone.utc).timestamp() * 1000)
    while t < end:
        url = "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000&startTime=%d" % t
        rows = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
        if not rows:
            break
        out += [(float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if r[0] < end]
        t = rows[-1][0] + 1
        time.sleep(0.08)
    return out


def run_trade(b, i, side, entry, stop):
    risk = abs(entry - stop)
    if risk <= entry * 0.0005:
        return None
    tgt = entry + 2 * risk if side > 0 else entry - 2 * risk
    for j in range(i, min(i + MAXB, len(b))):
        o, h, l, c = b[j]
        if side > 0:
            if l <= stop:
                r = -1.0
                break
            if h >= tgt:
                r = 2.0
                break
        else:
            if h >= stop:
                r = -1.0
                break
            if l <= tgt:
                r = 2.0
                break
    else:
        j = min(i + MAXB, len(b)) - 1
        r = (b[j][3] - entry) / risk * side
    return r - COST * entry / risk


def main():
    b = bars()
    n = len(b)
    sh = [False] * n
    sl = [False] * n
    for i in range(2, n - 2):
        h, l = b[i][1], b[i][2]
        sh[i] = h > max(b[i - 2][1], b[i - 1][1], b[i + 1][1], b[i + 2][1])
        sl[i] = l < min(b[i - 2][2], b[i - 1][2], b[i + 1][2], b[i + 2][2])
    A, B = [], []
    highs, lows = [], []  # (index, price) of known swings
    used_h, used_l = set(), set()
    for i in range(4, n - 1):
        k = i - 2  # swing at k is known at bar i
        if sh[k]:
            highs.append((k, b[k][1]))
        if sl[k]:
            lows.append((k, b[k][2]))
        if len(highs) < 2 or len(lows) < 2:
            continue
        c = b[i][3]
        for side in (1, -1):
            if side > 0:
                bear = lows[-1][1] < lows[-2][1]
                lvl, key = highs[-1][1], highs[-1][0]
                if not bear or key in used_h or c <= lvl:
                    continue
                used_h.add(key)
                anchor = lows[-1][0]
                stopA = min(x[2] for x in b[anchor:i + 1])
            else:
                bull = highs[-1][1] > highs[-2][1]
                lvl, key = lows[-1][1], lows[-1][0]
                if not bull or key in used_l or c >= lvl:
                    continue
                used_l.add(key)
                anchor = highs[-1][0]
                stopA = max(x[1] for x in b[anchor:i + 1])
            if i + 1 >= n:
                continue
            ra = run_trade(b, i + 1, side, b[i + 1][0], stopA)
            if ra is not None:
                A.append(ra)
            # B: first post-shift pullback swing, then a sweep-and-reclaim of it
            pull = None
            for j in range(i + 1, min(i + MAXB, n - 3)):
                o, h, l, cc = b[j]
                if (side > 0 and l <= stopA) or (side < 0 and h >= stopA):
                    break
                kk = j - 2
                if pull is None and kk > i:
                    if side > 0 and sl[kk]:
                        pull = b[kk][2]
                    elif side < 0 and sh[kk]:
                        pull = b[kk][1]
                    continue
                if pull is not None:
                    if side > 0 and l < pull and cc > pull:
                        rb = run_trade(b, j + 1, side, b[j + 1][0], l)
                        if rb is not None:
                            B.append(rb)
                        break
                    if side < 0 and h > pull and cc < pull:
                        rb = run_trade(b, j + 1, side, b[j + 1][0], h)
                        if rb is not None:
                            B.append(rb)
                        break

    def summ(x):
        return {"trades": len(x), "win_rate": round(sum(r > 0 for r in x) / len(x), 3) if x else None,
                "mean_R_after_costs": round(statistics.mean(x), 3) if x else None,
                "total_R": round(sum(x), 1)}
    res = {"bars": n, "A_shift_entry": summ(A), "B_inducement_entry": summ(B)}
    print(json.dumps(res))
    (HERE / "result.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
