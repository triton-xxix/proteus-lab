"""P-0433: how often do opening gaps fill, and does fading them pay? Rules are in README.md.

Local only: reads sandbox/p0082/data/<SYM>.csv (Yahoo daily, price only). Seeded.
"""
import csv, json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = Path("/Users/triton/PROTEUS/sandbox/p0082/data")
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
MIN_GAP, COST, DRAWS = 0.0005, 0.0002, 2000
BUCKETS = [(0.0005, 0.0025, "0.05-0.25%"), (0.0025, 0.005, "0.25-0.5%"), (0.005, 0.01, "0.5-1%"), (0.01, 9.0, "over 1%")]
RNG = np.random.default_rng(433)


def load(sym):
    d, o, h, l, c = [], [], [], [], []
    with open(DATA / (sym + ".csv")) as f:
        for r in csv.DictReader(f):
            try:
                vals = [float(r[k]) for k in ("open", "high", "low", "close")]
            except ValueError:
                continue
            if min(vals) <= 0:
                continue
            d.append(r["date"]); o.append(vals[0]); h.append(vals[1]); l.append(vals[2]); c.append(vals[3])
    return d, np.array(o), np.array(h), np.array(l), np.array(c)


def gaps(sym, since=None):
    d, o, h, l, c = load(sym)
    rows = []
    n = len(d)
    for t in range(1, n):
        if since and d[t] < since:
            continue
        pc = c[t - 1]
        g = o[t] / pc - 1.0
        if abs(g) < MIN_GAP:
            continue
        up = g > 0
        dist = abs(o[t] - pc)
        mirror = o[t] + dist if up else o[t] - dist

        def filled(k):
            e = min(n, t + k)
            return bool(l[t:e].min() <= pc) if up else bool(h[t:e].max() >= pc)

        f1 = filled(1)
        mir = bool(h[t] >= mirror) if up else bool(l[t] <= mirror)
        oc = c[t] / o[t] - 1.0
        # filled: the move from the open to yesterday's close, as a share of the open; else out at the close
        fade = dist / o[t] if f1 else (-oc if up else oc)
        follow = dist / o[t] if mir else (oc if up else -oc)
        up = bool(up)
        rows.append({"sym": sym, "date": d[t], "gap": g, "abs": abs(g), "up": up,
                     "chart": bool(o[t] > h[t - 1]) if up else bool(o[t] < l[t - 1]),
                     "f1": f1, "f5": filled(5), "f20": filled(20), "mirror": mir,
                     "fade": fade, "follow": follow})
    alloc = float(np.mean(c[1:] / o[1:] - 1.0)) if not since else float(np.mean([c[t] / o[t] - 1.0 for t in range(1, n) if d[t] >= since]))
    days = n - 1 if not since else sum(1 for t in range(1, n) if d[t] >= since)
    return rows, days, alloc


def rate(rows, key):
    return round(100.0 * sum(1 for r in rows if r[key]) / len(rows), 1) if rows else None


def summarise(rows):
    if not rows:
        return {"gaps": 0}
    fade = np.array([r["fade"] for r in rows]) - COST
    follow = np.array([r["follow"] for r in rows]) - COST
    means = []
    for i in range(0, DRAWS, 100):
        pick = RNG.random((100, len(rows))) < 0.5
        means.extend(np.where(pick, fade, follow).mean(axis=1).tolist())
    means = np.array(means)
    out = {"gaps": len(rows), "fill_same_day": rate(rows, "f1"), "fill_5d": rate(rows, "f5"), "fill_20d": rate(rows, "f20"),
           "mirror_same_day": rate(rows, "mirror"),
           "fade_mean_pct": round(100 * float(fade.mean()), 4), "fade_mean_before_cost_pct": round(100 * float(fade.mean() + COST), 4),
           "fade_win_pct": round(100 * float((fade > 0).mean()), 1),
           "fade_worst_pct": round(100 * float(fade.min()), 2),
           "fade_t": round(float(fade.mean() / (fade.std(ddof=1) / np.sqrt(len(fade)))), 2),
           "follow_mean_pct": round(100 * float(follow.mean()), 4),
           "coin_mean_pct": round(100 * float(means.mean()), 4),
           "p_fade_v_coin": round(float((means >= fade.mean()).mean()), 4)}
    out["buckets"] = {}
    for lo, hi, name in BUCKETS:
        b = [r for r in rows if lo <= r["abs"] < hi]
        if b:
            bf = np.array([r["fade"] for r in b]) - COST
            out["buckets"][name] = {"gaps": len(b), "fill_same_day": rate(b, "f1"), "fill_5d": rate(b, "f5"), "fill_20d": rate(b, "f20"),
                                    "mirror_same_day": rate(b, "mirror"), "fade_mean_pct": round(100 * float(bf.mean()), 4)}
    ch = [r for r in rows if r["chart"]]
    if ch:
        cf = np.array([r["fade"] for r in ch]) - COST
        out["chart_gaps"] = {"gaps": len(ch), "fill_same_day": rate(ch, "f1"), "fill_5d": rate(ch, "f5"), "fill_20d": rate(ch, "f20"),
                             "mirror_same_day": rate(ch, "mirror"), "fade_mean_pct": round(100 * float(cf.mean()), 4)}
    for side, flag in (("up", True), ("down", False)):
        s = [r for r in rows if r["up"] is flag]
        if s:
            sf = np.array([r["fade"] for r in s]) - COST
            out[side] = {"gaps": len(s), "fill_same_day": rate(s, "f1"), "fade_mean_pct": round(100 * float(sf.mean()), 4)}
    return out


def main():
    res = {"rules": {"min_gap": MIN_GAP, "cost_round_trip": COST, "draws": DRAWS, "basket": BASKET}}
    for label, since in (("all", None), ("since_2009", "2009-01-01")):
        pooled, block = [], {}
        for sym in BASKET:
            rows, days, oc = gaps(sym, since)
            pooled.extend(rows)
            s = summarise(rows)
            s["days"], s["first"], s["last"], s["open_to_close_all_days_pct"] = days, rows[0]["date"], rows[-1]["date"], round(100 * oc, 4)
            block[sym] = s
            print(label, sym, s["gaps"], "gaps of", days, "days | fill 1d", s["fill_same_day"], "5d", s["fill_5d"], "20d", s["fill_20d"],
                  "| mirror", s["mirror_same_day"], "| fade mean", s["fade_mean_pct"], "win", s["fade_win_pct"], "t", s["fade_t"],
                  "p", s["p_fade_v_coin"], "| o-c all days", s["open_to_close_all_days_pct"])
        block["POOLED"] = summarise(pooled)
        p = block["POOLED"]
        print(label, "POOLED", p["gaps"], "| fill 1d", p["fill_same_day"], "5d", p["fill_5d"], "20d", p["fill_20d"], "| mirror", p["mirror_same_day"],
              "| fade mean", p["fade_mean_pct"], "win", p["fade_win_pct"], "worst", p["fade_worst_pct"], "t", p["fade_t"], "follow", p["follow_mean_pct"],
              "coin", p["coin_mean_pct"], "p", p["p_fade_v_coin"])
        for name, b in p["buckets"].items():
            print("   ", label, "POOLED bucket", name, b)
        print("   ", label, "POOLED chart gaps", p.get("chart_gaps"))
        print("   ", label, "POOLED up", p.get("up"), "down", p.get("down"))
        print("   ", label, "SPY buckets", json.dumps(block["SPY"]["buckets"]))
        print("   ", label, "SPY chart gaps", block["SPY"].get("chart_gaps"))
        res[label] = block
    (HERE / "results.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
