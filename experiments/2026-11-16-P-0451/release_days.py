"""P-0451: are BTC daily moves on FOMC and CPI days bigger than on ordinary days since 2023?

Called shot (before the run): yes for FOMC and CPI alike, release-day mean |move| about 1.2x an
ordinary day, permutation p under 0.10 for the pooled set.

Data, keyless:
- FOMC decision days (second day of each scheduled meeting), 2023 to 2026, from
  experiments/2026-10-26-P-0227/fomc.json (parsed from federalreserve.gov on 26 Oct 2026).
- CPI release days from the BLS CPI release archive page (bls.gov blocks curl, so the Wayback
  copy, sandbox/p0451-cpi.html), codes cpi_MMDDYYYY.
- BTCUSDT daily candles (UTC days) from data-api.binance.vision.
Move = |close / open - 1| on the UTC day of the release (both releases land inside that UTC day).
"""
import json
import random
import re
import statistics
import time
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
FOMC_JSON = Path("/Users/triton/PROTEUS/experiments/2026-10-26-P-0227/fomc.json")
CPI_HTML = Path("/Users/triton/PROTEUS/sandbox/p0451-cpi.html")
START, END = date(2023, 1, 1), date(2026, 11, 15)
MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                          "August", "September", "October", "November", "December"])}


def fomc_days():
    data = json.loads(FOMC_JSON.read_text())
    out = []
    for y, block in data.items():
        for m in block["scheduled"]:
            month = m["month"].split("/")[-1]
            last = int(re.findall(r"\d+", m["days"])[-1])
            mnum = next(v for k, v in MONTHS.items() if k.startswith(month.strip()[:3]))
            out.append(date(int(y), mnum, last))
    return sorted(d for d in out if START <= d <= END)


def cpi_days():
    codes = set(re.findall(r"cpi_(\d{2})(\d{2})(\d{4})", CPI_HTML.read_text("utf-8", "replace")))
    out = sorted(date(int(y), int(m), int(d)) for m, d, y in codes)
    return [d for d in out if START <= d <= END]


def klines():
    rows = {}
    t = int(datetime(START.year, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
    while True:
        url = ("https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=1000"
               f"&startTime={t}")
        with urllib.request.urlopen(url, timeout=30) as r:
            batch = json.loads(r.read())
        if not batch:
            break
        for k in batch:
            d = datetime.fromtimestamp(k[0] / 1000, timezone.utc).date()
            if START <= d <= END:
                rows[d] = abs(float(k[4]) / float(k[1]) - 1) * 100
        t = batch[-1][0] + 86400000
        if len(batch) < 1000:
            break
        time.sleep(0.3)
    return rows


def perm_p(event, pool, n=20000, seed=7):
    rnd = random.Random(seed)
    obs = statistics.mean(event)
    k = len(event)
    hits = sum(statistics.mean(rnd.sample(pool, k)) >= obs for _ in range(n))
    return hits / n


def summary(name, days, moves, ordinary):
    ev = [moves[d] for d in days if d in moves]
    allv = list(moves.values())
    return {"set": name, "n": len(ev), "mean_abs_pct": round(statistics.mean(ev), 3),
            "median_abs_pct": round(statistics.median(ev), 3),
            "ratio_mean_vs_ordinary": round(statistics.mean(ev) / statistics.mean(ordinary), 3),
            "ratio_median_vs_ordinary": round(statistics.median(ev) / statistics.median(ordinary), 3),
            "share_above_ordinary_median": round(sum(v > statistics.median(ordinary) for v in ev) / len(ev), 3),
            "perm_p_vs_all_days": perm_p(ev, allv)}


def main():
    f, c = fomc_days(), cpi_days()
    moves = klines()
    events = set(f) | set(c)
    ordinary = [v for d, v in moves.items() if d not in events]
    by_year = {}
    for y in range(2023, 2027):
        fy = [d for d in f if d.year == y]
        cy = [d for d in c if d.year == y]
        oy = [v for d, v in moves.items() if d.year == y and d not in events]
        by_year[y] = {"ordinary_mean": round(statistics.mean(oy), 3),
                      "fomc_mean": round(statistics.mean([moves[d] for d in fy if d in moves]), 3) if fy else None,
                      "cpi_mean": round(statistics.mean([moves[d] for d in cy if d in moves]), 3) if cy else None,
                      "n_fomc": len(fy), "n_cpi": len(cy)}
    out = {"window": [str(START), str(END)], "days": len(moves),
           "ordinary": {"n": len(ordinary), "mean_abs_pct": round(statistics.mean(ordinary), 3),
                        "median_abs_pct": round(statistics.median(ordinary), 3)},
           "results": [summary("FOMC", f, moves, ordinary), summary("CPI", c, moves, ordinary),
                       summary("FOMC or CPI", sorted(events), moves, ordinary)],
           "by_year": by_year,
           "fomc_days": [str(d) for d in f], "cpi_days": [str(d) for d in c]}
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("window", "days", "ordinary", "results", "by_year")}, indent=1))


if __name__ == "__main__":
    main()
