"""Lookahead audit, 13 Oct 2026. Luke's word after the luck-test Workshop ("do it").

Every vectorised backtest behind a live book is replayed by a separate bar-by-bar stepper that can
only see the past: at the open of bar t it fills orders placed earlier; at the close of bar t it
decides with indicator values at index <= t, checked separately to be causal (recomputed on the
series cut at t). The two must agree trade for trade: same entry bar, same exit bar, same return.

Positive control: the first draft of luck_test.py's sma rule, which used each close's signal from
that bar's open. The harness has to flag it, or a clean result means nothing.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-13-lookahead-audit/audit.py
"""
import importlib.util
import json
import math
import sys

import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0091")
from p0082 import load, rsi_wilder, sma, rsi5_rp, ma_filter_rp, trades_from_rp  # noqa: E402
from basket_backtest import rsi5_next_open_rp  # noqa: E402
from p0091 import books  # noqa: E402

spec = importlib.util.spec_from_file_location("lt", "/Users/triton/PROTEUS/docs/tools/luck-test/luck_test.py")
lt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lt)

OUT = "/Users/triton/PROTEUS/experiments/2026-10-13-lookahead-audit/result.json"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
TOL = 1e-9


def causal(fn, c, n_cuts=60, seed=3):
    """Indicator at t must not change when everything after t is removed."""
    full = fn(c)
    rng = np.random.default_rng(seed)
    worst = 0.0
    for t in rng.integers(250, c.size, n_cuts):
        a, b = fn(c[:t + 1])[t], full[t]
        if not (np.isnan(a) and np.isnan(b)):
            worst = max(worst, abs(a - b))
    return worst


class Stepper:
    """Orders placed at a close fill at the next open ('open') or at that same close ('close')."""

    def __init__(self, o, c):
        self.o, self.c = o, c
        self.pos, self.pending, self.trades, self.entry = 0, None, [], None

    def open_bar(self, t):
        if self.pending == "buy":
            self.pos, self.entry = 1, (t, self.o[t])
        elif self.pending == "sell":
            self.trades.append((self.entry[0], t, self.o[t] / self.entry[1] - 1))
            self.pos = 0
        self.pending = None

    def at_close(self, t, order, fill):
        if order is None:
            return
        if fill == "open":
            self.pending = order
        elif order == "buy":
            self.pos, self.entry = 1, (t, self.c[t])
        else:
            self.trades.append((self.entry[0], t, self.c[t] / self.entry[1] - 1))
            self.pos = 0

    def flat(self):
        return self.pos == 0 and self.pending is None


def step_rsi5(o, c, variant, fill):
    r, m = rsi_wilder(c, 5), sma(c, 200)
    s = Stepper(o, c)
    for t in range(c.size):
        s.open_bar(t)
        order = None
        if s.pos == 1 and s.pending is None and r[t] > 50:
            order = "sell"
        elif s.flat() and t >= 3 and not np.isnan(m[t]) and not np.isnan(r[t - 3]):
            ok = c[t] > m[t] and r[t] < 30
            if variant >= 2:
                ok = ok and r[t] < r[t - 1] < r[t - 2] < r[t - 3]
            if variant >= 3:
                ok = ok and r[t - 3] < 60
            order = "buy" if ok else None
        s.at_close(t, order, fill)
    return s.trades


def step_ibs_gated(o, h, l, c):
    """Book 1 (next open) decides first at each close; IBS buys only if book 1 is flat after that."""
    r, m = rsi_wilder(c, 5), sma(c, 200)
    b1, b2 = Stepper(o, c), Stepper(o, c)
    for t in range(c.size):
        b1.open_bar(t)
        b2.open_bar(t)
        o1 = None
        if b1.pos == 1 and r[t] > 50:
            o1 = "sell"
        elif b1.flat() and t >= 3 and not np.isnan(m[t]) and not np.isnan(r[t - 3]) and c[t] > m[t] and r[t] < 30:
            o1 = "buy"
        b1.at_close(t, o1, "open")
        o2 = None
        if b2.pos == 1 and t >= 1 and c[t] > h[t - 1]:
            o2 = "sell"
        elif b2.flat() and h[t] > l[t] and (c[t] - l[t]) / (h[t] - l[t]) < 0.2 and b1.flat():
            o2 = "buy"
        b2.at_close(t, o2, "open")
    return b1.trades, b2.trades


def step_sma(o, c, n):
    m = sma(c, n)
    s = Stepper(o, c)
    for t in range(c.size):
        s.open_bar(t)
        order = None
        if not np.isnan(m[t]):
            if s.flat() and c[t] > m[t]:
                order = "buy"
            elif s.pos == 1 and s.pending is None and c[t] < m[t]:
                order = "sell"
        s.at_close(t, order, "open")
    return s.trades


def shift(trades, a, b):
    """Move the stepper's bar labels onto the backtest's labelling convention; returns untouched."""
    return [(x[0] + a, x[1] + b, x[2]) for x in trades]


