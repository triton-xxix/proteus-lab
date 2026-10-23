#!/usr/bin/env python3
"""E-003, E-004, E-006 admission tests on the RECENT window, per edges/RULES.md. Luke asked 23 Oct 2026.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/edges/recent-2026-10-23/admission.py

Fixed before the run (23 Oct 2026, about 01:05 UTC, before any of the window's numbers were read):

  E-003 weak-Monday reversal, nine ETFs (SPY QQQ DIA IWM EFA EEM EWU EWJ EWG), Yahoo daily.
        Window  the last 21 complete weeks (a week is complete when its last session has a close).
        Signal  the week's first session closes below the low of the prior week's last session.
        Trade   long at the first session's close, exit at the week's last session close.
        Costs   0.05% round trip (the systems book's figure).
        Control random entries at any session close inside the window on the same ETF, held the
                same number of sessions as the median event hold (4), never overlapping an event's
                own hold on that ETF. 300 draws an ETF.
  E-004 jobs-report Friday long SPY. First Friday of the month stands in for the BLS date, as in
        P-0087 (the 2025 shutdown moved several real releases; those Fridays are not release days).
        Window  the last 12 first Fridays with a close.
        Trade   long at Thursday's close (the prior session), exit at Friday's close. 0.05% round trip.
        Control random one-session holds on SPY inside the window, event days excluded. 300 draws.
                Other Fridays in the window reported beside it.
  E-006 top-decile funding as a spot long, BTC and ETH, Binance (keyless).
        Signal  the UTC day's summed funding is at or above the 90th percentile of the trailing 180
                days (that day excluded), as P-0108.
        Window  the 21 signal-eligible days ending at the last day whose 7-day hold is complete.
        Trade   long spot at that day's close, exit at the close 7 days later. 0.20% round trip
                (0.10% a side, Binance spot taker).
        Control random entry days in the same window that are not signal days, same hold and costs,
                300 draws a coin. With 7-day holds inside 21 days the control cannot avoid
                overlapping the events' holds; the report says so.

  All three: each event ranks among its own instrument's draws; pooled permutation p = share of
  2,000 permutations (one draw an event from its instrument's pool) whose pooled mean is at least the
  edge's. Admission line: mean net above the control mean, p below 0.10, winners at least 5 in 8 of N.

Called shots, written before the run:
  E-003 not admitted, 0.65 (21 weeks across nine correlated ETFs is a thin, clustered window).
  E-004 not admitted, 0.75 (12 one-day holds, the noise swamps a 0.2-point effect).
  E-006 not admitted, 0.60 (funding has been quiet; few or no signal days in 21).
Writes admission.json beside this file and prints the tables.
"""
import json
import random
import statistics
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone

OUT = "/Users/triton/PROTEUS/edges/recent-2026-10-23/admission.json"
ETFS = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
DRAWS, PERMS = 300, 2000
rng = random.Random(20261023)


