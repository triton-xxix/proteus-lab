"""Backfill rugcheck's creator and insider fields for every gate-passer in features.csv and compare
winners with losers. Caveat: rugcheck's report is today's state, not the state at entry. A creator's
launch count only grows and insider networks are mostly found at launch, so this is a lead to
pre-register on forward data, not a backtest.
Writes creator_insiders.csv and prints the comparison."""
import csv
import json
import os
import statistics
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "creator_insiders.csv")


def report(mint):
    url = "https://api.rugcheck.xyz/v1/tokens/%s/report" % mint
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(3 * (attempt + 1))
    return None


def main():
    rows = list(csv.DictReader(open(os.path.join(HERE, "features.csv"))))
    done = {}
    if os.path.exists(OUT):
        done = {r["mint"]: r for r in csv.DictReader(open(OUT))}
    out = []
    for r in rows:
        if r["mint"] in done:
            out.append(done[r["mint"]])
            continue
        rep = report(r["mint"]) or {}
        nets = rep.get("insiderNetworks") or []
        ct = rep.get("creatorTokens")
        out.append({"mint": r["mint"], "symbol": r["symbol"], "night": r["night"], "bought": r["bought"],
                    "outcome": r["outcome"], "pnl_gbp": r["pnl_gbp"],
                    "creator": rep.get("creator") or "",
                    "creator_tokens": "" if ct is None else len(ct),
                    "graph_insiders": "" if rep.get("graphInsidersDetected") is None else rep.get("graphInsidersDetected"),
                    "insider_networks": len(nets),
                    "insider_net_max_pct": max([(n.get("tokenAmount") or 0) / max(1, (rep.get("token") or {}).get("supply") or 1) * 100 for n in nets] or [0]),
                    "fetched": int(bool(rep))})
        time.sleep(0.4)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    got = [r for r in out if str(r["fetched"]) == "1"]
    print("fetched", len(got), "of", len(out))
    creators = {}
    for r in got:
        if r["creator"]:
            creators.setdefault(r["creator"], []).append(r)
    rep_c = {c: v for c, v in creators.items() if len(v) > 1}
    print("creators behind more than one gate-passer:", len(rep_c), [(c[:6], [(x["symbol"], x["outcome"]) for x in v]) for c, v in rep_c.items()])
    for k in ("creator_tokens", "graph_insiders", "insider_networks"):
        vals = [(float(r[k]), r["outcome"]) for r in got if r[k] not in ("", None)]
        if not vals:
            continue
        for name, sel in (("winners", "take_profit"), ("stopped", "stop_loss"), ("rugs", "rug")):
            xs = [v for v, o in vals if o == sel]
            if xs:
                print("%-17s %-8s median %6.1f  mean %6.1f  n %d" % (k, name, statistics.median(xs), statistics.mean(xs), len(xs)))
        s = sorted(vals)
        t = len(s) // 3
        if t and len({v for v, o in s}) > 3:
            parts = [s[:t], s[t:2 * t], s[2 * t:]]
            print("%-17s win rate by tercile: %s" % (k, " / ".join("%.0f%% (%.0f-%.0f)" % (
                100 * sum(o == "take_profit" for v, o in p) / len(p), p[0][0], p[-1][0]) for p in parts)))
        zero = [o for v, o in vals if v == 0]
        some = [o for v, o in vals if v > 0]
        if zero and some:
            print("%-17s zero: %.0f%% wins, %.0f%% rugs of %d | above zero: %.0f%% wins, %.0f%% rugs of %d" % (
                k, 100 * zero.count("take_profit") / len(zero), 100 * zero.count("rug") / len(zero), len(zero),
                100 * some.count("take_profit") / len(some), 100 * some.count("rug") / len(some), len(some)))


if __name__ == "__main__":
    main()
