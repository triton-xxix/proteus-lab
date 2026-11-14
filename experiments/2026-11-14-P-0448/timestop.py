"""P-0448: book 1's RSI(5) rule in the 2009 to 2026 backtest, by hold length, and a 5-session time stop.

Rules written before the run (README): close above SMA200 and Wilder RSI(5) under 30 at the close -> buy
next open; RSI(5) over 50 at a close -> sell next open. Nine ETFs, price-only Yahoo bars cached in
sandbox/p0082/data/ (to 6 Oct 2026). Entries from 2009-01-02. Gross, open to open; costs not netted.
Hold = sessions from buy open to sell open.

Time stop T: also sell at the next open after the T-th close in the trade if RSI has not exited yet.
Same entries both ways, so the paired difference per trade is the effect; its luck test is a sign-flip
permutation on the per-trade differences (10,000). A random-entry control (P-0089 style) asks whether the
time-stopped rule's mean beats random entries above SMA200 with the same exits (2,000 draws per ETF set).
"""
import csv
import json
import pathlib
import random
import statistics
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/systems")
from systems import rsi_wilder, sma, BASKET  # noqa: E402

HERE = pathlib.Path(__file__).parent
DATA = pathlib.Path("/Users/triton/PROTEUS/sandbox/p0082/data")
FROM = "2009-01-02"


def load(sym):
    rows = list(csv.DictReader(open(DATA / f"{sym}.csv")))
    out = []
    for r in rows:
        try:
            out.append((r["date"], float(r["open"]), float(r["close"])))
        except ValueError:
            pass
    return out


def run(b, rs, ms, entries, stop=None):
    """entries: list of signal-close indices. Returns trades (ret, hold) with RSI exit and optional time stop."""
    trades = []
    busy_until = -1
    for i in entries:
        if i <= busy_until or i + 1 >= len(b):
            continue
        j = i + 1  # buy open
        k = None
        for c in range(j, len(b) - 1):
            if rs[c] is not None and rs[c] > 50:
                k = c + 1
                break
            if stop is not None and c - j + 1 >= stop:
                k = c + 1
                break
        if k is None:
            break
        trades.append((b[k][1] / b[j][1] - 1, k - j, i))
        busy_until = k - 1
    return trades


def summ(t):
    if not t:
        return {"n": 0}
    r = [x[0] * 100 for x in t]
    return {"n": len(r), "mean_pct": round(statistics.mean(r), 3), "win": round(sum(1 for x in r if x > 0) / len(r), 3)}


def bucket(h):
    return "1-3" if h <= 3 else "4-5" if h <= 5 else "6-9" if h <= 9 else "10+"


allb, base, stops = {}, [], {3: [], 5: [], 7: []}
sig_by = {}
for sym in BASKET:
    b = load(sym)
    cs = [x[2] for x in b]
    rs, ms = rsi_wilder(cs), sma(cs)
    sig = [i for i in range(len(b)) if b[i][0] >= FROM and ms[i] and rs[i] is not None and cs[i] > ms[i] and rs[i] < 30]
    allb[sym] = (b, rs, ms)
    sig_by[sym] = sig
    base += [(sym,) + t for t in run(b, rs, ms, sig)]
    for T in stops:
        stops[T] += [(sym,) + t for t in run(b, rs, ms, sig, T)]

base_t = [(t[1], t[2]) for t in base]
out = {"base": summ(base_t), "backtest_quoted": {"mean_pct": 0.63, "win": 0.75}}
out["by_hold"] = {k: summ([(t[1], t[2]) for t in base if bucket(t[2]) == k]) for k in ("1-3", "4-5", "6-9", "10+")}
for T, tr in stops.items():
    out[f"stop{T}"] = summ([(t[1], t[2]) for t in tr])

# paired: same entry signal index, base v stop5
b5 = {(t[0], t[3]): t[1] for t in base}
s5 = {(t[0], t[3]): t[1] for t in stops[5]}
common = sorted(set(b5) & set(s5))
diffs = [(s5[k] - b5[k]) * 100 for k in common]
changed = [d for d in diffs if abs(d) > 1e-12]
obs = statistics.mean(diffs)
rng = random.Random(448)
ge = 0
for _ in range(10000):
    m = statistics.mean([d if rng.random() < 0.5 else -d for d in diffs])
    if m >= obs:
        ge += 1
out["paired_stop5"] = {"common_entries": len(common), "changed": len(changed), "mean_diff_pct_per_trade": round(obs, 4),
                       "mean_diff_on_changed": round(statistics.mean(changed), 3) if changed else None,
                       "signflip_p_stop_better": round((ge + 1) / 10001, 4)}

# random-entry control for stop5: same filter (close above SMA200), same exits, same trade count per ETF
n_by = {sym: sum(1 for t in stops[5] if t[0] == sym) for sym in BASKET}
real = out["stop5"]["mean_pct"]
draws, beat = 500, 0
dist = []
for _ in range(draws):
    pooled = []
    for sym in BASKET:
        b, rs, ms = allb[sym]
        pool = [i for i in range(len(b)) if b[i][0] >= FROM and ms[i] and b[i][2] > ms[i]]
        picks = sorted(rng.sample(pool, min(len(pool), n_by[sym] * 3)))
        tr = run(b, rs, ms, picks, 5)[: n_by[sym]]
        pooled += [x[0] * 100 for x in tr]
    m = statistics.mean(pooled)
    dist.append(m)
    if m >= real:
        beat += 1
out["random_entry_stop5"] = {"draws": draws, "random_mean_pct": round(statistics.mean(dist), 3), "p": round((beat + 1) / (draws + 1), 4)}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
