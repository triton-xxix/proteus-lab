"""P-0102: is BTC's hour after a high-impact USD release at least 1.5x as volatile as baseline?

Events (dates fetched 8 Oct 2026 from the Fed's FOMC calendar and the BLS release schedules):
FOMC decisions 14:00 ET, CPI and Employment Situation 08:30 ET. The BLS pages list Dec 2025 onward
only, so CPI and NFP cover Dec 2025 to Oct 2026; FOMC covers Oct 2025 to Sep 2026.
Hour = the two 30-minute Binance BTCUSDT candles starting at the release time.
Volatility = (highest high - lowest low) / open over that hour; also |close/open - 1|.
Baseline = the same clock time (UTC) on every other weekday in the window that is not an event day.
"""
import json
import pathlib
import statistics
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone

HERE = pathlib.Path(__file__).parent
FOMC = ["2025-10-29", "2025-12-10", "2026-01-28", "2026-03-18", "2026-04-29", "2026-06-17", "2026-07-29", "2026-09-16"]
CPI = ["2025-12-18", "2026-01-13", "2026-02-13", "2026-03-11", "2026-04-10", "2026-05-12", "2026-06-10", "2026-07-14",
       "2026-08-12", "2026-09-11"]
NFP = ["2025-12-16", "2026-01-09", "2026-02-11", "2026-03-06", "2026-04-03", "2026-05-08", "2026-06-05", "2026-07-02",
       "2026-08-07", "2026-09-04", "2026-10-02"]
START, END = date(2025, 10, 9), date(2026, 10, 8)


def edt(d):
    # US daylight time: 2nd Sunday in March to 1st Sunday in November
    def nth_sunday(y, m, n):
        x = date(y, m, 1)
        x += timedelta(days=(6 - x.weekday()) % 7)
        return x + timedelta(weeks=n - 1)
    return nth_sunday(d.year, 3, 2) <= d < nth_sunday(d.year, 11, 1)


def utc_at(day, hh, mm):
    off = 4 if edt(day) else 5
    return datetime(day.year, day.month, day.day, hh, mm, tzinfo=timezone.utc) + timedelta(hours=off)


def klines():
    out = {}
    t = int(datetime(2025, 10, 8, tzinfo=timezone.utc).timestamp() * 1000)
    end = int(datetime(2026, 10, 8, 23, 0, tzinfo=timezone.utc).timestamp() * 1000)
    while t < end:
        url = "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=30m&limit=1000&startTime=%d" % t
        rows = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
        if not rows:
            break
        for r in rows:
            out[r[0]] = (float(r[1]), float(r[2]), float(r[3]), float(r[4]))
        t = rows[-1][0] + 1
        time.sleep(0.1)
    return out


def hour_stats(k, start):
    ms = int(start.timestamp() * 1000)
    a, b = k.get(ms), k.get(ms + 1800000)
    if not a or not b:
        return None
    hi, lo = max(a[1], b[1]), min(a[2], b[2])
    return (hi - lo) / a[0], abs(b[3] / a[0] - 1)


def main():
    k = klines()
    kinds = {"FOMC": (FOMC, 14, 0), "CPI": (CPI, 8, 30), "NFP": (NFP, 8, 30)}
    event_days = {d for v in kinds.values() for d in v[0]}
    res = {"candles": len(k)}
    allr, allb = [], []
    for name, (days, hh, mm) in kinds.items():
        ev, base = [], []
        for ds in days:
            d = date.fromisoformat(ds)
            s = hour_stats(k, utc_at(d, hh, mm))
            if s:
                ev.append(s)
        d = START
        while d <= END:
            if d.weekday() < 5 and d.isoformat() not in event_days:
                s = hour_stats(k, utc_at(d, hh, mm))
                if s:
                    base.append(s)
            d += timedelta(days=1)
        er, br = [x[0] for x in ev], [x[0] for x in base]
        ea, ba = [x[1] for x in ev], [x[1] for x in base]
        p75 = sorted(br)[int(len(br) * 0.75)]
        res[name] = {
            "events": len(ev), "baseline_hours": len(base),
            "range_median_ratio": round(statistics.median(er) / statistics.median(br), 2),
            "range_mean_ratio": round(statistics.mean(er) / statistics.mean(br), 2),
            "absret_median_ratio": round(statistics.median(ea) / statistics.median(ba), 2),
            "event_range_median_pct": round(100 * statistics.median(er), 3),
            "baseline_range_median_pct": round(100 * statistics.median(br), 3),
            "share_events_above_baseline_p75": round(sum(x > p75 for x in er) / len(er), 2),
        }
        allr += [x / statistics.median(br) for x in er]
        print(name, res[name])
    res["pooled_median_ratio_vs_own_slot"] = round(statistics.median(allr), 2)
    res["pooled_events"] = len(allr)
    print("pooled", res["pooled_median_ratio_vs_own_slot"], len(allr))
    (HERE / "result.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
