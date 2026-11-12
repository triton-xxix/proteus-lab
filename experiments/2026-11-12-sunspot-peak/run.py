"""Wildcard, 12 Nov 2026: has solar cycle 25 peaked, and how does it sit against the
official forecast? Keyless pull of SILSO's monthly and 13-month smoothed sunspot numbers.

Usage: python3 run.py   (writes monthly.csv, smoothed.csv, results.json beside itself)
"""
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
URLS = {
    "monthly": "https://www.sidc.be/SILSO/DATA/SN_m_tot_V2.0.csv",
    "smoothed": "https://www.sidc.be/SILSO/DATA/SN_ms_tot_V2.0.csv",
}


def pull(name):
    req = urllib.request.Request(URLS[name], headers={"User-Agent": "python-urllib"})
    raw = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
    with open(os.path.join(HERE, name + ".csv"), "w") as f:
        f.write(raw)
    rows = []
    for line in raw.splitlines():
        p = [x.strip() for x in line.split(";")]
        if len(p) < 4:
            continue
        try:
            rows.append((int(p[0]), int(p[1]), float(p[3])))
        except ValueError:
            continue
    return rows


def main():
    m = pull("monthly")
    s = [r for r in pull("smoothed") if r[2] >= 0]  # -1 marks months not yet smoothable
    out = {"monthly_rows": len(m), "smoothed_rows": len(s),
           "last_monthly": m[-1], "last_smoothed": s[-1]}

    # cycle 25 began at the December 2019 minimum
    c25m = [r for r in m if (r[0], r[1]) >= (2019, 12)]
    c25s = [r for r in s if (r[0], r[1]) >= (2019, 12)]
    pk_s = max(c25s, key=lambda r: r[2])
    pk_m = max(c25m, key=lambda r: r[2])
    out["c25_smoothed_peak"] = pk_s
    out["c25_monthly_peak"] = pk_m
    months_since = (s[-1][0] - pk_s[0]) * 12 + (s[-1][1] - pk_s[1])
    out["smoothed_months_after_peak"] = months_since
    out["last_smoothed_as_share_of_peak"] = round(s[-1][2] / pk_s[2], 3)
    out["last_12_monthly"] = c25m[-12:]
    last6 = [r[2] for r in c25m[-6:]]
    out["last_6_monthly_mean"] = round(sum(last6) / 6, 1)

    # the 2019 NOAA/NASA panel forecast: smoothed peak 115 (95 to 130), July 2025 +/- 8 months
    out["panel_forecast"] = {"peak": 115, "low": 95, "high": 130, "when": "2025-07 +/- 8 months"}
    out["peak_over_panel_central"] = round(pk_s[2] / 115, 2)
    panel_month = (2025, 7)
    out["peak_months_before_panel"] = (panel_month[0] - pk_s[0]) * 12 + (panel_month[1] - pk_s[1])

    # every earlier cycle's smoothed maximum, split at smoothed minima found as the lowest
    # value in a 10-year window (crude but standard enough for a ranking)
    peaks = []
    vals = s
    i = 0
    mins = []
    for k in range(60, len(vals) - 60):
        w = vals[k - 60:k + 61]
        if vals[k][2] == min(x[2] for x in w):
            if not mins or k - mins[-1] > 60:
                mins.append(k)
    for a, b in zip(mins, mins[1:] + [len(vals)]):
        seg = vals[a:b]
        peaks.append(max(seg, key=lambda r: r[2]))
    out["cycles_found"] = len(peaks)
    ranked = sorted(peaks, key=lambda r: -r[2])
    out["c25_rank_among_cycles"] = 1 + [r[2] for r in ranked].index(pk_s[2]) if pk_s in peaks else None
    out["all_cycle_peaks"] = peaks
    prev = peaks[-2] if len(peaks) >= 2 else None
    out["previous_cycle_peak"] = prev
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=1)
    for k in ("last_monthly", "last_smoothed", "c25_smoothed_peak", "c25_monthly_peak",
              "smoothed_months_after_peak", "last_smoothed_as_share_of_peak",
              "last_6_monthly_mean", "peak_over_panel_central", "peak_months_before_panel",
              "cycles_found", "c25_rank_among_cycles", "previous_cycle_peak"):
        print(k, out[k])
    print("last 12 monthly", [(r[0], r[1], r[2]) for r in c25m[-12:]])


if __name__ == "__main__":
    main()