def getj(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise


def yahoo(sym):
    r = getj("https://query1.finance.yahoo.com/v8/finance/chart/%s?range=2y&interval=1d" % sym)["chart"]["result"][0]
    q, off = r["indicators"]["quote"][0], r["meta"].get("gmtoffset", 0)
    rows = []
    for ts, lo, c in zip(r["timestamp"], q["low"], q["close"]):
        if c is not None and lo is not None:
            rows.append((datetime.fromtimestamp(ts + off, tz=timezone.utc).date(), float(lo), float(c)))
    today = datetime.now(timezone.utc).date()
    return [x for x in rows if x[0] < today]  # today's bar may be live


def summarise(trades, pools, cost):
    """trades: list of (instrument, net). pools: instrument -> list of control nets."""
    nets = [t[1] for t in trades]
    if not nets:
        return {"n": 0}
    edge = statistics.mean(nets)
    ctrl = [x for k in {t[0] for t in trades} for x in pools[k]]
    ranks = [sum(1 for x in pools[k] if x < v) / len(pools[k]) for k, v in trades]
    hits = sum(1 for _ in range(PERMS) if statistics.mean(rng.choice(pools[k]) for k, _ in trades) >= edge)
    wins = sum(1 for x in nets if x > 0)
    need = -(-5 * len(nets) // 8)
    res = {"n": len(nets), "mean_net_pct": round(edge * 100, 3), "median_net_pct": round(statistics.median(nets) * 100, 3),
           "winners": wins, "winners_needed": need, "control_mean_pct": round(statistics.mean(ctrl) * 100, 3),
           "control_median_pct": round(statistics.median(ctrl) * 100, 3), "mean_rank_in_draws": round(statistics.mean(ranks), 3),
           "perm_p": round(hits / PERMS, 4), "cost_round_trip_pct": cost * 100}
    res["admitted"] = edge > statistics.mean(ctrl) and res["perm_p"] < 0.10 and wins >= need
    return res


def e003(data):
    trades, pools, detail, spans = [], {}, [], []
    for sym in ETFS:
        bars = data[sym]
        weeks = {}
        for i, (d, _, _) in enumerate(bars):
            weeks.setdefault(d.isocalendar()[:2], []).append(i)
        keys = sorted(weeks)
        last_complete = keys[-1] if bars[weeks[keys[-1]][-1]][0].weekday() == 4 else None
        keys = [k for k in keys if k != keys[-1] or last_complete]
        keys = keys[-22:]  # 21 weeks plus the one before the first for its last session
        events, busy = [], set()
        for prev, cur in zip(keys, keys[1:]):
            p, idx = weeks[prev][-1], weeks[cur]
            if bars[idx[0]][2] < bars[p][1] and len(idx) > 1:
                net = bars[idx[-1]][2] / bars[idx[0]][2] - 1 - 0.0005
                events.append((sym, net))
                busy.update(range(idx[0], idx[-1] + 1))
                detail.append({"etf": sym, "monday": str(bars[idx[0]][0]), "exit": str(bars[idx[-1]][0]), "net_pct": round(net * 100, 3)})
        lo, hi = weeks[keys[1]][0], weeks[keys[-1]][-1]
        spans.append((bars[lo][0], bars[hi][0]))
        starts = [i for i in range(lo, hi - 4 + 1) if not busy.intersection(range(i, i + 5))]
        pools[sym] = [bars[i + 4][2] / bars[i][2] - 1 - 0.0005 for i in (rng.choice(starts) for _ in range(DRAWS))]
        trades += events
    res = summarise(trades, pools, 0.0005)
    res["window"] = "%s to %s, 21 weeks, nine ETFs" % (min(s[0] for s in spans), max(s[1] for s in spans))
    res["trades"] = detail
    return res


def e004(spy):
    idx = {d: i for i, (d, _, _) in enumerate(spy)}
    fridays = [i for i, (d, _, _) in enumerate(spy) if d.weekday() == 4 and d.day <= 7 and i > 0]
    ev = fridays[-12:]
    trades, detail = [], []
    for i in ev:
        net = spy[i][2] / spy[i - 1][2] - 1 - 0.0005
        trades.append(("SPY", net))
        detail.append({"friday": str(spy[i][0]), "net_pct": round(net * 100, 3)})
    lo, hi = ev[0] - 1, ev[-1]
    cand = [i for i in range(lo + 1, hi + 1) if i not in ev]
    pools = {"SPY": [spy[i][2] / spy[i - 1][2] - 1 - 0.0005 for i in (rng.choice(cand) for _ in range(DRAWS))]}
    other_fri = [spy[i][2] / spy[i - 1][2] - 1 - 0.0005 for i in cand if spy[i][0].weekday() == 4]
    res = summarise(trades, pools, 0.0005)
    res["window"] = "%s to %s, last 12 first Fridays" % (spy[ev[0]][0], spy[ev[-1]][0])
    res["other_fridays"] = {"n": len(other_fri), "mean_net_pct": round(statistics.mean(other_fri) * 100, 3)}
    res["trades"] = detail
    return res


def binance_daily_funding(sym, start_ms):
    out, t = {}, start_ms
    while True:
        d = getj("https://fapi.binance.com/fapi/v1/fundingRate?symbol=%s&startTime=%d&limit=1000" % (sym, t))
        for x in d:
            day = datetime.fromtimestamp(x["fundingTime"] / 1000, tz=timezone.utc).date()
            out[day] = out.get(day, 0.0) + float(x["fundingRate"])
        if len(d) < 1000:
            return out
        t = d[-1]["fundingTime"] + 1


def binance_closes(sym, start_ms):
    out, t = {}, start_ms
    while True:
        d = getj("https://api.binance.com/api/v3/klines?symbol=%s&interval=1d&startTime=%d&limit=1000" % (sym, t))
        for k in d:
            out[datetime.fromtimestamp(k[0] / 1000, tz=timezone.utc).date()] = float(k[4])
        if len(d) < 1000:
            return out
        t = d[-1][0] + 86400000


def quantile(xs, q):
    s = sorted(xs)
    pos = (len(s) - 1) * q
    lo = int(pos)
    return s[lo] + (s[min(lo + 1, len(s) - 1)] - s[lo]) * (pos - lo)


def e006():
    today = datetime.now(timezone.utc).date()
    start = int(datetime.combine(today - timedelta(days=260), datetime.min.time(), tzinfo=timezone.utc).timestamp() * 1000)
    trades, pools, detail, per = [], {}, [], {}
    for sym in ("BTCUSDT", "ETHUSDT"):
        f, c = binance_daily_funding(sym, start), binance_closes(sym, start)
        days = sorted(d for d in f if d in c and d < today)  # only closed days
        last = max(d for d in days if d + timedelta(days=7) in c and d + timedelta(days=7) < today)
        win = [d for d in days if d <= last][-21:]
        events, ctrl_days = [], []
        for d in win:
            hist = [f[x] for x in days if d - timedelta(days=180) <= x < d]
            th = quantile(hist, 0.9)
            net = c[d + timedelta(days=7)] / c[d] - 1 - 0.002
            if f[d] >= th:
                events.append((sym, net))
                detail.append({"coin": sym, "day": str(d), "funding_pct": round(f[d] * 100, 4), "p90_pct": round(th * 100, 4), "net_pct": round(net * 100, 3)})
            else:
                ctrl_days.append(net)
        pools[sym] = [rng.choice(ctrl_days) for _ in range(DRAWS)] if ctrl_days else [0.0]
        per[sym] = {"window": "%s to %s" % (win[0], win[-1]), "signal_days": len(events)}
        trades += events
    res = summarise(trades, pools, 0.002)
    res["per_coin"] = per
    res["trades"] = detail
    res["note"] = "7-day holds inside a 21-day window: event and control holds overlap; trades on neighbouring days are near copies"
    return res


def main():
    data = {}
    for s in ETFS:
        data[s] = yahoo(s)
        time.sleep(1)
    out = {"run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "E-003": e003(data), "E-004": e004(data["SPY"]), "E-006": e006()}
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    for k in ("E-003", "E-004", "E-006"):
        print(k, json.dumps({x: y for x, y in out[k].items() if x != "trades"}))


if __name__ == "__main__":
    main()
