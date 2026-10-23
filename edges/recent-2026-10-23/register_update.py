#!/usr/bin/env python3
"""Write the 23 Oct 2026 admission results into REGISTER.csv and add the video candidates E-008 to E-010."""
import csv
import json

REG = "/Users/triton/PROTEUS/edges/REGISTER.csv"
res = json.load(open("/Users/triton/PROTEUS/edges/recent-2026-10-23/admission.json"))
rows = list(csv.DictReader(open(REG)))
fields = list(rows[0].keys())


def line(k):
    r = res[k]
    if r["n"] == 0:
        return "NOT ADMITTED 23 Oct 2026: 0 signal days in the window (%s); nothing to test" % "; ".join(
            "%s %s" % (c, v["window"]) for c, v in r["per_coin"].items())
    return ("NOT ADMITTED 23 Oct 2026: %s; n %d, mean net %+.2f%% median %+.2f%%, winners %d (needed %d), "
            "random control mean %+.2f%%, perm p %.2f; costs %.2f%% round trip" % (
                r["window"], r["n"], r["mean_net_pct"], r["median_net_pct"], r["winners"], r["winners_needed"],
                r["control_mean_pct"], r["perm_p"], r["cost_round_trip_pct"]))


for row in rows:
    if row["id"] in ("E-003", "E-004", "E-006"):
        row["admission"] = line(row["id"]) + "; script edges/recent-2026-10-23/admission.py (5038b57); earlier: " + row["admission"]
        row["forward"] = "retest on the next window when the nightly cadence comes round"

new = [
    ("E-008", "5-minute opening range breakout on single stocks (TSLA META NVDA AMD AAPL AMZN; SPY QQQ as control)",
     "video V1 TOS Indicators, experiments/2026-10-23-trading-videos"),
    ("E-009", "Crypto 1-hour Bollinger long/short with 4-hour RSI trend and ADX filters, Binance perps",
     "video V3 Quant Tactics, experiments/2026-10-23-trading-videos"),
    ("E-010", "Fade the London move at the NY open (15-minute ORB against London's direction), BTC or NQ",
     "video V2 Trade with Pat, experiments/2026-10-23-trading-videos"),
]
for i, name, src in new:
    if not any(r["id"] == i for r in rows):
        rows.append({"id": i, "name": name, "source": src, "status": "candidate", "admitted": "",
                     "window": "to pick, see NOTES.md", "admission": "not run; the video's own numbers are claims, not admission",
                     "kill_line": "to fix at admission", "forward": ""})

with open(REG, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print("register rows:", len(rows))
