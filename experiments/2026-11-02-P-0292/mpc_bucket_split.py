"""P-0292: P-0280 split by what the MPC did. Each meeting since 2009 from the Bank Rate sheet of the Bank's
mpcvoting.xlsx (column B the date, C the rate decided, one column per member holding the rate that member
voted for or "Increase"/"Decrease"). Decision = hike, cut or hold against the previous meeting's rate; split
= any member cell differing from the decided rate. RSI(5) next-open trades whose signal day sits in the 5
trading days before a meeting carry that meeting's labels. Per bucket: trades, mean, the random-entry
control (P-0280's), and a permutation test of bucket v the trades outside any pre-window. Plus split v
unanimous inside the pre-window.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 -I experiments/2026-11-02-P-0292/mpc_bucket_split.py
"""
import datetime as dt
import json
import sys
import zipfile
import xml.etree.ElementTree as ET

import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
from p0082 import load, sma  # noqa: E402
from basket_backtest import rsi5_next_open_rp, BASKET  # noqa: E402

XLSX = "/Users/triton/PROTEUS/sandbox/boe-mpcvoting.xlsx"
OUT = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0292/results.json"
MEET = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0292/meetings.json"
WINDOW = 5
N_DRAWS = 1000
N_PERM = 5000
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def col(ref):
    return "".join(ch for ch in ref if ch.isalpha())


def meetings():
    z = zipfile.ZipFile(XLSX)
    shared = ["".join(t.text or "" for t in si.iter("{%s}t" % NS["m"]))
              for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]
    root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    rows = []
    for row in root.iter("{%s}row" % NS["m"]):
        cells = {}
        for c in row.findall("m:c", NS):
            v = c.find("m:v", NS)
            val = v.text if v is not None else ""
            if c.get("t") == "s" and val != "":
                val = shared[int(val)]
            if val != "":
                cells[col(c.get("r"))] = val
        try:
            d = float(cells.get("B", ""))
            rate = float(cells.get("C", ""))
        except ValueError:
            continue
        if not 20000 < d < 60000:
            continue
        date = (dt.datetime(1899, 12, 30) + dt.timedelta(days=d)).date()
        votes = {k: v for k, v in cells.items() if k not in ("A", "B", "C")}
        dissent = 0
        for v in votes.values():
            try:
                if abs(float(v) - rate) > 1e-9:
                    dissent += 1
            except ValueError:
                dissent += 1                 # "Increase" / "Decrease" text is a vote against the decided rate
        rows.append({"date": date, "rate": rate, "voters": len(votes), "dissent": dissent})
    rows.sort(key=lambda r: r["date"])
    out = []
    for prev, r in zip(rows, rows[1:]):
        if r["date"] < dt.date(2009, 1, 1):
            continue
        diff = r["rate"] - prev["rate"]
        kind = "hike" if diff > 1e-9 else "cut" if diff < -1e-9 else "hold"
        out.append({"date": r["date"].isoformat(), "rate_pct": round(r["rate"] * 100, 3), "kind": kind,
                    "voters": r["voters"], "dissent": r["dissent"], "split": r["dissent"] > 0})
    return out


M = meetings()
json.dump(M, open(MEET, "w"), indent=0)
counts = {k: sum(1 for m in M if m["kind"] == k) for k in ("hike", "cut", "hold")}
nsplit = sum(m["split"] for m in M)
print("meetings", len(M), counts, "split", nsplit, "voters range", min(m["voters"] for m in M), max(m["voters"] for m in M), flush=True)

rng = np.random.default_rng(20261102)
BUCKETS = ("hike", "cut", "hold", "split", "unanimous")


def labels_for(m):
    return (m["kind"], "split" if m["split"] else "unanimous")


