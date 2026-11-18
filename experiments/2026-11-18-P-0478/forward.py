#!/usr/bin/env python3
"""P-0478: which of tonight's joined Munich markets are new since P-0434 (13 Nov),
and how the favourite did on those alone, by the same 0.40 cut."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = Path("/Users/triton/PROTEUS/experiments/2026-11-13-P-0434/results.json")

old = {r["market_id"] for r in json.loads(OLD.read_text())["rows"]}
new = json.loads((HERE / "results.json").read_text())
fwd = [r for r in new["rows"] if r["market_id"] not in old]


def cut(rows):
    hi = [r for r in rows if r["fav_mid"] >= 0.40]
    lo = [r for r in rows if r["fav_mid"] < 0.40]
    return {"n": len(rows), "won": sum(r["fav_won"] for r in rows),
            "at_0.40_plus": {"n": len(hi), "won": sum(r["fav_won"] for r in hi)},
            "under_0.40": {"n": len(lo), "won": sum(r["fav_won"] for r in lo)}}


def back(rows):
    pl = [(1.0 / (r["fav_mid"] + r["fav_spread"] / 2.0) - 1.0) * 0.98 if r["fav_won"] else -1.0 for r in rows]
    return round(sum(pl), 2)


out = {"p0434_rows": len(old), "tonight_rows": len(new["rows"]), "forward": cut(fwd),
       "forward_back_at_offer_0.40_plus_units": back([r for r in fwd if r["fav_mid"] >= 0.40]),
       "forward_back_at_offer_all_units": back(fwd),
       "forward_rows": [{k: r[k] for k in ("event", "favourite", "fav_mid", "winner", "fav_won", "two_sided")} for r in fwd]}
(HERE / "forward.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
