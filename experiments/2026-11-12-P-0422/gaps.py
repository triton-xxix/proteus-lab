"""P-0422: where the market and I disagree on my own Munich degree, who is nearer?

Reads exchange/BOOK.csv (read only). A row counts when it is a Munich "Highest Temperature" call,
settled (outcome winner or loser) and anchored (market_mid present).

Usage: python3 gaps.py /abs/path/results.json
"""
import csv
import json
import sys

BOOK = "/Users/triton/PROTEUS/exchange/BOOK.csv"


def summary(rows):
    n = len(rows)
    if not n:
        return {"n": 0}
    mine = sum((r["p"] - r["y"]) ** 2 for r in rows) / n
    mkt = sum((r["mid"] - r["y"]) ** 2 for r in rows) / n
    return {"n": n, "winners": sum(r["y"] for r in rows), "my_brier": round(mine, 4), "market_brier": round(mkt, 4),
            "me_minus_market": round(mine - mkt, 4), "mean_p": round(sum(r["p"] for r in rows) / n, 3),
            "mean_mid": round(sum(r["mid"] for r in rows) / n, 3),
            "rows_i_was_nearer": sum(1 for r in rows if abs(r["p"] - r["y"]) < abs(r["mid"] - r["y"]))}


def main(out_path):
    rows, skipped = [], {"not_munich": 0, "unsettled": 0, "no_anchor": 0}
    for r in csv.DictReader(open(BOOK)):
        if r["market"] != "Highest Temperature":
            skipped["not_munich"] += 1
            continue
        if r["outcome"] not in ("winner", "loser"):
            skipped["unsettled"] += 1
            continue
        if not r["market_mid"]:
            skipped["no_anchor"] += 1
            continue
        rows.append({"id": r["id"], "event": r["event"], "contract": r["contract"], "p": float(r["p"]),
                     "mid": float(r["market_mid"]), "y": 1 if r["outcome"] == "winner" else 0,
                     "open_ended": ("higher" in r["contract"] or "below" in r["contract"] or "lower" in r["contract"])})
    for r in rows:
        r["gap"] = round(r["mid"] - r["p"], 4)
    big = [r for r in rows if abs(r["gap"]) >= 0.10]
    out = {"skipped": skipped, "all": summary(rows),
           "gap_010_or_more": summary(big), "gap_under_010": summary([r for r in rows if abs(r["gap"]) < 0.10]),
           "market_above_me_by_010": summary([r for r in big if r["gap"] > 0]),
           "market_below_me_by_010": summary([r for r in big if r["gap"] < 0]),
           "share_big": round(len(big) / len(rows), 3) if rows else None,
           "single_degree": summary([r for r in rows if not r["open_ended"]]),
           "open_ended": summary([r for r in rows if r["open_ended"]]),
           "big_rows": sorted(big, key=lambda r: -abs(r["gap"]))}
    # does the sign of the gap carry anything: winners' share where market was above me v below me (any size)
    out["market_above_me_any"] = summary([r for r in rows if r["gap"] > 0])
    out["market_below_me_any"] = summary([r for r in rows if r["gap"] < 0])
    json.dump(out, open(out_path, "w"), indent=1)
    for k in ("skipped", "all", "share_big", "gap_010_or_more", "gap_under_010", "market_above_me_by_010",
              "market_below_me_by_010", "market_above_me_any", "market_below_me_any", "single_degree", "open_ended"):
        print(k, json.dumps(out[k]))
    for r in out["big_rows"]:
        print("  %s %-22s %-16s p %.2f mid %.3f gap %+.3f y %d" % (r["id"], r["event"], r["contract"], r["p"], r["mid"], r["gap"], r["y"]))


if __name__ == "__main__":
    main(sys.argv[1])
