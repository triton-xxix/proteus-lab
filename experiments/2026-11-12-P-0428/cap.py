"""P-0428: the exchange book's single-degree cap, fitted in sample, and the EPS band as a signal.

Reads exchange/BOOK.csv and exchange/icon_eps_band.jsonl (read only). Rows: settled Munich
"Highest Temperature" calls on a single degree (open-ended top and bottom bins left out).
In sample throughout: this describes the rows, it does not test a rule.
"""
import csv
import json
import re
import sys
from datetime import datetime

MONTHS = {"October": 10, "November": 11, "December": 12, "September": 9}
rows = []
for r in csv.DictReader(open("/Users/triton/PROTEUS/exchange/BOOK.csv")):
    if r["market"] != "Highest Temperature" or r["outcome"] not in ("winner", "loser"):
        continue
    if any(w in r["contract"] for w in ("higher", "below", "lower")):
        continue
    m = re.match(r"(\w+) (\d+)\w+, (\d{4})", r["event"])
    day = "%s-%02d-%02d" % (m.group(3), MONTHS[m.group(1)], int(m.group(2)))
    lead = (datetime.strptime(day, "%Y-%m-%d") - datetime.strptime(r["committed_at"][:10], "%Y-%m-%d")).days
    rows.append({"id": r["id"], "day": day, "lead_days": lead, "p": float(r["p"]), "y": 1 if r["outcome"] == "winner" else 0,
                 "mid": float(r["market_mid"]) if r["market_mid"] else None, "degree": int(re.match(r"(-?\d+)", r["contract"]).group(1))})


def brier(ps, ys):
    return round(sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ys), 4)


ys = [r["y"] for r in rows]
n, w = len(rows), sum(ys)
out = {"n": n, "winners": w, "hit_rate": round(w / n, 3), "my_brier": brier([r["p"] for r in rows], ys),
       "mean_p": round(sum(r["p"] for r in rows) / n, 3)}
grid = {("%.2f" % (k / 100)): brier([k / 100] * n, ys) for k in range(10, 61, 5)}
out["flat_p_grid"] = grid
out["best_flat_p"] = round(w / n, 3)
out["best_flat_brier"] = brier([w / n] * n, ys)
anch = [r for r in rows if r["mid"] is not None]
out["anchored"] = {"n": len(anch), "market_brier": brier([r["mid"] for r in anch], [r["y"] for r in anch]),
                   "my_brier": brier([r["p"] for r in anch], [r["y"] for r in anch]),
                   "flat_at_hit_rate": brier([sum(r["y"] for r in anch) / len(anch)] * len(anch), [r["y"] for r in anch])}
# by lead and by era (the +1C city correction was dropped on 9 Nov's call for 11 Nov)
for key, f in (("lead_1", lambda r: r["lead_days"] <= 1), ("lead_2_plus", lambda r: r["lead_days"] >= 2),
               ("with_plus_1C_to_10_Nov", lambda r: r["day"] <= "2026-11-10"), ("metar_rule_from_11_Nov", lambda r: r["day"] > "2026-11-10")):
    rs = [r for r in rows if f(r)]
    out[key] = {"n": len(rs), "winners": sum(r["y"] for r in rs)} if rs else {"n": 0}
# EPS band width on the day, where captured
band = {}
for line in open("/Users/triton/PROTEUS/exchange/icon_eps_band.jsonl"):
    b = json.loads(line)
    band[b["day"]] = b
bw = [dict(r, width=round(band[r["day"]]["p90"] - band[r["day"]]["p10"], 2),
           in_band=band[r["day"]]["p10"] - 0.5 <= r["degree"] <= band[r["day"]]["p90"] + 0.5) for r in rows if r["day"] in band]
won = [r["width"] for r in bw if r["y"]]
lost = [r["width"] for r in bw if not r["y"]]
out["eps"] = {"rows_with_band": len(bw), "won": len(won), "lost": len(lost),
              "mean_width_won": round(sum(won) / len(won), 2) if won else None,
              "mean_width_lost": round(sum(lost) / len(lost), 2) if lost else None,
              "narrow_half_hit": None, "rows": [{k: r[k] for k in ("id", "day", "degree", "p", "y", "width", "in_band")} for r in bw]}
if len(bw) >= 4:
    srt = sorted(bw, key=lambda r: r["width"])
    half = len(srt) // 2
    out["eps"]["narrow_half_hit"] = "%d of %d" % (sum(r["y"] for r in srt[:half]), half)
    out["eps"]["wide_half_hit"] = "%d of %d" % (sum(r["y"] for r in srt[half:]), len(srt) - half)
json.dump(out, open(sys.argv[1], "w"), indent=1)
for k, v in out.items():
    if k != "eps":
        print(k, json.dumps(v))
e = out["eps"]
print("eps", {k: e[k] for k in e if k != "rows"})
for r in e["rows"]:
    print("  ", r)
