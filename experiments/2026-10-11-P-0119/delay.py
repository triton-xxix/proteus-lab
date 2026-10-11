"""P-0119 (D-003): the Grinder's v0.2 book with entry one minute after the snapshot.

Same trades, same stops, same cost model (paths.pnl_v02), saved candles only, as
../2026-10-06-grinder-fill-check/fillcheck.py. Variant: instead of filling at the snapshot price, buy at
the OPEN of the first one-minute candle starting at least 60 s after the snapshot, and set the take-profit,
stop and rug lines from that price. Exits use the booked "touch" rule. Read-only; writes into this folder.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = "/Users/triton/PROTEUS/"
sys.path.insert(0, ROOT + "grinder")
sys.path.insert(0, ROOT + "experiments/2026-10-06-grinder-fill-check")
import paths  # noqa: E402

HERE = Path(__file__).parent
TP, SL, RUG, HOLD = paths.TAKE_PROFIT, paths.STOP_LOSS, paths.RUG_DROP, paths.TIME_STOP_H


def walk(c, entry, t0, horizon):
    tp, stop, rug = entry * (1 + TP), entry * (1 + SL), entry * (1 + RUG)
    win = [x for x in c if t0 <= x[0] < horizon]
    for ts, o, h, l, cl, v in win:
        if l <= rug:
            return ts, min(cl, o if o <= stop else stop), "rug"
        if l <= stop:
            return ts, (o if o <= stop else stop), "stop_loss"
        if h >= tp:
            return ts, (o if o >= tp else tp), "take_profit"
    if win:
        return win[-1][0], win[-1][4], "time_stop"
    return horizon, entry, "time_stop"


rows = [r for r in csv.DictReader(open(ROOT + "grinder/LEDGER.csv")) if r["rule_version"] == "v0.2" and r["exit_at"]]
per, missing, no_next = [], [], []
for r in rows:
    c = paths.load_saved(r["id"])
    if not c:
        missing.append(r["id"])
        continue
    entry0, t0 = float(r["entry_price_usd"]), paths.parse(r["entered_at"]).timestamp()
    horizon = t0 + HOLD * 3600
    liq = float(r["entry_liq_usd"] or 0) or None
    base = walk(c, entry0, t0, horizon)
    nxt = next((x for x in c if x[0] >= t0 + 60), None)
    if not nxt or nxt[0] >= horizon:
        no_next.append(r["id"])
        continue
    entry1 = nxt[1]
    d = walk(c, entry1, nxt[0], horizon)
    per.append({"id": r["id"], "token": r["token"], "entered": r["entered_at"][:10],
                "slip_pct": round(100 * (entry1 / entry0 - 1), 2),
                "base_reason": base[2], "base_pnl": paths.pnl_v02(entry0, base[1], base[2], 100.0, liq),
                "delay_reason": d[2], "delay_pnl": paths.pnl_v02(entry1, d[1], d[2], 100.0, liq),
                "ledger_pnl": float(r["pnl_gbp"])})

n = len(per)
slips = sorted(p["slip_pct"] for p in per)
res = {"n": n, "missing_candles": missing, "no_minute_after": no_next,
       "median_entry_slip_pct": slips[n // 2] if n else None,
       "base_net_gbp": round(sum(p["base_pnl"] for p in per), 2),
       "delay_net_gbp": round(sum(p["delay_pnl"] for p in per), 2),
       "base_per_trade": round(sum(p["base_pnl"] for p in per) / max(n, 1), 2),
       "delay_per_trade": round(sum(p["delay_pnl"] for p in per) / max(n, 1), 2),
       "base_wins": sum(1 for p in per if p["base_reason"] == "take_profit"),
       "delay_wins": sum(1 for p in per if p["delay_reason"] == "take_profit"),
       "delay_better_trades": sum(1 for p in per if p["delay_pnl"] > p["base_pnl"]),
       "delay_worse_trades": sum(1 for p in per if p["delay_pnl"] < p["base_pnl"])}
(HERE / "per_trade.json").write_text(json.dumps(per, indent=1))
(HERE / "summary.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