def from_tid(rets, tid):
    """(entry bar, last bar, simple return) from a vectorised backtest's trade ids."""
    out = {}
    for i in range(len(tid)):
        k = int(tid[i])
        if k:
            a = out.setdefault(k, [i, i, 0.0])
            a[1], a[2] = i, a[2] + rets[i]
    return [(a[0], a[1], math.expm1(a[2])) for a in out.values()]


def compare(ref, test, label, open_trades_ok=True):
    """Closed trades from the stepper against the backtest's. The backtest may also hold a trade
    still open at the end; that one is dropped."""
    test = [x for x in test if x[0] <= (ref[-1][1] if ref else -1)] if open_trades_ok else test
    n = min(len(ref), len(test))
    first = next((i for i in range(n) if ref[i][0] != test[i][0] or ref[i][1] != test[i][1]
                  or abs(ref[i][2] - test[i][2]) > TOL), None)
    ok = first is None and len(ref) == len(test)
    row = {"check": label, "stepper_trades": len(ref), "backtest_trades": len(test), "match": ok}
    if not ok:
        i = first if first is not None else n
        row["first_difference"] = {"stepper": ref[i] if i < len(ref) else None, "backtest": test[i] if i < len(test) else None}
    return row


def lt_total(rule, o, h, l, c, **kw):
    class A:  # luck_test.py's argparse namespace
        n, threshold = kw.get("n", 200), kw.get("threshold", 30.0)
    return float(rule(o, h, l, c, A).sum())


def main():
    rows, causal_worst = [], {}
    for s in BASKET:
        df = load(s, adjusted=False)
        o, h, l, c = (df[x].to_numpy() for x in ("open", "high", "low", "close"))
        causal_worst[s] = max(causal(lambda x: rsi_wilder(x, 5), c), causal(lambda x: sma(x, 200), c))
        for v, nm in ((1, "simple"), (3, "triple")):
            rows.append(compare(step_rsi5(o, c, v, "open"), from_tid(*rsi5_next_open_rp(o, c, v)), f"{s} P-0083 rsi5 {nm} next open"))
            # close fills: the backtest's first return bar is the one after the signal close
            rows.append(compare(shift(step_rsi5(o, c, v, "close"), 1, 0), from_tid(*rsi5_rp(c, v)), f"{s} P-0082 rsi5 {nm} close"))
        b1, b2 = step_ibs_gated(o, h, l, c)
        rr, rt, ir, it = books(o, h, l, c, True)
        rows.append(compare(b1, from_tid(rr, rt), f"{s} P-0091 book 1 inside books()"))
        rows.append(compare(b2, from_tid(ir, it), f"{s} P-0091 ibs gated"))
        # open-to-open returns: the backtest's last bar is the one before the exit open
        rows.append(compare(shift(step_sma(o, c, 200), 0, -1), from_tid(*ma_filter_rp(o, c, 200)), f"{s} P-0082 sma200"))
        print(s, "done", flush=True)

    # luck_test.py, the published tool, against the stepper on SPY (total log return over closed trades)
    df = load("SPY")
    o, h, l, c = (df[x].to_numpy() for x in ("open", "high", "low", "close"))
    ref = step_sma(o, c, 200)
    ref_total = sum(math.log1p(x[2]) for x in ref)
    last = ref[-1][1]
    tool = lt.rule_sma(o, h, l, c, type("A", (), {"n": 200})())
    tool_total = float(tool[:last].sum())

    def bugged(o, c, n):  # the first draft, as it was before the fix at about 16:55
        m = lt.sma(c, n)
        sig = np.where(np.isnan(m), 0, np.where(c > m, 1, np.where(c < m, -1, 0)))
        pos = np.zeros(c.size)
        p = 0
        for t in range(c.size):
            pos[t] = p
            p = 1 if sig[t] == 1 else (0 if sig[t] == -1 else p)
        rets = np.zeros(c.size)
        lo = np.log(o)
        rets[:-1] = pos[1:] * (lo[1:] - lo[:-1])
        return rets
    bug_total = float(bugged(o, c, 200)[:last].sum())
    control = {"stepper_total_log": round(ref_total, 6), "tool_total_log": round(tool_total, 6),
               "tool_match": abs(ref_total - tool_total) < 1e-6,
               "bugged_draft_total_log": round(bug_total, 6), "bugged_draft_flagged": abs(ref_total - bug_total) > 1e-6}

    res = {"checks": rows, "indicator_causality_worst_abs_diff": causal_worst, "luck_test_tool_and_control": control,
           "all_match": all(r["match"] for r in rows) and control["tool_match"] and control["bugged_draft_flagged"]}
    json.dump(res, open(OUT, "w"), indent=1, default=float)
    bad = [r for r in rows if not r["match"]]
    print(f"{len(rows) - len(bad)} of {len(rows)} backtest checks match; causality worst {max(causal_worst.values()):.2e}")
    for r in bad:
        print("MISMATCH", r)
    print("tool and control", control)


if __name__ == "__main__":
    main()
