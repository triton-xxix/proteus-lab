"""What do the Grinder's winners have in common, and its losers? (Luke's questions, 9 Oct 2026.)

Population: every gate-passer since 22 Sep (replay2.population, group "pass"), each replayed under
v0.2's exit (V01: +100% / -50% / 24h, v0.2 costs) on its cached GeckoTerminal minute candles. Also the
subset the live book actually bought (top 4 by 1h volume a night = LEDGER.csv v0.2).
For each feature known at the snapshot: medians for winners, stop-outs and rugs, and the win rate by
tercile of the feature. Small samples: this is a list of leads to pre-register, not a result.
Writes features.csv and report.txt beside this file.
"""
import csv
import os
import statistics
import sys
import time

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
sys.path.insert(0, "/Users/triton/PROTEUS/grinder/harness")
import paper  # noqa: E402
import replay  # noqa: E402
import replay2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
f = paper.fnum


def feats(r, m):
    b, s = f(r.get("buys_h1")) or 0, f(r.get("sells_h1")) or 0
    liq, v1, mc = f(r.get("liq_usd")), f(r.get("vol_h1")), f(r.get("mcap_usd"))
    tg = replay2.src_count(r, m, "telegram")
    rd = replay2.src_count(r, m, "reddit")
    xx = replay2.src_count(r, m, "x")
    paid = replay2.paid_before(r, m)
    return {
        "age_h": f(r.get("age_h")),
        "liq_usd": liq,
        "mcap_usd": mc,
        "mcap_per_liq": (mc / liq) if mc and liq else None,
        "vol_h1": v1,
        "vol_h24": f(r.get("vol_h24")),
        "turnover_h1": (v1 / liq) if v1 and liq else None,
        "h1_share_of_24h": (v1 / f(r.get("vol_h24"))) if v1 and f(r.get("vol_h24")) else None,
        "trades_h1": b + s,
        "buy_share_h1": b / (b + s) if b + s else None,
        "chg_h1": f(r.get("chg_h1")),
        "chg_h24": f(r.get("chg_h24")),
        "top10_pct": f(r.get("top10_pct")),
        "holders": f(r.get("holders")),
        "lp_locked_pct": f(r.get("lp_locked_pct")),
        "rug_score": f(r.get("rug_score")),
        "rug_risk_named": 1.0 if (r.get("rug_risks") or "").strip() else 0.0,
        "socials": f(r.get("socials")),
        "pumpswap": 1.0 if r.get("dex") == "pumpswap" else 0.0,
        "tg_mentions": tg,
        "reddit_mentions": rd,
        "x_mentions": xx,
        "paid_promo": None if paid is None else (1.0 if paid else 0.0),
    }


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def fmt(x):
    if x is None:
        return "-"
    return ("%.0f" % x) if abs(x) >= 100 else ("%.2f" % x)


def report(rows, title):
    out = ["", "## " + title, "n %d: wins %d, stop-outs %d, rugs %d, time stops %d, mean £%.1f" % (
        len(rows), sum(r["out"] == "take_profit" for r in rows), sum(r["out"] == "stop_loss" for r in rows),
        sum(r["out"] == "rug" for r in rows), sum(r["out"] == "time_stop" for r in rows),
        statistics.mean(r["pnl"] for r in rows))]
    out.append("%-17s %9s %9s %9s | win rate by tercile low / mid / high (n)" % ("feature", "winners", "stopped", "rugs"))
    for k in rows[0]["f"]:
        w = med(r["f"][k] for r in rows if r["out"] == "take_profit")
        s = med(r["f"][k] for r in rows if r["out"] == "stop_loss")
        g = med(r["f"][k] for r in rows if r["out"] == "rug")
        have = sorted([r for r in rows if r["f"][k] is not None], key=lambda r: r["f"][k])
        terc = ""
        vals = {r["f"][k] for r in have}
        if len(have) >= 15 and len(vals) > 3:
            t = len(have) // 3
            parts = [have[:t], have[t:2 * t], have[2 * t:]]
            terc = " / ".join("%2.0f%%" % (100 * sum(r["out"] == "take_profit" for r in p) / len(p)) for p in parts)
            terc += "  (%d)" % len(have)
        elif len(have) >= 10 and vals <= {0.0, 1.0}:
            a = [r for r in have if r["f"][k] == 0]
            b = [r for r in have if r["f"][k] == 1]
            if a and b:
                terc = "no: %2.0f%% of %d, yes: %2.0f%% of %d" % (
                    100 * sum(r["out"] == "take_profit" for r in a) / len(a), len(a),
                    100 * sum(r["out"] == "take_profit" for r in b) / len(b), len(b))
        out.append("%-17s %9s %9s %9s | %s" % (k, fmt(w), fmt(s), fmt(g), terc))
    return out


def main():
    m = replay2.mentions()
    pop = [(r, replay.candles(r, True)) for r in replay2.population(time.time()) if r.get("_grp") == "pass"]
    pop = [(r, c) for r, c in pop if c]
    res = {(x["mint"], x["night"]): x for x in replay.run_variant("V01", pop)}
    ledger = {(x["mint"], x["entered_at"][:10]) for x in csv.DictReader(open("/Users/triton/PROTEUS/grinder/LEDGER.csv"))
              if x["rule_version"] == "v0.2"}
    rows = []
    for r, c in pop:
        x = res.get((r["mint"], r["ts"][:10]))
        if not x:
            continue
        rows.append({"r": r, "f": feats(r, m), "out": x["reason"], "pnl": x["pnl"],
                     "bought": (r["mint"], r["ts"][:10]) in ledger})
    lines = ["# Winners and losers, every gate-passer replayed under v0.2 exits (built %s)" % time.strftime("%Y-%m-%d %H:%M")]
    lines += report(rows, "All gate-passers")
    lines += report([r for r in rows if r["bought"]], "Only the ones the live book bought")
    lines += report([r for r in rows if not r["bought"]], "Gate-passers the book did not buy")
    txt = "\n".join(lines)
    print(txt)
    open(os.path.join(HERE, "report.txt"), "w").write(txt + "\n")
    with open(os.path.join(HERE, "features.csv"), "w", newline="") as fh:
        keys = list(rows[0]["f"])
        w = csv.writer(fh)
        w.writerow(["night", "symbol", "mint", "bought", "outcome", "pnl_gbp"] + keys)
        for r in rows:
            w.writerow([r["r"]["ts"][:10], r["r"]["symbol"], r["r"]["mint"], int(r["bought"]), r["out"], round(r["pnl"], 2)]
                       + [("" if r["f"][k] is None else round(r["f"][k], 4)) for k in keys])


if __name__ == "__main__":
    main()
