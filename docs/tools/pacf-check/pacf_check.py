"""pacf_check.py: is that lag in your daily returns real, or one window's noise?

Partial autocorrelation of daily log returns, lags 1 to N, in two windows split at a date, with the
95% band +-1.96/sqrt(n). A lag outside the band in one window and inside it in the other is flagged
"one window only". Standard library only.

  python3 pacf_check.py prices.csv --split 2024-10-23
  python3 pacf_check.py --yahoo SPY QQQ EWU --start 2022-10-23 --split 2024-10-23
  python3 pacf_check.py a.csv b.csv --split 2024-10-23 --lags 10 --json out.json

A CSV needs a date column and a close column (adjclose is used if present). Several series give a
pooled count per lag; correlated markets share their artefacts, so k of 9 is not 9 coin flips.
From Proteus probes P-0191 and P-0193 (22 Oct 2026). Not advice.
"""
import argparse
import csv
import json
import math
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone


def read_csv(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("%s: no rows" % path)
    keys = {k.lower().replace(" ", "").replace("_", ""): k for k in rows[0]}
    dk = keys.get("date") or sys.exit("%s: no date column" % path)
    ck = keys.get("adjclose") or keys.get("close") or sys.exit("%s: no close column" % path)
    out = []
    for r in rows:
        try:
            out.append((r[dk][:10], float(r[ck])))
        except (ValueError, TypeError):
            continue
    return sorted(out)


def read_yahoo(sym):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?range=5y&interval=1d" % sym
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            d = json.load(urllib.request.urlopen(req, timeout=30))
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    r = d["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    off = r["meta"].get("gmtoffset", 0)
    return [(datetime.fromtimestamp(ts + off, tz=timezone.utc).date().isoformat(), float(c))
            for ts, c in zip(r["timestamp"], q["close"]) if c is not None]


def acf(x, maxlag):
    n = len(x)
    m = sum(x) / n
    d = [v - m for v in x]
    c0 = sum(v * v for v in d) / n
    return [1.0] + [sum(d[i] * d[i - k] for i in range(k, n)) / n / c0 for k in range(1, maxlag + 1)]


def pacf(rho, maxlag):
    """Durbin-Levinson."""
    out, prev = [], []
    for k in range(1, maxlag + 1):
        if k == 1:
            kk, phi = rho[1], [rho[1]]
        else:
            num = rho[k] - sum(prev[j] * rho[k - 1 - j] for j in range(k - 1))
            den = 1 - sum(prev[j] * rho[j + 1] for j in range(k - 1))
            kk = num / den
            phi = [prev[j] - kk * prev[k - 2 - j] for j in range(k - 1)] + [kk]
        out.append(kk)
        prev = phi
    return out


def window(closes, lo, hi, maxlag):
    cs = [c for d, c in closes if lo <= d < hi]
    rets = [math.log(cs[i] / cs[i - 1]) for i in range(1, len(cs))]
    n = len(rets)
    if n < 4 * maxlag:
        sys.exit("window %s to %s has %d returns, too few for %d lags" % (lo, hi, n, maxlag))
    band = 1.96 / math.sqrt(n)
    p = pacf(acf(rets, maxlag), maxlag)
    return {"from": lo, "to": hi, "n_returns": n, "band": round(band, 4),
            "pacf": [round(v, 4) for v in p], "outside": [k + 1 for k, v in enumerate(p) if abs(v) > band]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="CSV files with date and close")
    ap.add_argument("--yahoo", nargs="+", default=[], help="symbols to pull from Yahoo (5 years, keyless)")
    ap.add_argument("--split", required=True, help="first date of the second window, YYYY-MM-DD")
    ap.add_argument("--start", default="0000", help="first date of the first window")
    ap.add_argument("--end", default="9999", help="day after the last date of the second window")
    ap.add_argument("--lags", type=int, default=10)
    ap.add_argument("--json", help="write the full result here")
    a = ap.parse_args()
    series = [(f, read_csv(f)) for f in a.files]
    for s in a.yahoo:
        series.append((s, read_yahoo(s)))
        time.sleep(1)
    if not series:
        ap.error("give CSV files or --yahoo symbols")

    res = {"split": a.split, "lags": a.lags, "series": {}}
    for name, closes in series:
        A = window(closes, a.start, a.split, a.lags)
        B = window(closes, a.split, a.end, a.lags)
        one = sorted(set(A["outside"]) ^ set(B["outside"]))
        both = sorted(set(A["outside"]) & set(B["outside"]))
        res["series"][name] = {"first": A, "second": B, "both_windows": both, "one_window_only": one}
        print("%s  (n %d | %d, band %.3f | %.3f)" % (name, A["n_returns"], B["n_returns"], A["band"], B["band"]))
        print("  lag " + " ".join("%7d" % (k + 1) for k in range(a.lags)))
        for lab, W in (("1st", A), ("2nd", B)):
            print("  %s " % lab + " ".join("%6.3f%s" % (v, "*" if k + 1 in W["outside"] else " ")
                                          for k, v in enumerate(W["pacf"])))
        print("  outside in both windows: %s   one window only: %s" % (both or "none", one or "none"))
    if len(series) > 1:
        S = res["series"].values()
        pooled = {w: [sum(1 for s in S if k in s[w]["outside"]) for k in range(1, a.lags + 1)]
                  for w in ("first", "second")}
        res["pooled"] = pooled
        print("pooled, series with the lag outside the band (of %d):" % len(series))
        print("  lag " + " ".join("%3d" % (k + 1) for k in range(a.lags)))
        print("  1st " + " ".join("%3d" % v for v in pooled["first"]))
        print("  2nd " + " ".join("%3d" % v for v in pooled["second"]))
        print("chance alone puts about %.1f series outside per lag; correlated markets move together, so read it loosely"
              % (0.05 * len(series)))
    if a.json:
        with open(a.json, "w") as f:
            json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
