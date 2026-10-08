"""The four live-book losers that fell through -50% and then ran past +100% (Agency, Human, AIRPAD,
EGO): what the minute candles and the cached Telegram channels show around the low and the bounce.
For comparison, the same numbers for the stop-outs that never came back."""
import csv
import glob
import json
import os
import statistics
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper  # noqa: E402

ROOT = "/Users/triton/PROTEUS/"
H = 3600
P = {r["id"]: r for r in csv.DictReader(open(ROOT + "grinder/PATHS.csv"))}
L = [r for r in csv.DictReader(open(ROOT + "grinder/LEDGER.csv")) if r["rule_version"] == "v0.2" and r["exit_reason"]]


def ts(s):
    from datetime import datetime, timezone
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def candles(r):
    p = ROOT + "grinder/candles/%s.csv" % r["id"]
    if not os.path.exists(p):
        p = ROOT + "grinder/harness/candles/%s_%s.csv" % (r["mint"][:16], r["entered_at"][:10])
    if not os.path.exists(p):
        return None
    rows = list(csv.reader(open(p)))
    return [[float(x) for x in row] for row in rows[1:] if row and row[0].replace(".", "").isdigit()]


TG = {}
for fp in glob.glob(ROOT + "state/research/telegram/*.jsonl"):
    ch = os.path.basename(fp)[:-6]
    for line in open(fp):
        try:
            m = json.loads(line)
        except ValueError:
            continue
        TG.setdefault(ch, []).append(m)


def tg_hits(mint, symbol, t0, t1):
    out = []
    for ch, msgs in TG.items():
        for m in msgs:
            if t0 <= m.get("t", 0) < t1 and (mint in (m.get("text") or "") or mint[:20] in (m.get("text") or "")):
                out.append((m["t"], ch))
    return sorted(out)


def profile(r):
    c = candles(r)
    if not c:
        return None
    t0 = ts(r["entered_at"])
    e = float(r["entry_price_usd"])
    w = [x for x in c if t0 <= x[0] < t0 + 24 * H]
    if not w:
        return None
    lo = min(w, key=lambda x: x[3])
    after = [x for x in w if x[0] >= lo[0]]
    hi = max(after, key=lambda x: x[2])
    vol_before_low = sum(x[5] for x in w if x[0] < lo[0])
    vol_low_hour = sum(x[5] for x in w if lo[0] - H <= x[0] < lo[0])
    vol_after = sum(x[5] for x in w if lo[0] <= x[0] < hi[0])
    hits = tg_hits(r["mint"], r["token"], t0 - 24 * H, t0 + 24 * H)
    return {
        "token": r["token"], "night": r["entered_at"][:10], "exit": r["exit_reason"],
        "low_pct": round(100 * (lo[3] / e - 1)), "low_after_h": round((lo[0] - t0) / H, 1),
        "bounce_peak_pct": round(100 * (hi[2] / e - 1)), "peak_after_low_h": round((hi[0] - lo[0]) / H, 1),
        "bounce_x_from_low": round(hi[2] / lo[3], 1),
        "usd_vol_first_to_low": round(vol_before_low), "usd_vol_hour_into_low": round(vol_low_hour),
        "usd_vol_low_to_peak": round(vol_after),
        "tg_calls_24h_before_entry": sum(1 for t, ch in hits if t < t0),
        "tg_calls_entry_to_low": sum(1 for t, ch in hits if t0 <= t < lo[0]),
        "tg_calls_low_to_peak": sum(1 for t, ch in hits if lo[0] <= t < hi[0]),
        "tg_channels_low_to_peak": sorted({ch for t, ch in hits if lo[0] <= t < hi[0]}),
    }


def main():
    bounce = {"Agency", "Human", "AIRPAD", "EGO"}
    out = {"bounced": [], "stayed_down": []}
    for r in L:
        if r["exit_reason"] not in ("stop_loss", "rug"):
            continue
        p = profile(r)
        if not p:
            continue
        (out["bounced"] if r["token"] in bounce else out["stayed_down"]).append(p)
    for p in out["bounced"]:
        print(json.dumps(p))
    sd = out["stayed_down"]
    print("stayed-down stop-outs: n", len(sd))
    for k in ("bounce_x_from_low", "low_after_h", "tg_calls_24h_before_entry", "tg_calls_low_to_peak", "usd_vol_low_to_peak"):
        print("  median", k, statistics.median(p[k] for p in sd))
    print("  share with any Telegram call between low and bounce peak:",
          round(sum(p["tg_calls_low_to_peak"] > 0 for p in sd) / len(sd), 2))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bounce.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