def run(symbols, name):
    trades = {b: [] for b in BUCKETS + ("rest",)}
    pool = {b: [] for b in BUCKETS + ("rest",)}
    opens = {}
    for s in symbols:
        df = load(s)
        o, c = df["open"].to_numpy(), df["close"].to_numpy()
        idx = df.index.values
        opens[s] = o
        start = int(np.searchsorted(idx, np.datetime64("2009-01-01")))
        lab = [None] * len(idx)
        for m in M:
            p = int(np.searchsorted(idx, np.datetime64(m["date"]), side="left"))
            if p >= len(idx):
                continue
            for i in range(max(0, p - WINDOW), p):
                lab[i] = labels_for(m)
        rets, tid = rsi5_next_open_rp(o, c, 1)
        for k in np.unique(tid[start:][tid[start:] > 0]):
            w = np.where(tid == k)[0]
            e, x = w[0], w[-1]
            if x == len(c) - 1 and rets[x] == np.log(c[x]) - np.log(c[x - 1]):
                continue                     # open trade at the end of the data
            r = (float(np.expm1(rets[w].sum())), int(x - e))
            L = lab[e - 1]
            for b in (L if L else ("rest",)):
                trades[b].append(r)
        m200 = sma(c, 200)
        for i in range(start, len(o) - 60):
            if c[i] > m200[i]:
                for b in (lab[i] if lab[i] else ("rest",)):
                    pool[b].append((s, i))
    rest = np.array([r for r, _ in trades["rest"]])
    out = {}
    for b in BUCKETS + ("rest",):
        a = np.array([r for r, _ in trades[b]])
        holds = np.array([h for _, h in trades[b]])
        n = a.size
        if n < 2:
            out[b] = {"trades": int(n), "note": "too few"}
            print(name, b, out[b], flush=True)
            continue
        P = pool[b]
        sims = np.empty(N_DRAWS)
        for j in range(N_DRAWS):
            pick = rng.integers(0, len(P), n)
            hh = holds[rng.integers(0, n, n)]
            sims[j] = np.mean([opens[P[q][0]][P[q][1] + 1 + h] / opens[P[q][0]][P[q][1] + 1] - 1 for q, h in zip(pick, hh)])
        row = {"trades": int(n), "mean_pct": round(a.mean() * 100, 3), "win_pct": round((a > 0).mean() * 100, 1),
               "control_mean_pct": round(float(sims.mean()) * 100, 3),
               "excess_pct": round((a.mean() - sims.mean()) * 100, 3),
               "p_v_control": round(float((sims >= a.mean()).mean()), 4)}
        if b != "rest":
            allr = np.concatenate([a, rest])
            obs = a.mean() - rest.mean()
            perm = np.empty(N_PERM)
            for j in range(N_PERM):
                rng.shuffle(allr)
                perm[j] = allr[:n].mean() - allr[n:].mean()
            row["minus_rest_pct"] = round(obs * 100, 3)
            row["perm_p_two_sided"] = round(float((np.abs(perm) >= abs(obs)).mean()), 4)
        out[b] = row
        print(name, b, row, flush=True)
    sa = np.array([r for r, _ in trades["split"]])
    ua = np.array([r for r, _ in trades["unanimous"]])
    if sa.size >= 2 and ua.size >= 2:
        allr = np.concatenate([sa, ua])
        obs = sa.mean() - ua.mean()
        perm = np.empty(N_PERM)
        for j in range(N_PERM):
            rng.shuffle(allr)
            perm[j] = allr[:sa.size].mean() - allr[sa.size:].mean()
        out["split_minus_unanimous"] = {"diff_pct": round(obs * 100, 3),
                                        "perm_p_two_sided": round(float((np.abs(perm) >= abs(obs)).mean()), 4)}
        print(name, "split v unanimous", out["split_minus_unanimous"], flush=True)
    return out


res = {"window_trading_days_before_decision": WINDOW, "meetings_since_2009": len(M), "kinds": counts,
       "split_meetings": int(nsplit), "n_draws": N_DRAWS, "n_perm": N_PERM,
       "EWU": run(["EWU"], "EWU"), "all_nine": run(BASKET, "all nine")}
json.dump(res, open(OUT, "w"), indent=1)
print("wrote", OUT)
