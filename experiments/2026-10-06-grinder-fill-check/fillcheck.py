"""Grinder fill check, 6 Oct 2026: does the v0.2 book's profit survive a stricter take-profit fill?

The live rule books a take-profit the moment any one-minute candle's HIGH touches 2x. A wick can be
one trade. Three stricter rules, same stops, same cost model (paths.pnl_v02), saved candles only:

  touch   as booked: high >= 2x, fill at 2x (or the open if it gapped above)
  close   the minute must CLOSE at or above 2x; fill at that close
  late    the touch is seen, the sell lands at the NEXT minute's open, whatever it is
  depth   touch, but only if that minute traded at least 10x our stake in USD (else keep walking)

Read-only: writes only into this folder.
"""
import csv, json, sys
from pathlib import Path

ROOT = "/Users/triton/PROTEUS/"
sys.path.insert(0, ROOT + "grinder")
import paths  # noqa: E402

HERE = Path(__file__).parent
TP, SL, RUG, HOLD = paths.TAKE_PROFIT, paths.STOP_LOSS, paths.RUG_DROP, paths.TIME_STOP_H
STAKE_USD = 100 * paths.GBPUSD


def walk(c, entry, t0, mode):
    tp, stop, rug, horizon = entry * (1 + TP), entry * (1 + SL), entry * (1 + RUG), t0 + HOLD * 3600
    win = [x for x in c if t0 <= x[0] < horizon]
    for i, (ts, o, h, l, cl, v) in enumerate(win):
        if l <= rug:
            return ts, min(cl, o if o <= stop else stop), "rug"
        if l <= stop:
            return ts, (o if o <= stop else stop), "stop_loss"
        if h >= tp:
            if mode == "touch":
                return ts, (o if o >= tp else tp), "take_profit"
            if mode == "close" and cl >= tp:
                return ts, cl, "take_profit"
            if mode == "late":
                if i + 1 < len(win):
                    nxt = win[i + 1]
                    return nxt[0], nxt[1], "take_profit" if nxt[1] >= entry else "stop_loss"
                return ts, cl, "take_profit"
            if mode == "depth" and v >= 10 * STAKE_USD:   # GeckoTerminal volume is USD (currency=usd)
                return ts, (o if o >= tp else tp), "take_profit"
    if win:
        return win[-1][0], win[-1][4], "time_stop"
    return horizon, entry, "time_stop"


def volume_usd_unit(c):
    # GeckoTerminal ohlcv volume is in USD already for these pools if a typical minute is
    # thousands; report the raw figure so a reader can judge.
    return None


rows = [r for r in csv.DictReader(open(ROOT + "grinder/LEDGER.csv")) if r["rule_version"] == "v0.2" and r["exit_at"]]
modes = ["touch", "close", "late", "depth"]
per, missing = [], []
for r in rows:
    c = paths.load_saved(r["id"])
    if not c:
        missing.append(r["id"])
        continue
    entry, t0 = float(r["entry_price_usd"]), paths.parse(r["entered_at"]).timestamp()
    liq = float(r["entry_liq_usd"] or 0) or None
    rec = {"id": r["id"], "token": r["token"], "entered": r["entered_at"][:10],
           "ledger_reason": r["exit_reason"], "ledger_pnl": float(r["pnl_gbp"])}
    for m in modes:
        ts, fill, reason = walk(c, entry, t0, m)
        rec[m + "_reason"] = reason
        rec[m + "_pnl"] = paths.pnl_v02(entry, fill, reason, 100.0, liq)
    # the touch minute itself, for the wick question
    tp = entry * (1 + TP)
    touch = next((x for x in c if x[0] >= t0 and x[2] >= tp), None)
    if touch and rec["ledger_reason"] == "take_profit":
        ts, o, h, l, cl, v = touch
        rec["touch_close_vs_tp_pct"] = round(100 * (cl / tp - 1), 1)
        rec["touch_minute_volume"] = round(v, 1)
    per.append(rec)


def summary(sub):
    out = {"n": len(sub)}
    for m in modes:
        wins = sum(1 for r in sub if r[m + "_reason"] == "take_profit" and r[m + "_pnl"] > 0)
        out[m] = {"wins": wins, "net_gbp": round(sum(r[m + "_pnl"] for r in sub), 2),
                  "per_trade": round(sum(r[m + "_pnl"] for r in sub) / max(len(sub), 1), 2)}
    out["ledger_net_gbp"] = round(sum(r["ledger_pnl"] for r in sub), 2)
    return out


res = {"all_v02": summary(per),
       "first_4_days_25_to_28_sep": summary([r for r in per if r["entered"] < "2026-09-29"]),
       "last_7_days_29_sep_to_4_oct": summary([r for r in per if r["entered"] >= "2026-09-29"]),
       "missing_candles": missing}
tps = [r for r in per if r["ledger_reason"] == "take_profit"]
res["booked_wins_whose_touch_minute_closed_below_2x"] = sum(1 for r in tps if r.get("touch_close_vs_tp_pct", 0) < 0)
res["booked_wins"] = len(tps)
(HERE / "per_trade.json").write_text(json.dumps(per, indent=1))
(HERE / "summary.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
for r in tps:
    print(r["id"], r["token"], "touch close vs 2x", r.get("touch_close_vs_tp_pct"), "% vol", r.get("touch_minute_volume"),
          "| close", r["close_reason"], r["close_pnl"], "| late", r["late_reason"], r["late_pnl"], "| depth", r["depth_reason"], r["depth_pnl"])
