"""P-0434: the Smarkets Munich favourite on the night before, against what settled.

Local only: exchange/SNAPSHOTS.csv (nightly quotes, prices in basis points) joined by market_id to
exchange/munich_outcomes.jsonl. For each settled market: the last snapshot taken before event_start
in which at least one contract has both a bid and an offer; the favourite is the highest mid.
"""
import csv, json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EX = Path("/Users/triton/PROTEUS/exchange")


def main():
    outcomes = {}
    for line in (EX / "munich_outcomes.jsonl").read_text().splitlines():
        if line.strip():
            o = json.loads(line)
            outcomes[o["market_id"]] = o
    snaps = defaultdict(lambda: defaultdict(list))   # market -> snap_utc -> rows
    with open(EX / "SNAPSHOTS.csv") as f:
        for r in csv.DictReader(f):
            if r["market_id"] in outcomes:
                snaps[r["market_id"]][r["snap_utc"]].append(r)
    rows, skipped = [], []
    for mid_, o in sorted(outcomes.items(), key=lambda kv: kv[0]):
        by_snap = snaps.get(mid_, {})
        chosen = None
        for ts in sorted(by_snap):
            rs = by_snap[ts]
            if ts >= rs[0]["event_start"]:
                continue
            if any(r["mid"] for r in rs):
                chosen = ts
        if not chosen:
            skipped.append({"market_id": mid_, "event": o["event"], "snapshots": len(by_snap),
                            "why": "no snapshot before the day with a two-sided price"})
            continue
        rs = by_snap[chosen]
        priced = [(float(r["mid"]) / 10000.0, r) for r in rs if r["mid"]]
        priced.sort(key=lambda x: -x[0])
        p, fav = priced[0]
        second = priced[1][0] if len(priced) > 1 else None
        win_row = next((r for r in rs if r["contract_id"] == o["winner_id"]), None)
        win_mid = float(win_row["mid"]) / 10000.0 if win_row and win_row["mid"] else None
        win_offer = float(win_row["offer"]) / 10000.0 if win_row and win_row["offer"] else None
        spread = (float(fav["offer"]) - float(fav["bid"])) / 10000.0
        rank = next((i + 1 for i, (_, r) in enumerate(priced) if r["contract_id"] == o["winner_id"]), None)
        rows.append({"market_id": mid_, "event": o["event"], "snap_utc": chosen, "event_start": rs[0]["event_start"],
                     "contracts": len(rs), "two_sided": len(priced), "sum_mids": round(sum(x for x, _ in priced), 3),
                     "favourite": fav["contract"], "fav_mid": round(p, 4), "fav_spread": round(spread, 4), "second_mid": second,
                     "winner": o["winner"], "fav_won": fav["contract_id"] == o["winner_id"],
                     "winner_mid": win_mid, "winner_offer": win_offer, "winner_rank_among_priced": rank})
    n = len(rows)
    wins = [r for r in rows if r["fav_won"]]
    loss = [r for r in rows if not r["fav_won"]]
    hit = len(wins) / n if n else None
    mean = lambda xs: round(sum(xs) / len(xs), 4) if xs else None
    brier_fav = mean([(r["fav_mid"] - (1.0 if r["fav_won"] else 0.0)) ** 2 for r in rows])
    brier_flat = mean([(hit - (1.0 if r["fav_won"] else 0.0)) ** 2 for r in rows])
    hi = [r for r in rows if r["fav_mid"] >= 0.40]
    lo = [r for r in rows if r["fav_mid"] < 0.40]
    summary = {"outcomes": len(outcomes), "joined": n, "skipped": len(skipped), "fav_won": len(wins), "hit_rate": round(hit, 3) if n else None,
               "mean_fav_mid": mean([r["fav_mid"] for r in rows]),
               "mean_fav_mid_won": mean([r["fav_mid"] for r in wins]), "mean_fav_mid_lost": mean([r["fav_mid"] for r in loss]),
               "brier_fav_price": brier_fav, "brier_flat_hit_rate": brier_flat,
               "fav_mid_0.40_plus": {"n": len(hi), "won": sum(1 for r in hi if r["fav_won"]), "mean_mid": mean([r["fav_mid"] for r in hi])},
               "fav_mid_under_0.40": {"n": len(lo), "won": sum(1 for r in lo if r["fav_won"]), "mean_mid": mean([r["fav_mid"] for r in lo])},
               "mean_fav_spread": mean([r["fav_spread"] for r in rows]), "mean_two_sided": mean([r["two_sided"] for r in rows]),
               "winner_unpriced": sum(1 for r in rows if r["winner_mid"] is None),
               "winner_rank": {str(k): sum(1 for r in rows if r["winner_rank_among_priced"] == k) for k in (1, 2, 3, 4, 5)},
               }
    # paper only: back the favourite at its offer (mid plus half the spread), 2% commission on winnings, 1 unit a night
    def back(sel):
        pl = []
        for r in sel:
            offer = r["fav_mid"] + r["fav_spread"] / 2.0
            pl.append((1.0 / offer - 1.0) * 0.98 if r["fav_won"] else -1.0)
        return {"n": len(pl), "total_units": round(sum(pl), 2), "mean_units": mean(pl)}
    summary["back_fav_at_offer_all"] = back(rows)
    summary["back_fav_at_offer_0.40_plus"] = back(hi)
    summary["back_fav_at_offer_under_0.40"] = back(lo)
    # chance of at least this many winners among the 0.40-plus favourites if each won at its own mid
    import random
    rnd = random.Random(434)
    k = summary["fav_mid_0.40_plus"]["won"]
    draws = 20000
    summary["p_at_least_this_many_if_mids_true_0.40_plus"] = round(
        sum(1 for _ in range(draws) if sum(1 for r in hi if rnd.random() < r["fav_mid"]) >= k) / draws, 4)
    k2 = summary["fav_mid_under_0.40"]["won"]
    summary["p_at_most_this_many_if_mids_true_under_0.40"] = round(
        sum(1 for _ in range(draws) if sum(1 for r in lo if rnd.random() < r["fav_mid"]) <= k2) / draws, 4)
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows, "skipped": skipped}, indent=1, ensure_ascii=False))
    for r in rows:
        print(r["event"], "| snap", r["snap_utc"][5:16], "| priced", r["two_sided"], "of", r["contracts"], "sum", r["sum_mids"],
              "| fav", r["favourite"], r["fav_mid"], "spread", r["fav_spread"], "| winner", r["winner"], "mid", r["winner_mid"],
              "rank", r["winner_rank_among_priced"], "| WON" if r["fav_won"] else "| lost")
    for s in skipped:
        print("SKIPPED", s)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
